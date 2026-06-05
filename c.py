from rich.table import Table
from rich.text import Text
from logo import logo,height
from ui.rui import pnl

h = height()

def main_panel():
    left = logo()

    right = Text()
    right.append("")
    right.append("model  gpt-oss\n", style="dim")
    right.append("mode   chat\n", style="dim")
    right.append("cwd    ~/Iris\n", style="dim")

    grid = Table.grid(expand=True)
    grid.add_column(width=40)
    grid.add_column(width=1)
    grid.add_column(ratio=1)

#    divider = "\n".join(["│"] * h)
    grid.add_row(
        left,
        Text(""),
        right
    )

    pnl(grid, title="アイリス")

if __name__ == "__main__":
   main_panel()
