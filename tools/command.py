import shlex
import subprocess

ALLOWED = {"rg", "jq", "grep", "sed"}
MAX_OUTPUT = 12000
TIMEOUT_SECONDS = 8


def run_command(command):
    parts = shlex.split(command)
    if not parts:
        return "Empty command."

    if parts[0] not in ALLOWED:
        allowed = ", ".join(sorted(ALLOWED))
        return f'Command "{parts[0]}" is not allowed. Allowed: {allowed}.'

    try:
        res = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=TIMEOUT_SECONDS,
        )
    except FileNotFoundError:
        return f'Command "{parts[0]}" is not installed.'
    except subprocess.TimeoutExpired:
        return f'Command timed out after {TIMEOUT_SECONDS} seconds: {command}'

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

    if len(text) > MAX_OUTPUT:
        text = text[:MAX_OUTPUT] + "\n...[truncated]"

    return text
