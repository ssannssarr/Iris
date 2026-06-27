from rich.console import Console
from rich.live import Live 
from rich.markdown import Markdown as md
from SDK import api

console = Console()
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
