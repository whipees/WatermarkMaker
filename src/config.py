import os

BASE_DIR = os.getcwd()
INPUT_FOLDER = os.path.join(BASE_DIR, "input_images")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output_watermarked")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed_originals")
ERROR_FOLDER = os.path.join(BASE_DIR, "error_files")


WATERMARK_FILE = os.path.join(BASE_DIR, "watermark.png")

NUM_WORKERS = 4

WATERMARK_SCALE_RATIO = 0.3
PADDING = 20