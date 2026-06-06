from prompt_toolkit import PromptSession

s = PromptSession()


while True:
    text = s.prompt("> ", bottom_toolbar="? shortcuts")
    if text == "/exit":
        break
    print(f"You typed {text}")
