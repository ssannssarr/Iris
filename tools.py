import json
import os
import re
import shlex
import subprocess
import threading
from pathlib import Path

MAX_FILE_CHARS = 12000
MAX_CMD_OUTPUT = 12000
CMD_TIMEOUT_SECONDS = 8
ALLOWED_COMMANDS = {"rg", "jq", "grep", "sed"}

_permission_lock = threading.Lock()
_pending_permission = None


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
    if len(text) > MAX_FILE_CHARS:
        text = text[:MAX_FILE_CHARS] + "\n...[truncated]"
    return f'<file path="{path}">\n{text}\n</file>'


def request_write_permission(path, content):
    global _pending_permission

    req = {
        "kind": "write_file",
        "path": path,
        "content": content,
        "approved": False,
        "event": threading.Event(),
    }
    with _permission_lock:
        _pending_permission = req
    req["event"].wait()
    return req["approved"]


def has_pending_permission():
    with _permission_lock:
        return _pending_permission is not None


def get_pending_permission():
    with _permission_lock:
        return _pending_permission


def resolve_pending_permission(approved):
    global _pending_permission

    with _permission_lock:
        req = _pending_permission
        _pending_permission = None

    if req is None:
        return

    req["approved"] = approved
    req["event"].set()


def write_file(path, content):
    p = Path(path).expanduser()
    if p.exists() and not p.is_file():
        return f"The path {path} is not a file."
    if not request_write_permission(path, content):
        return f'Write cancelled for "{path}".'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f'Wrote {len(content)} characters to "{path}".'


def run_command(command):
    parts = shlex.split(command)
    if not parts:
        return "Empty command."
    if parts[0] not in ALLOWED_COMMANDS:
        allowed = ", ".join(sorted(ALLOWED_COMMANDS))
        return f'Command "{parts[0]}" is not allowed. Allowed: {allowed}.'
    try:
        res = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=CMD_TIMEOUT_SECONDS,
        )
    except FileNotFoundError:
        return f'Command "{parts[0]}" is not installed.'
    except subprocess.TimeoutExpired:
        return f"Command timed out after {CMD_TIMEOUT_SECONDS} seconds: {command}"

    out = res.stdout
    err = res.stderr
    text = f"$ {command}\n"
    if out:
        text += out
    if err:
        if out and not out.endswith("\n"):
            text += "\n"
        text += f"[stderr]\n{err}"
    if not out and not err:
        text += "(no output)"
    if len(text) > MAX_CMD_OUTPUT:
        text = text[:MAX_CMD_OUTPUT] + "\n...[truncated]"
    return text


def expand_mentions(text):
    paths = re.findall(r"@([\w./~\\-]+)", text)
    if not paths:
        return text

    chunks = [text]
    for path in paths:
        chunks.append(read_file(path))
    return "\n\n".join(chunks)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a UTF-8 text file from disk.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative or absolute file path."}
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write UTF-8 text content to a file on disk.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative or absolute file path."},
                    "content": {"type": "string", "description": "Full file content to write."},
                },
                "required": ["path", "content"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a read-only terminal command when targeted search or filtering is needed. Only rg, jq, grep, and sed are allowed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "A single rg, jq, grep, or sed command."}
                },
                "required": ["command"],
                "additionalProperties": False,
            },
        },
    },
]

TOOL_IMPLS = {
    "read_file": lambda args: read_file(args["path"]),
    "write_file": lambda args: write_file(args["path"], args["content"]),
    "run_command": lambda args: run_command(args["command"]),
}


def run_tool_call(tool_call):
    try:
        fn = tool_call["function"]
        name = fn["name"]
        args = json.loads(fn.get("arguments") or "{}")
        tool = TOOL_IMPLS.get(name)
        if tool is None:
            return f"Unknown tool: {name}"
        return tool(args)
    except Exception as e:
        return f"{type(e).__name__}: {e}"
