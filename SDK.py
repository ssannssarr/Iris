import requests as rq 
import json
from get_key import key


def api(chat_history: list) -> Generator[str,None,None]:
	url = 'https://openrouter.ai/api/v1/chat/completions'
	headers = {
		'Authorization': f'Bearer {key()}',
		'Content-Type':'application/json'
	}

	payload = {
		'model':'openrouter/free',
		'messages':chat_history,
		'stream':True
	}

	response = rq.post(url,headers=headers,json=payload,stream=True)

	if response.status_code == 200:
		for line in response.iter_lines():
			if line:
				line = line.decode('utf-8')
				if line.startswith('data: ') and line != 'data: [DONE]':
					line = line[6:].strip()
					chunk = json.loads(line)
					token = chunk['choices'][0]['delta'].get('content')
					yield token
	else:
		print(response.text,'\n',response.status_code)

