from rich.table import Table
from rich.text import Text
from logo import logo
from ui.rui import pnl

def main_panel():
    left = logo()

    right = Text()
    right.append("アイリス\n", style="bold #c084fc")
    right.append("model  gpt-oss\n", style="dim")
    right.append("mode   chat\n", style="dim")
    right.append("cwd    ~/Iris\n", style="dim")

    grid = Table.grid(expand=True)
    grid.add_column(width=40)
    grid.add_column(width=1)
    grid.add_column(ratio=1)

    grid.add_row(
        left,
        Text("│", style="bright_magenta"),
        right
    )

    pnl(grid, title="アイリス")

if __name__ == "__main__":
   main_panel()
