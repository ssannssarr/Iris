import os 
from pathlib import Path
from SDK import api
import json
import subprocess as sp


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


def run_shell_command(cmd):
    sensitive_cmd=('rm','rm -rf','rmv')
    if not cmd in sensitive_cmd:
        result = sp.run(cmd,capture_output=True,shell=True,text=True)
        if result.returncode != 0:
            return result.stderr 

        return result.stdout
    else:
        return 'This commands are restricted by devloper!'

def mention_handler(prompt: str):
    prompt_list = prompt.split()
    if prompt_list[0].startswith('!'):
        cmd = prompt.removeprefix('!').strip()
        print(run_shell_command(cmd))
        return True

    return False



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




TOOL_MAPPING = {
    'read_file': read_file,
    'run_shell_command': run_shell_command
}


TOOL_REGISTRY = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specified file. If the file exceeds 4000 characters, it returns only the first 4000 characters with a truncation note.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name or relative/absolute path of the file to read."
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        'type':'function',
        'function':{
            'name':'run_shell_command',
            'description':'runs shell commands and return stdout and stderr if any.',
            'parameters':{
                'type':'object',
                'properties':{
                    'cmd':{
                        'type':'string',
                        'description':'The command that has to be ran in the shel.',
                    }
                },
                'required':['cmd']
            }
        }
    }
]

def run_tool_loop(chat_history):
    """
    The Agentic Loop:
    1. Sends history + tools to API.
    2. If tool_calls are returned, executes them locally and appends results.
    3. Loops until the model returns a normal text response.
    """
    while True:
        response = api(chat_history, tools=TOOL_REGISTRY)
        if not response:
            return "Error: API request failed."
            
        message = response['choices'][0]['message']
        
        # Check if the model wants to use a tool
        if message.get('tool_calls'):
            # 1. Append the assistant's tool call request to history
            chat_history.append(message)
            
            # 2. Execute each tool call locally
            for tool_call in message['tool_calls']:
                func_name = tool_call['function']['name']
                func_args = json.loads(tool_call['function']['arguments'])
                
                print(f"""
-> Calling tool:
    L {func_name}""")
                
                # Execute the mapped function
                if func_name in TOOL_MAPPING:
                    try:
                        result = TOOL_MAPPING[func_name](**func_args)
                    except Exception as e:
                        result = f'Error executing tool: {str(e)}'
                else:
                    result = "Error: Tool not found"
                    
                # 3. Append tool result back to history
                chat_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call['id'],
                    "content": str(result)
                })
        else:
            # No tool calls! The model gave a final text response.
            # Append it to history and break the loop.
            chat_history.append(message)
            return message.get('content', '')
