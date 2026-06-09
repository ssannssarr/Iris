from rich.markdown import Markdown as md

from ui.rui import cp, render_thinking


def render(messages, model):
    for message in messages:
        role = message["role"]
        text = message["text"]

        if role == "user":
            print()
            cp(f"[on black white]❯ {text} [/]")
            continue

        if message.get("reasoning"):
            render_thinking(message["reasoning"])

        safe_text = text.replace("\n", "\n  ")
        cp(md(f"* {safe_text}"))
