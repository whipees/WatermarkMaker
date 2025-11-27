import time
import os
import queue
from src import config,logger,image_processing
import shutil

task_queue = queue.Queue()
running = True

def stop_threads():
    """
    Sets the global running flag to False to signal all threads to stop
    """
    global running
    running = False

def producer():
    """
    scans the input folder for new images and adds them to the task queue
    Runs as a separate thread
    """
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
                        logger.logger("PRODUCER", f"Added to queue: {file}")

            time.sleep(1)
        except Exception as e:
            logger.logger("PRODUCER", f"Error: {e}")

def worker(worker_id):
    """
    Retrieves image tasks from the queue, applies the watermark, and handles file movements
    Runs as a separate thread
    :param worker_id: The identifier of the worker thread
    """
    name = f"Worker {worker_id}"
    logger.logger(name, f"Starting worker {worker_id}")

    while running:
        try:
            filepath,filename = task_queue.get(timeout=1)
            if os.path.exists(filepath):
                try:
                    image_processing.apply_watermark(filepath,config.WATERMARK_FILE,config.OUTPUT_FOLDER,filename)
                    logger.logger(name, "WATERMARK PROCESSED")
                    shutil.move(filepath,os.path.join(config.PROCESSED_FOLDER,filename))
                except Exception as e:
                    logger.logger(name, f"error: {e}")
                    if os.path.exists(filepath):
                        shutil.move(filepath, os.path.join(config.ERROR_FOLDER, filename))

            task_queue.task_done()
        except queue.Empty:
            continue