import os
import json

messages = []


def add(role, content):
    messages.append({"role": role, "text": content})


def out():
    return messages

def save_msg(messages):
    with open(".iris.json", "w") as m:
        json.dump(messages,m,indent=4)