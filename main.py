from ui.rui import (
    main_panel,
    prompt,
    queue,
    c,
    end,
    show_queued_input,
)
from queue_state import dequeue
import threading
from llm import ask_ai, thinking, response, F
from state import add, out
from api_format import to_api
from ui.render import render
from ui.events import event
from tools import set_event_sink

c.clear()
model = F.get("MODEL")
set_event_sink(event)
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
            event("error", "Request failed", data["error"])
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
