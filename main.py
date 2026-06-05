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
        if not usr_in:
            continue
        if usr_in == "/exit":
            end()
            break
        data = ask_ai(usr=usr_in)

        if "error" in data:
            reply(model="error",content=data["error"])
            continue
        thnk = thinking(data=data)
        think(thnk)

        time.sleep(1) # A fake delay just for now

        res = response(data=data)
        reply(model=model,content=res)

except KeyboardInterrupt:
    end()
