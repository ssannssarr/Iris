from prompts import SYSTEM_PROMPT
from state import messages
from tools import expand_mentions


def to_api():
    api = [{"role": "system", "content": SYSTEM_PROMPT}]

    for message in messages:
        if message["role"] not in ("user", "assistant"):
            continue
        api.append(
            {
                "role": message["role"],
                "content": expand_mentions(message["text"]) if message["role"] == "user" else message["text"],
            }
        )

    return api
