from ui.rui import main_panel,prompt,c,reply,think,end
from ui.msg_state import to_api
import time
from sv1 import ask_ai,thinking,response,F
from ui.msg_state import add,out,render

c.clear()
model = F.get("MODEL")
main_panel()
usr_in=""
try:
    while True:
        usr_in = prompt(model)
        if not usr_in:
            continue
        if usr_in == "/exit":
            end()
            break
        add('user',usr_in)
        data = ask_ai(messages=to_api())

        if "error" in data:
            reply(model="error",content=data["error"])
            continue
        res = response(data=data)
        add('assistant',res)
        r = out()
        c.clear()
        main_panel()
        render(r,model=model)
except (KeyboardInterrupt,EOFError):
    end()
