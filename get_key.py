import os

def key():
	API_KEY = os.getenv('OPENROUTER_API_KEY')
	if not API_KEY:
		console.print('''
		[red]ERORR[/][#ffd3e9b]:OPENROUTER_API_KEY Not Found In Envioroment![/]
		[yellow]hint: export OPENROUTER_API_KEY="<your-key-here>"[/]
		[yellow]hint: get API key from https://openrouter.ai[/]
		''')
		exit()
	return API_KEY