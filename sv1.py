import requests as rq
import os
import json
import sys

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
    sys.exit(1)





def ask_ai(messages):
    headers = {
        "Authorization": f"Bearer {F['KEY']}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": F["MODEL"],
        "messages":messages,
    }

    try:
        res = rq.post(url=F['URL'], headers=headers, json=payload)
        res.raise_for_status()
        data = res.json()
        msg = data["choices"][0]["message"]
        return msg
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


