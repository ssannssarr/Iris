from ui.rui import cp,pnl,main_panel,prompt,c,reply,think

c.clear()

main_panel()

usr_in=""
while True:
    usr_in = prompt("openai/Iris")
    if usr_in != "/exit":
        continue
    else:
        think(f"you typed {usr_in}")
        reply("* hiii")