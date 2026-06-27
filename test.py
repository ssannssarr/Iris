import os 
from pathlib import Path

def mention_expandiser(prompt: str):
	prompt_list = prompt.split()
	for word in prompt_list:
		if word.startswith('@'):
			filename = word.strip('@')
			if not filename:
				continue
			return filename

def read_file(filename):
	if Path(filename).exists():
		with open(filename ,'r') as file:
			file_content = file.read()
		if len(file_content) > 4000:
			return f'{file_content[:4000]}\n\nNOTE: only first 4000 chars'
		else:
			return file_content
	else:
		return 'File doesnt exist'

def read_file_line(filename:str,start_char:int,end_char:int):
	if Path(filename).exists():
		with open(filename,'r') as file:
			return file.read()[start_char:end_char]



def mention_handler(prompt: str):
	prompt_list = prompt.split()
	if prompt_list[0].startswith('!'):
		cmd = prompt.strip('!')
		os.system(cmd)



def main():
	while True:
		prompt = input(': ').strip()
		if not prompt:
			continue
		mention_handler(prompt)
		file = mention_expandiser(prompt)
		if file:
			print(read_file(file))

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\nBYE!!')