import requests as rq
import os
import json
import sys
from tools import TOOLS, run_tool_call

MAX_TOOL_STEPS = 8

def _load_settings():
    try:
        with open('.settings.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

_settings = _load_settings()

api_key = os.environ.get('OPENROUTER_API_KEY') or _settings.get('API_KEY')
model = os.environ.get('IRIS_MODEL') or _settings.get('MODEL')
url = os.environ.get('IRIS_BASE_URL') or _settings.get('BASE_URL')

F = {
    "MODEL":model,
    "KEY":api_key,
    "URL":url
}

try:
    if not F.get("KEY"):
        raise RuntimeError('OPENROUTER_API_KEY not found')
    elif not F.get("MODEL"):
        raise RuntimeError('IRIS_MODEL not found!!')
    elif not F.get("URL"):
        raise RuntimeError('IRIS_BASE_URL not found!!')
except RuntimeError as e:
    print(f"[ERROR]: {type(e).__name__}: {e}")





def ask_ai(messages):
    headers = {
        "Authorization": f"Bearer {F['KEY']}",
        "Content-Type": "application/json",
    }

    convo = list(messages)

    try:
        for _ in range(MAX_TOOL_STEPS):
            payload = {
                "model": F["MODEL"],
                "messages": convo,
                "tools": TOOLS,
            }
            res = rq.post(url=F['URL'], headers=headers, json=payload)
            res.raise_for_status()
            data = res.json()
            msg = data["choices"][0]["message"]
            tool_calls = msg.get("tool_calls") or []

            if not tool_calls:
                if not (msg.get("content") or "").strip():
                    msg["content"] = "I finished the tool calls but the model returned no final text."
                return msg

            convo.append(
                {
                    "role": "assistant",
                    "content": msg.get("content") or "",
                    "tool_calls": tool_calls,
                }
            )

            for tool_call in tool_calls:
                convo.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": tool_call["function"]["name"],
                        "content": run_tool_call(tool_call),
                    }
                )

        return {"error": f"Tool loop exceeded {MAX_TOOL_STEPS} steps"}
    except rq.exceptions.Timeout:
        return {"error": "Request Timeout"}
    except rq.exceptions.HTTPError as e:
        return {"error": f"HTTPError: {e}"}
    except rq.exceptions.RequestException as e:
        return {"error": f"Network Error: {e}"}
    except (KeyError, IndexError, TypeError):
        return {"error": "Unexpected API response"}
    except ValueError:
        return {"error": "Invalid JSON in API response"}

def ask_ai_stream(messages):
    headers = {
        "Authorization": f"Bearer {F['KEY']}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": F["MODEL"],
        "messages": messages,
        "stream": True,
    }

    try:
        res = rq.post(url=F['URL'], headers=headers, json=payload, stream=True)
        res.raise_for_status()
        for line in res.iter_lines():
            if not line:
                continue
            line_str = line.decode('utf-8').strip()
            if line_str.startswith("data: "):
                data_str = line_str[6:]
                if data_str == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    delta = chunk["choices"][0]["delta"]
                    yield {
                        "content": delta.get("content") or "",
                        "reasoning": delta.get("reasoning") or delta.get("reasoning_content") or ""
                    }
                except (KeyError, IndexError, ValueError):
                    continue
    except rq.exceptions.Timeout:
        yield {"error": "Request Timeout"}
    except rq.exceptions.HTTPError as e:
        yield {"error": f"HTTPError: {e}"}
    except rq.exceptions.RequestException as e:
        yield {"error": f"Network Error: {e}"}

def thinking(data):
    return data.get("reasoning") or ""

def response(data):
    return data.get("content") or ""
