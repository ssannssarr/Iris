from llm import ask_ai, response, thinking, F
from api_format import to_api
from state import add,messages,save_msg
from rich.markdown import Markdown as md
from ui import cp,c, _status_parts, _rule_ptk,AtPathCompleter,reply
from ui.events import event, say
from prompt_toolkit import PromptSession


ses = PromptSession(completer=AtPathCompleter())


usr_in = ""
c.clear()
_rule_ptk(_status_parts(model=F.get("MODEL")))

print()


try:
    while True:
        usr_in = ses.prompt([('class:arrow', ' ❯ ')]).strip()

        if usr_in.lower().strp() == "/exit":
            cp("[#FFDAB9]✦ BYE~~[/]")
            save_msg(messages)
            break
            

        if not usr_in:
        	continue

        
        add(role="user",content=usr_in)

        with c.status("[bold blink #AB82FF]✦ Iris thinking...[/]", 
                       spinner="dots", spinner_style="#AB82FF"
                    ):
        		data = ask_ai(to_api())

        res = response(data=data)
        thnk = thinking(data=data)
        add(role="assistant", content=res)

        reply(res=res)

except (EOFError, KeyboardInterrupt):
    c.clear()
    cp("[#FFDAB9]✦ BYE~~[/]")
    save_msg(messages)
