from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.markdown import Markdown as md
from rich.table import Table
from rich.text import Text
from rich.markup import escape
from ui.logo import logo
import os
import json
try:
    from ui.config import cdui
except ModuleNotFoundError:
    from config import cdui

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
    try:
        with open('.ui.json' , 'r') as df:
            ui_data = json.load(df)
        p = f'{ui_data.get(var)}'
        return f"{p}"
    except FileNotFoundError:
        cdui()


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
    status = f"[{pr}]─[/] [{st}]Iris[/][{pr}]|[/][{st}]MODEL: {model}[/][{pr}]|[/][{st}]CWD: {cwd}[/]"
    return status


def end():
    print("")
    rule(style="white")
    pnl("BYE")

def think(*args, **kwargs):
   rule("[cyan]───[/] [white]thinking...[/]", align="left", style="cyan")
   cp(md(*args, **kwargs))

def reply(model,content):
   rule(f"[cyan]───[/] {model} [white][/]", align="left", style="cyan")
   cp(md(content))

def main_panel():
    left = logo()

    right = Text()
    right.append("")
    right.append("model  gpt-oss\n", style="dim")
    right.append("mode   chat\n", style="dim")
    right.append("cwd    ~/Iris\n", style="dim")

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
