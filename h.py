from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.console import Console

console = Console()

def start_panel():
    grid = Table.grid(padding=(0, 2))
    grid.add_column(style="bold violet")
    grid.add_column(style="white")

    grid.add_row("model", "openai/gpt-oss-120b:free")
    grid.add_row("mode", "chat")
    grid.add_row("project", "~/Iris")
    grid.add_row("", "")
    grid.add_row("/ask", "ask anything")
    grid.add_row("/fix", "fix code")
    grid.add_row("/explain", "explain file")
    grid.add_row("/theme", "change look")

    panel = Panel(
        Align.center(grid),
        title="[bold]アイリス[/bold]",
        subtitle="[dim]ready[/dim]",
        border_style="bright_magenta",
        padding=(1, 4),
    )

    console.print(panel)

start_panel()
