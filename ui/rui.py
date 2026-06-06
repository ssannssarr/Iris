from rich.markdown import Markdown as md
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.text import Text
from ui.logo import logo
from ui.ui import ui
from sv1 import F
import time
import os

c = Console()
def cp(*args, **kwargs):
    c.print(*args, **kwargs)

def pnl(*args, **kwargs):
    p = config("panel")
    kwargs.setdefault("border_style",p)
    cp(Panel(*args,**kwargs))

def rule(*args, **kwargs):
    processed = (Text.from_markup(a) if isinstance(a, str) else a for a in args)
    cp(Rule(*processed, **kwargs))

def config(var):
    return ui.get(var, "")


def prompt(s):
    print('')
    pr = config('prompt')
    s = statusline(s)
    rule(s, style=f"{pr}" , align="left")
    usr = input(" ❯ ").strip()
    rule(style=f"{pr}")
    return usr

def statusline(model):
    cwd = os.path.basename(os.getcwd()) or os.getcwd()
    model = model
    pr = config('prompt')
    st = config('statusline')
    status = f"[{pr}]─[/] [{st}]Iris[/] [{pr}]|[/] [{st}]MODEL: {model}[/] [{pr}]|[/] [{st}]CWD: {cwd}[/]"
    return status


def end():
    print("")
    rule(style="white")
    pnl("BYE")
    time.sleep(0.5)
    c.clear()

def think(*args, **kwargs):
   rule("[cyan]───[/] [white]thinking...[/]", align="left", style="cyan")
   if args and args[0]:
      cp(md(*args, **kwargs))
   else:
      cp("[dim]No reasoning returned.[/dim]")
   print("\n")

def reply(model,content):
   rule(f"[cyan]───[/] {model} [white][/]", align="left", style="cyan")
   cp(md(content or ""))
   print("\n")

def main_panel():
    cwd = os.path.basename(os.getcwd()) or os.getcwd()
    left = logo()

    right = Text()
    right.append("\n")
    right.append('\n')
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
