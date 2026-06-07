from rich.markdown import Markdown as md
from ui.rui import cp
msg = []

def add(role,content):
    msg.append({
        "role":role,
        "text":content
        })

def out():
    return msg

def render(msg):
    for m in msg:
        title='❯' if m['role'] == 'user' else ''
        r = m['text']
        cp(md(title,r))
