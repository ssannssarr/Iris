import requests as rq
import os
import json
import sys

api_key = os.environ.get('OPENROUTER_API_KEY')
model = os.environ.get('IRIS_MODEL')
url = os.environ.get('IRIS_BASE_URL')

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
        "stream": True,
        "messages":messages,
    }
    full_text = ""
    reasoning_text = ""

    try:
        with rq.post(
            F["URL"],
            headers=headers,
            json=payload,
            stream=True,
            timeout=60
        ) as r:
            r.raise_for_status()

            for line in r.iter_lines():
                if not line:
                    continue

                line = line.decode("utf-8")

                if not line.startswith("data: "):
                    continue

                chunk = line[6:]

                if chunk == "[DONE]":
                    break

                data = json.loads(chunk)
                delta = data["choices"][0].get("delta", {})

                reasoning = delta.get("reasoning", "")
                if reasoning:
                    reasoning_text += reasoning

                text = delta.get("content", "")
                if text:
                    full_text += text

        return {
            "content": full_text,
            "reasoning": reasoning_text,
        }

    except rq.exceptions.Timeout:
        return {"error": "Request Timeout"}
    except rq.exceptions.HTTPError as e:
        return {"error": f"HTTPError: {e}"}
    except rq.exceptions.RequestException as e:
        return {"error": f"Network Error: {e}"}

def thinking(data):
    return data.get("reasoning") or ""

def response(data):
    return data.get("content") or ""

