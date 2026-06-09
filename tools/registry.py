import json

from .read_file import read_file
from .write_file import write_file
from .command import run_command

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a UTF-8 text file from disk.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative or absolute file path.",
                    }
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
                    "path": {
                        "type": "string",
                        "description": "Relative or absolute file path.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Full file content to write.",
                    },
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
                    "command": {
                        "type": "string",
                        "description": "A single rg, jq, grep, or sed command.",
                    }
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
