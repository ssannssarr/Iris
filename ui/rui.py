from rich.console import Console
from rich.panel import Panel 
from rich.rule import Rule
from ui.config import cdui
import os
import json

c = Console()
def cp(*args, **kwargs):
    c.print(*args, **kwargs)

def pnl(content):
    p = config("panel")
    cp(Panel(content, border_style=f"{p}"))

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


def prompt():
    print('')
    pr = config('prompt')
    rule(cwd(), style=f"{pr}" , align="left")
    usr = input("❯ ").strip()
    rule(style="white")
    return usr

def cwd():
    cwd = f"──── {os.getcwd()}"
    return cwd


def end():
    print("")
    rule(style="white")
    pnl("BYE")


if __name__ == "__main__":
    prompt()