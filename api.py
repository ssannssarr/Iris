import requests as rq 
import json
import os
from rich.console import Console
from rich.live import Live 
from rich.markdown import Markdown as md

console = Console()

def key():
	API_KEY = os.getenv('OPENROUTER_API_KEY')
	if not API_KEY:
		console.print('''
		[red]ERORR[/][#ffd3e9b]:OPENROUTER_API_KEY Not Found In Envioroment![/]
		[yellow]hint: export OPENROUTER_API_KEY="<your-key-here>"[/]
		[yellow]hint: get API key from https://openrouter.ai[/]
		''')
	return API_KEY

def api(chat_history: list) -> Generator[str,None,None]:
	url = 'https://openrouter.ai/api/v1/chat/completions'
	headers = {
		'Authorization': f'Bearer {key()}',
		'Content-Type':'application/json'
	}

	payload = {
		'model':"openai/gpt-oss-120b:free",
		'messages':chat_history,
		'stream':True,
		'tools':[
			{"type": "openrouter:web_search"}
		]
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
		console.print(response.text,	'\n',response.status_code)

chat = []

def add(role,content):
	chat.append(
		{
				'role':role,
				'content':content
		}
	)


def main():
	try:
		while True:
			usr_in = input(': ').strip()
			if not usr_in:
				continue
			add(role='user',content=usr_in)
			full = ''
			with Live(md(full),refresh_per_second=12,console=console) as live:
				for token in api(chat):
					full += token
					live.update(md(full))
				add('assistant',full)
	except KeyboardInterrupt:
		console.print('BYE!!')


if __name__ == '__main__':
	main()

