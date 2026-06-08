import json
import os

_default_ui = {
    "panel": "bright_magenta",
    "prompt": "white",
    "statusline": "bold violet",
}

def _load_ui():
    try:
        with open(".ui.json", "r") as f:
            loaded = json.load(f)
            merged = dict(_default_ui)
            merged.update(loaded)
            return merged
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(_default_ui)

ui = _load_ui()
