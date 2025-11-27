import threading

print_lock = threading.Lock()

def logger(worker_name, message):
    """
    Prints the message to the console
    :param worker_name: name of the worker thread whose message is being printed
    :param message: message to be printed
    """
    with print_lock:
        print(f"[{worker_name}] {message}")
