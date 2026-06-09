from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.text import Text
from ui.logo import logo
from ui.theme import ui
from llm import F
from queue_state import enqueue, queue_size
from tools import (
    has_pending_permission,
    get_pending_permission,
    resolve_pending_permission,
)
import time
import os
import re
import shutil

# ── Catppuccin-inspired prompt_toolkit style ──────────────────────────
style = Style.from_dict({
    'rule':         '#585b70',
    'sep':          'bold #7f849c',
    'label':        'bold #cba6f7',
    'value':        '#cdd6f4',
    'arrow':        'bold #cba6f7',
    # queue
    'queue-arrow':  'bold #f9e2af',
    'queued':       '#a6e3a1',
    'queue-tag':    'bold #a6e3a1',
    # thinking phase
    'spinner':      'bold #f9e2af',
    'hint':         '#585b70',
    # reasoning block
    'think-label':  'bold #74c7ec',
    'think-border': '#45475a',
    'think-text':   '#a6adc8',
    'think-dim':    'italic #585b70',
})


class AtPathCompleter(Completer):
    def get_completions(self, document, complete_event):
        match = re.search(r"(^|\s)@([^\s@]*)$", document.text_before_cursor)
        if not match:
            return

        fragment = match.group(2)
        expanded = os.path.expanduser(fragment)
        parent = os.path.dirname(expanded) or "."
        prefix = os.path.basename(expanded)

        try:
            names = os.listdir(parent)
        except OSError:
            return

        for name in sorted(names, key=lambda item: (not os.path.isdir(os.path.join(parent, item)), item.lower())):
            if not name.startswith(prefix):
                continue

            candidate = os.path.join(parent, name)
            completed = os.path.join(os.path.dirname(fragment), name) if os.path.dirname(fragment) else name
            if os.path.isdir(candidate):
                completed += "/"

            yield Completion(
                completed,
                start_position=-len(fragment),
                display=completed,
                display_meta="dir" if os.path.isdir(candidate) else "file",
            )


ses = PromptSession(style=style, completer=AtPathCompleter())
c = Console()

# ══════════════════════════════════════════════════════════════════════
#  UI styling & layout functions
# ══════════════════════════════════════════════════════════════════════
def cp(*args, **kwargs):
    c.print(*args, **kwargs)

def pnl(*args, **kwargs):
    p = config("panel")
    kwargs.setdefault("border_style", p)
    cp(Panel(*args, **kwargs))

def rule(*args, **kwargs):
    processed = (Text.from_markup(a) if isinstance(a, str) else a for a in args)
    cp(Rule(*processed, **kwargs))

def config(var):
    return ui.get(var, "")

def _width():
    return shutil.get_terminal_size().columns

def _rule_ptk(parts=None):
    """Print a horizontal rule with prompt_toolkit, optionally with inline status text."""
    w = _width()
    if parts:
        visible = sum(len(txt) for _, txt in parts)
        fill = max(0, w - visible - 1)
        line = list(parts) + [('class:rule', '─' * fill)]
    else:
        line = [('class:rule', '─' * w)]
    print_formatted_text(FormattedText(line), style=style)

def _status_parts(model):
    """Build the formatted status tokens for the rule line."""
    cwd = os.path.basename(os.getcwd()) or os.getcwd()
    return [
        ('class:rule',  '─ '),
        ('class:label', 'Iris'),
        ('class:sep',   ' │ '),
        ('class:label', 'MODEL: '),
        ('class:value', str(model)),
        ('class:sep',   ' │ '),
        ('class:label', 'CWD: '),
        ('class:value', cwd),
        ('class:rule',  ' '),
    ]

# ══════════════════════════════════════════════════════════════════════
#  Prompt & Queue Interactive Functions
# ══════════════════════════════════════════════════════════════════════
def prompt(model): 
    """Show status rule → collect input with ❯ → close with a rule."""
    print('')
    _rule_ptk(_status_parts(model))
    usr = ses.prompt([('class:arrow', ' ❯ ')]).strip()
    _rule_ptk()
    return usr


def _permission_preview(text, limit=240):
    text = text.replace("\t", "    ")
    if len(text) <= limit:
        return text
    return text[:limit] + "\n...[truncated]"


def _handle_permission_prompt():
    req = get_pending_permission()
    if not req:
        return

    path = req["path"]
    content = req["content"]
    action = "overwrite" if os.path.exists(os.path.expanduser(path)) else "create"

    print_formatted_text(FormattedText([
        ('class:label', f' write permission required '),
    ]), style=style)
    print_formatted_text(FormattedText([
        ('class:value', f' {action}: {path}\n'),
        ('class:hint', f' size: {len(content)} chars\n'),
        ('class:hint', ' preview:\n'),
        ('class:value', _permission_preview(content) + '\n'),
    ]), style=style)

    try:
        ans = ses.prompt([('class:arrow', ' allow write? [y/N] ')]).strip().lower()
    except (KeyboardInterrupt, EOFError):
        ans = ""

    resolve_pending_permission(ans in ("y", "yes"))

def queue(model, ai_done_event, first_chunk_received=None): # This part is done by AI (gemini 3.5 flash (high) Through Antigravity!
    """Interactive queue prompt showing dynamic thinking animation spinner."""
    import time
    from prompt_toolkit.application.current import get_app

    # Print the status line rule once
    print('')
    _rule_ptk(_status_parts(model))

    spinner_frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    spinner_index = 0

    # Define dynamic prompt function
    def get_prompt_text():
        frame = spinner_frames[spinner_index % len(spinner_frames)]
        q = queue_size()
        
        parts = [
            ('class:spinner', f' {frame} '),
        ]
        if q > 0:
            parts.append(('class:queued', f'({q} queued) '))
        parts.append(('class:arrow', '❯ '))
        return FormattedText(parts)

    # Define inputhook to update spinner frame and check for AI completion or first token arrival
    def my_inputhook(context):
        nonlocal spinner_index
        while not context.input_is_ready():
            if has_pending_permission():
                try:
                    app = get_app()
                    if app.is_running:
                        app.exit(result="__PERMISSION__")
                except Exception:
                    pass
                break

            if ai_done_event.is_set() or (first_chunk_received and first_chunk_received.is_set()):
                try:
                    app = get_app()
                    if app.is_running:
                        app.exit(result="__AI_DONE__")
                except Exception:
                    pass
                break
                
            spinner_index += 1
            try:
                app = get_app()
                if app.is_running:
                    app.invalidate()
            except Exception:
                pass
            time.sleep(0.08)

    # Prompt user until AI completes or sends the first token
    while not ai_done_event.is_set() and not (first_chunk_received and first_chunk_received.is_set()):
        try:
            res = ses.prompt(get_prompt_text, inputhook=my_inputhook)
            if res == "__AI_DONE__":
                break
            if res == "__PERMISSION__":
                _handle_permission_prompt()
                continue
            res = res.strip()
            if res:
                enqueue(res)
                q = queue_size()
                print_formatted_text(FormattedText([
                    ('class:queue-tag', f'  ✓ queued ({q})'),
                ]), style=style)
        except (KeyboardInterrupt, EOFError):
            break

    # Print closing rule
    _rule_ptk()

def show_queued_input(text, model): # This part is done by AI (gemini 3.5 flash (high) Through Antigravity!
    """Display a queued message as if the user typed it."""
    print('')
    _rule_ptk(_status_parts(model))
    print_formatted_text(FormattedText([
        ('class:arrow', ' ❯ '),
        ('class:value', text),
        ('class:queue-tag', '  ⊕ from queue'),
    ]), style=style)
    _rule_ptk()

# ══════════════════════════════════════════════════════════════════════
#  Reasoning / Thinking Renderer
# ══════════════════════════════════════════════════════════════════════
def render_thinking(text):
    """Display AI reasoning in a styled block with borders."""
    w = _width()

    if not text:
        print_formatted_text(FormattedText([
            ('class:think-dim', '  ◇ no reasoning returned'),
        ]), style=style)
        print()
        return

    # ── header ────────────────────────────────────────────────────
    header = ' reasoning '
    fill = max(0, w - len(header) - 4)
    print_formatted_text(FormattedText([
        ('class:think-label', '  ◆'),
        ('class:think-label', header),
        ('class:think-border', '─' * fill),
    ]), style=style)

    # ── content ───────────────────────────────────────────────────
    lines = text.strip().split('\n')
    for line in lines:
        print_formatted_text(FormattedText([
            ('class:think-border', '  │ '),
            ('class:think-text', line),
        ]), style=style)

    # ── footer ────────────────────────────────────────────────────
    print_formatted_text(FormattedText([
        ('class:think-border', '  ╰'),
        ('class:think-border', '─' * max(0, w - 4)),
    ]), style=style)
    print()

def end():
    print("")
    rule(style="white")
    pnl("BYE")
    time.sleep(0.5)
    c.clear()

def main_panel():
    cwd = os.path.basename(os.getcwd()) or os.getcwd()
    left = logo()

    right = Text()
    right.append("\n")
    right.append('\n')
    right.append("Iris by SannS")
    right.append("\n")
    right.append(f"model: {F.get('MODEL')}\n", style="dim")
    right.append(f"cwd: {cwd}\n", style="dim")

    grid = Table.grid(expand=True)
    grid.add_column(width=40)
    grid.add_column(width=1)
    grid.add_column(ratio=1)

    grid.add_row(
        left,
        Text(""),
        right
    )

    pnl(grid, title="[white]アイリス[/]", title_align="left")

if __name__ == "__main__":
    prompt("hiiii")
