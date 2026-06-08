from rich.markdown import Markdown as md
from ui.rui import cp,rule
from prompts import SYSTEM_PROMPT
messages = []

def add(role,content):
    messages.append({
        "role":role,
        "text":content
        })

def out():
    return messages

from ui.rui import cp,rule,render_thinking

def render(msg,model):
    for m in msg:
        role = m['role']
        text = m['text']

        if role == 'user':
            print()
            cp(f"[on black white]❯ {text} [/]")
        else:
            if 'reasoning' in m and m['reasoning']:
                render_thinking(m['reasoning'])
            safe_text = text.replace("\n", "\n  ")
            cp(md(f"* {safe_text}"))
def to_api():
    api = [
        {
         "role":"system",
         "content":SYSTEM_PROMPT
        }
    ]

    for m in messages:
        if m['role'] in ('user','assistant'):
            api.append({
                "role":m['role'],
                "content":m['text']
                })
    return api
