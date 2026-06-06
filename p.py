from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings

kb = KeyBindings()
buf = Buffer(multiline=True)

line = "─" * 80

@kb.add("enter")
def _(event):
    event.app.exit(result=buf.text)

@kb.add("c-c")
def _(event):
    event.app.exit(result=None)

root = HSplit([
    Window(FormattedTextControl(line), height=1),
    Window(BufferControl(buffer=buf), height=3),
    Window(FormattedTextControl(line), height=1),
    Window(FormattedTextControl("? for shortcuts"), height=1),
])

app = Application(
    layout=Layout(root, focused_element=buf),
    key_bindings=kb,
    full_screen=False,
)

text = app.run()

print("\nYou typed:")
print(text)
