import requests as rq
import os
import json
import requests as rq

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

headers = {
    "Authorization": f"Bearer {F.get('KEY')}",
    "Content-Type": "application/json"
}


payload = payload = {
    "model": f"{F.get('MODEL')}",
    "messages": [{"role": "user","content": usr_in}]
}

resp = rq.post(url, headers=headers, json=payload)
data = resp.json()
message = data["choices"][0]["message"]

msg = message.get("content")
thnk = message.get("reasoning")


think(thnk)
res(model=F.get("MODEL"), content=msg)
