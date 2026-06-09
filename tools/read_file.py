from pathlib import Path

MAX_CHARS = 12000


def read_file(path):
    p = Path(path).expanduser()

    if not p.exists():
        return f"The file {path} does not exist."

    if not p.is_file():
        return f"The path {path} is not a file."

    try:
        text = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"The file {path} is a binary or non-text file."

    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n...[truncated]"

    return f'<file path="{path}">\n{text}\n</file>'
