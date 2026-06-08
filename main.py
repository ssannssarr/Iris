from ui.rui import main_panel,prompt,c,reply,think,end
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
        data = ask_ai(usr=usr_in)

        if "error" in data:
            reply(model="error",content=data["error"])
            continue
        add('user',usr_in)
        res = response(data=data)
        add('Assistant',res)
        r = out()
        c.clear()
        main_panel()
        render(r,model=model)
except (KeyboardInterrupt,EOFError):
    end()
