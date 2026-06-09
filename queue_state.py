import queue as queue_module

_msg_queue = queue_module.Queue()


def queue_size():
    return _msg_queue.qsize()


def enqueue(text):
    _msg_queue.put(text)


def dequeue():
    try:
        return _msg_queue.get_nowait()
    except queue_module.Empty:
        return None
