from rich.text import Text


f= """
             ~~~~      ∿≋≋∼
              ∼∼∼∼    ⌇~~∿
               ≋∿∿∿  ≋∼⌇⌇
                ~◦· ···
       ~⌇∼≋≋∿~~∘◦✿✿✿✿✿?≋∼∼⌇~∿≋∼
         ≋≋∿~⌇∼≋∿✿✿✿✿✿?○○⌇~∿∿≋∼⌇~
                ∘◦· ··⌇
              ⌇∼∼≋  ∿∿∿∿
             ∿~⌇⌇    ∼∼∼∼
            ≋≋∿∿      ⌇~~~
"""

COLOR_MAP = {
    "~": "#581c87",
    "∿": "#6b21a8",
    "≋": "#7e22ce",
    "∼": "#9333ea",
    "⌇": "#a855f7",

    "◦": "#c084fc",
    "∘": "#d8b4fe",
    "○": "#e9d5ff",
    "·": "#c4b5fd",

    "✿": "#f5e8ff",
    "?": "#f5e8ff",
    " ": None,
}


def paint_flower(FLOWER):
    txt = Text()

    for ch in FLOWER:
        if ch == "\n":
            txt.append("\n")
        else:
            color = COLOR_MAP.get(ch, "#ffffff")
            txt.append(ch, style=color)

    return txt

def logo():
   return(paint_flower(f))
