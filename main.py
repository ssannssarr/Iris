# main.py
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown as md
from tools import run_tool_loop,mention_handler
import time

console = Console()
chat = []

def add(role, content):
    chat.append({'role': role, 'content': content})

def main():
    try:
        while True:
            usr_in = input(': ').strip()
            if not usr_in:
                continue
            mention_handler(usr_in)
            add(role='user', content=usr_in)
            
            # 1. Run the tool loop 
            # (This automatically mutates the `chat` list with tool calls/results)
            final_response = run_tool_loop(chat)
            
            # 2. Display the final response with your rich streaming effect
            full = ''
            with Live(md(full), refresh_per_second=12, console=console) as live:
                # Simulate streaming by yielding chunks of the final response
                for i in range(0, len(final_response), 3):
                    full += final_response[i:i+3]
                    live.update(md(full))
                    time.sleep(0.01) # Adjust speed to your liking
                    
    except KeyboardInterrupt:
        console.print('\nBYE!!')

if __name__ == '__main__':
    main()