import threading

print_lock = threading.Lock()

def logger(worker_name, message):
    with print_lock:
        print(f"[{worker_name}] {message}")
