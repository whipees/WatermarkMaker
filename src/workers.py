import time
import os
import queue
from src import config,logger,image_processing

task_queue = queue.Queue()
running = True

def stop_threads():
    global running
    running = False

def producer():
    logger.logger("Producer","Scanning the folder")

    while running:
        try:
            if not os.path.exists(config.INPUT_FOLDER):
                time.sleep(1)
                continue

            files = os.listdir(config.INPUT_FOLDER)
            for file in files:
                full_path = os.path.join(config.INPUT_FOLDER, file)
                if os.path.isfile(full_path):
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                        task_queue.put((full_path, file))
                        logger.log_msg("PRODUCER", f"Added to queue: {file}")

            time.sleep(1)
        except Exception as e:
            logger.log_msg("PRODUCER", f"Error: {e}")