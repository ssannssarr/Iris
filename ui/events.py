from rich.text import Text
from ui.rui import cp

KIND_STYLES = {
    "explore": ("⌕", "Exploring", "cyan"),
    "read": ("◰", "Reading", "bright_blue"),
    "edit": ("✎", "Editing", "yellow"),
    "run": ("▶", "Running", "magenta"),
    "done": ("✓", "Done", "green"),
    "error": ("✕", "Error", "red"),
    "tool": ("◆", "Tool", "#AB82FF"),
}


def say(text):
    cp(f"\n[bold #cba6f7]Iris:[/] {text}")


def event(kind, title="", detail=""):
    icon, fallback, color = KIND_STYLES.get(kind, ("•", kind.title(), "white"))
    label = title or fallback

    line = Text()
    line.append("\n")
    line.append(f"{icon} ", style=f"bold {color}")
    line.append(label, style=f"bold {color}")
    cp(line)

    if detail:
        cp(f"  [#FFDAB9]⎿ {detail}[/]")


def render_diff(diff_text):
    if not diff_text:
        return

    for line in diff_text.splitlines():
        style = None

        if line.startswith("+") and not line.startswith("+++"):
            style = "green"
        elif line.startswith("-") and not line.startswith("---"):
            style = "red"
        elif line.startswith("@@"):
            style = "cyan"
        elif line.startswith(("diff ", "index ", "---", "+++")):
            style = "dim"

        cp(f"[{style}]{line}[/]" if style else line)