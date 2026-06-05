from ui.rui import main_panel,prompt,c,reply,think,end
import time
from sv1 import ask_ai,thinking,response,F

c.clear()
main_panel()
model = F.get("MODEL")
usr_in=""
try:
    while True:
        usr_in = prompt(model)
        if usr_in != "/exit":
            data = ask_ai(usr=usr_in)
            thnk = thinking(data=data)
            think(thnk)
            time.sleep(1)
            res = response(data=data)
            reply(model=model,content=res)
        else:
            end()
            break
except KeyboardInterrupt:
    end()
