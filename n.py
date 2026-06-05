from rich import print
from ui.rui import pnl,cp
from rich.columns import Columns
from rich.panel import Panel


l = Panel("jsyyy")
r = Panel("tryyyy")

cp(Columns([l,r],equal=True,expand=True))

pnl("hiii", title="[bold white]アイリス™[/]", title_align="left")
