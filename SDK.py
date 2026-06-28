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
		'stream':True,
		'tools':TOOL

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




def api_with_tools(chat_history: list, tools: list = None):
    """Non-streaming API call specifically for handling tool execution."""
    url = 'https://openrouter.ai/api/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {key()}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'openrouter/free', # Better tool support
        'messages': chat_history,
        'stream': False # Crucial for parsing tool calls easily
    }
    
    if tools:
        payload['tools'] = tools

    response = rq.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text, '\n', response.status_code)
        return None

