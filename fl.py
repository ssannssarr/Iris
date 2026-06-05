"""
Iris CLI startup panel — flower left, text right, equal height.
python iris_logo.py

Import:
    from iris_logo import print_logo
    print_logo()
"""
import math, sys
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table

console = Console()

W, H = 38,19
CX, CY = W / 2.0, H / 2.0
ASPECT = 2.05

def _p(col, row):
    dx = (col - CX) / ASPECT
    dy = row - CY
    return math.hypot(dx, dy), math.atan2(dy, dx)

def _outer(c, r): 
    d, t = _p(c, r)
    return d <= 5.5 * (abs(math.cos(3*t)) + 0.12*math.sin(6*t+0.5))

def _inner(c, r):
    d, t = _p(c, r)
    return d <= 2.7 * (abs(math.cos(3*t)) + 0.08*math.sin(6*t))

def _core(c, r):
    d, _ = _p(c, r)
    return d <= 1.1

def _c(r, g, b): return f"rgb({r},{g},{b})"

def _pcol(dist):
    t = min(dist / 6.0, 1.0)
    s = (t*2) if t < 0.5 else 1.0
    if t < 0.5:
        return _c(int(88+(147-88)*s), int(28+(51-28)*s), int(135+(234-135)*s))
    s = (t-0.5)*2
    return _c(int(147+(196-147)*s), int(51+(148-51)*s), 234)

def _icol(dist):
    t = 1 - min(dist/3.0, 1.0)
    return _c(int(216+24*t), int(180+40*t), 254)

OUTER = "~∿≋∼⌇"
INNER = "◦∘○·"

def build_flower() -> Text:
    out = Text()
    for row in range(H):
        for col in range(W):
            d, theta = _p(col, row)
            if _core(col, row):
                out.append("✿", style=_c(240, 220, 255))
            elif _inner(col, row):
                out.append(INNER[int(d*1.3+abs(theta)) % 4], style=_icol(d))
            elif _outer(col, row):
                out.append(OUTER[int(d*1.7+theta*1.5) % 5], style=_pcol(d))
            else:
                out.append(" ")
        if row < H - 1:
            out.append("\n")
    return out

# ── PUBLIC ────────────────────────────────────────────────
def print_logo():
    BORDER = _c(88, 28, 135)
    DIM    = _c(80, 40, 110)
    ACC    = _c(196, 148, 232)

    # flower renderable
    flower = build_flower()

    # right-side placeholder — edit this block
    rtext = Text(justify="left")
    rtext.append("アイリス  ", style=ACC)
    rtext.append("v0.1.0\n", style=DIM)
    rtext.append("─" * 20 + "\n\n", style=DIM)
    rtext.append("› ", style=ACC); rtext.append("placeholder line\n", style=DIM)
    rtext.append("› ", style=ACC); rtext.append("placeholder line\n", style=DIM)
    rtext.append("› ", style=ACC); rtext.append("placeholder line\n\n", style=DIM)
    rtext.append("ready\n", style=DIM)

    left  = Panel(flower, border_style=BORDER, padding=(0, 1), expand=False)
    right = Panel(rtext,  border_style=BORDER, padding=(1, 2), expand=True,
                  height=H + 2)   # match panel height (content + top/bot border)

    grid = Table.grid(padding=0, expand=True)
    grid.add_column(no_wrap=True)
    grid.add_column(ratio=1)
    grid.add_row(left, right)

    console.print(grid)

if __name__ == "__main__":
    build_flower()
