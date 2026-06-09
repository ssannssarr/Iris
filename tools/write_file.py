from pathlib import Path
from .permission import request_write_permission


def write_file(path, content):
    p = Path(path).expanduser()

    if p.exists() and not p.is_file():
        return f"The path {path} is not a file."

    if not request_write_permission(path, content):
        return f'Write cancelled for "{path}".'

    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

    return f'Wrote {len(content)} characters to "{path}".'
