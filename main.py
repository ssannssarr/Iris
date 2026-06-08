from ui.rui import (
    main_panel,
    prompt,
    queue,
    c,
    reply,
    end,
    show_queued_input,
    dequeue,
    style
)
from ui.msg_state import to_api
import time
import sys
import shutil
import threading
from sv1 import ask_ai, thinking, response, F
from ui.msg_state import add, out, render

c.clear()
model = F.get("MODEL")
main_panel()
usr_in=""
try:
    while True:
        # Check if there is any queued message first
        queued_in = dequeue()
        if queued_in is not None:
            usr_in = queued_in
            show_queued_input(usr_in, model)
        else:
            usr_in = prompt(model)

        if not usr_in:
            continue
        if usr_in == "/exit":
            end()
            break
        add('user',usr_in)
        r = out()
        c.clear()
        main_panel()
        render(r,model=model)

        # Run AI request in a background thread to allow animated spinner and input queueing
        ai_done_event = threading.Event()
        result_container = {}

        def run_api():
            try:
                result_container['data'] = ask_ai(messages=to_api())
            except Exception as e:
                result_container['data'] = {"error": str(e)}
            finally:
                ai_done_event.set()

        api_thread = threading.Thread(target=run_api, daemon=True)
        api_thread.start()

        # Merge fake prompt display and thinking animation/queue input in one call
        queue(model, ai_done_event)
        api_thread.join()

        data = result_container.get('data', {"error": "No response returned"})

        if "error" in data:
            reply(model="error", content=data["error"])
            continue

        res = response(data=data)
        thought = thinking(data)

        # Add to message state and redraw with markdown formatting
        add('assistant', res)
        r = out()
        if r:
            r[-1]['reasoning'] = thought

        c.clear()
        main_panel()
        render(r, model=model)
except (KeyboardInterrupt,EOFError):
    end()

