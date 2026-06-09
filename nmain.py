from llm import ask_ai, response, thinking, F
from api_format import to_api
from state import add
from rich.markdown import Markdown as md
from ui.rui import cp, c, _status_parts, _rule_ptk,rule



usr_in = ""
c.clear()
_rule_ptk(_status_parts(model=F.get("MODEL")))

print()
try:
	while True:
		usr_in = input("❯ ").strip()

		if usr_in.lower() == "/exit":
			cp("[#FFDAB9]✦ BYE~~[/]")

		add(role="user",content=usr_in)

		with c.status("[bold blink #AB82FF]✦ Iris thinking...[/]", spinner="dots", spinner_style="#AB82FF"):
			data = ask_ai(to_api())

		res = response(data=data)
		thnk = thinking(data=data)
		add(role="assistant", content=res)
		
		
		safe_text = res.replace("\n", "\n  ")
		rule(style="#AB82FF")
		cp(md(f"* {safe_text}"))
		print()
		rule(style="#AB82FF")
		print()

except (EOFError, KeyboardInterrupt):
	cp("[#FFDAB9]✦ BYE~~[/]")
