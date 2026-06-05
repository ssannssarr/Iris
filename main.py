from ui.rui import cp,pnl,main_panel,prompt,c,reply,think

c.clear()

main_panel()

usr_in=""
try:

while True:
    usr_in = prompt("openai/Iris")
    if usr_in != "/exit":
        think(f"you typed {usr_in}")
        reply("iris","* hiii")
    else:
        break
