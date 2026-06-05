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





def ask_ai(usr):

    headers = {
        "Authorization": f"Bearer {F.get('KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": f"{F.get('MODEL')}",
        "messages": [{"role": "user","content": usr}]
    }
    try:
        resp = rq.post(url, headers=headers, json=payload,timeout=60)
        resp.raise_for_status()
        return resp.json
    except rq.exceptions.Timeout:
        return {"error":'Request Timeout'}
    except rq.exceptions.HTTPError as e:
        return {'error':f'HTTPError {e}'}
    except rq.exceptions.RequestException as e:
        return {'error':f'Network Error: {e}'}

def thinking(data):
    return data.get("choices",[{}])[0].get('message',{}).get('reasoning')

def response(data):
    message = data["choices"][0]["message"]
    msg = message.get("content")
    return msg




