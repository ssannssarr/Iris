import json

DEFAULT_THEME = {
    "panel": "bright_magenta",
    "prompt": "white",
    "statusline": "bold violet",
}


def _load_theme():
    try:
        with open(".ui.json", "r") as f:
            theme = dict(DEFAULT_THEME)
            theme.update(json.load(f))
            return theme
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(DEFAULT_THEME)


ui = _load_theme()
