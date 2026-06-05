import requests as rq
import os
import json

with open('.settings.json','r') as f:
        data = json.load(f)

api_key = os.environ.get('OPENROUTER_API_KEY')
model = data.get('MODEL')
url = data.get('BASE_URL')
F = {
    "MODEL":model,
    "KEY":api_key,
    "URL":url
}





def ask_ai(usr):
    
    headers = {
        "Authorization": f"Bearer {F.get('KEY')}",
        "Content-Type": "application/json"
    }
        
    payload = {
        "model": f"{F.get('MODEL')}",
        "messages": [{"role": "user","content": usr}]
    }

    resp = rq.post(url, headers=headers, json=payload)
    data = resp.json()
    return data

def thinking(data):
    message = data["choices"][0]["message"]
    thnk = message.get("reasoning")
    return thnk

def response(data):
    message = data["choices"][0]["message"]
    msg = message.get("content")
    return msg




