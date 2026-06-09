import threading

_lock = threading.Lock()
_pending = None


def request_write_permission(path, content):
    global _pending

    req = {
        "kind": "write_file",
        "path": path,
        "content": content,
        "approved": False,
        "event": threading.Event(),
    }

    with _lock:
        _pending = req

    req["event"].wait()
    return req["approved"]


def has_pending_permission():
    with _lock:
        return _pending is not None


def get_pending_permission():
    with _lock:
        return _pending


def resolve_pending_permission(approved):
    global _pending

    with _lock:
        req = _pending
        _pending = None

    if req is None:
        return

    req["approved"] = approved
    req["event"].set()
