from rich.markdown import Markdown as md
from ui.rui import cp,rule

messages = []

def add(role,content):
    messages.append({
        "role":role,
        "text":content
        })

def out():
    return messages

def render(msg,model):
    for m in msg:
        role = m['role']
        text = m['text']

        if role == 'user':
            cp(md(f"**❯** {text}"))
            print()
        else:
            rule(f"[cyan]───[/] {model} [white][/]", align="left", style="cyan")
            cp(md(text))
        print()
