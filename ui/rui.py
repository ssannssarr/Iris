from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from ui.config import cdui
from rich.markdown import Markdown as md
import os
import json

c = Console()
def cp(*args, **kwargs):
    c.print(*args, **kwargs)

def pnl(*args, **kwargs):
    p = config("panel")
    kwargs.setdefault("border_style",p)
    cp(Panel(*args,**kwargs))

def rule(*args, **kwargs):
    cp(Rule(*args, **kwargs))

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
    usr = input("❯ ").strip()
    rule(style="white")
    return usr

def statusline(model):
    cwd = os.path.basename(os.getcwd()) or os.getcwd()
    model = model
    status = f"─ [bold]Iris[/] | MODEL: {model} | CWD: {cwd}"
    return status


def end():
    print("")
    rule(style="white")
    pnl("BYE")

def think(*args, **kwargs):
   rule("[cyan]───[/] [white]thinking...[/]", align="left", style="cyan")
   cp(md(*args, **kwargs))

def res(model,content):
   rule(f"[cyan]───[/] {model} [white][/]", align="left", style="cyan")
   cp(md(content))

if __name__ == "__main__":
    prompt("openai/Iris")
