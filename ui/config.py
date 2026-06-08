import json 
import os 

UI_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".ui.json")

default_ui = {
    'panel':"#e74d10",
    'prompt':'white',
    'statusline':'white'
}
# CDUI stands for create default UI
def cdui():
    if not os.path.exists(UI_FILE):
        with open(UI_FILE, 'w') as ui:
            json.dump(default_ui, ui, indent=4)
    print(f'Done {UI_FILE} with {default_ui}')







