import os
import threading
from src import config, workers, logger
import time

def ensure_directories():
    """
    Checks if necessary directories exist and creates them if they are missing
    Also verifies the existence of the watermark file
    """
    folders = [
        config.INPUT_FOLDER,
        config.OUTPUT_FOLDER,
        config.PROCESSED_FOLDER,
        config.ERROR_FOLDER
    ]

    for folder in folders:
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
                logger.logger("SYSTEM", f"Folder created: {os.path.basename(folder)}")
            except OSError as e:
                logger.logger("SYSTEM", f"Error while creating folder: {folder}: {e}")

    if not os.path.exists(config.WATERMARK_FILE):
        logger.logger("SYSTEM", f"!!! There is a file missing'{os.path.basename(config.WATERMARK_FILE)}' !!!")
        logger.logger("SYSTEM", "Insert watermark image into the folder")


def run_app():
    """
    Initializes the application, starts the producer and worker threads,
    and handles the main loop
    """
    ensure_directories()

    start_time = time.time()

    producer_thread = threading.Thread(target=workers.producer)
    producer_thread.start()

    worker_threads = []
    for i in range(config.NUM_WORKERS):
        t = threading.Thread(target=workers.worker, args=(i + 1,))
        t.start()
        worker_threads.append(t)

    all_threads = [producer_thread] + worker_threads

    logger.logger("SYSTEM", f"app started with {config.NUM_WORKERS} workers")
    logger.logger("SYSTEM", "watching images")


    try:
        input("\n>>> Press enter to exit program<<<\n\n")
    except KeyboardInterrupt:

        print()
        pass

    logger.logger("SYSTEM", "Stopping all threads...")

    workers.stop_threads()

    for t in all_threads:
        t.join()

    end_time = time.time()
    duration = end_time - start_time

    logger.logger("SYSTEM", f"Finished in {duration:.2f} seconds")

    logger.logger("SYSTEM", "all threads stopped, goodbye")