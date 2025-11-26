import os
import threading
from src import config, workers, logger


def ensure_directories():

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
                logger.log_msg("SYSTEM", f"Folder created: {os.path.basename(folder)}")
            except OSError as e:
                logger.log_msg("SYSTEM", f"Error while creating folder: {folder}: {e}")

    if not os.path.exists(config.WATERMARK_FILE):
        logger.log_msg("SYSTEM", f"!!! There is a file missing'{os.path.basename(config.WATERMARK_FILE)}' !!!")
        logger.log_msg("SYSTEM", "Insert watermark image into the folder")


def run_app():

    ensure_directories()

    producer_thread = threading.Thread(target=workers.producer)
    producer_thread.start()

    worker_threads = []
    for i in range(config.NUM_WORKERS):
        t = threading.Thread(target=workers.worker, args=(i + 1,))
        t.start()
        worker_threads.append(t)

    all_threads = [producer_thread] + worker_threads

    logger.log_msg("SYSTEM", f"app started with {config.NUM_WORKERS} workers")
    logger.log_msg("SYSTEM", "watching images")


    try:
        input("\n>>> Press enter to exit program<<<\n\n")
    except KeyboardInterrupt:

        print()
        pass

    logger.log_msg("SYSTEM", "Stopping all threads...")

    workers.stop_threads()

    for t in all_threads:
        t.join()

    logger.log_msg("SYSTEM", "all threads stopped, goodbye")