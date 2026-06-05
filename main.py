from ui.rui import cp,pnl,main_panel,prompt,c,reply,think,end
import time
c.clear()

main_panel()

usr_in=""
try:
    while True:
        usr_in = prompt("openai/Iris")
        if usr_in != "/exit":
            think(f"you typed {usr_in}")
            time.sleep(3)
            reply("iris","* hiii")
        else:
            break
except KeyboardInterrupt:
    end()
