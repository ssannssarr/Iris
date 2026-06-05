from ui.rui import cp,pnl,rule,prompt,c
from logo import logo

def main_panel():
    c.clear()
    pnl(logo(), title="[white]アイリス[/]", title_align="left")




usr_in=""

while True:
    usr_in = prompt()
if __name__ == "__main__":
   main_panel()
