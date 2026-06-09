messages = []


def add(role, content):
    messages.append({"role": role, "text": content})


def out():
    return messages
