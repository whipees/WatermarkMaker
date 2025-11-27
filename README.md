# WatermarkMaker - Automated Watermark Processing

**Version:** 1.0.0\
**Date:** November 27, 2024\
**Author:** Sebastian Janíček C4a\
**Contact:** janicek@spsejecna.cz, sebikjanecek@gmail.com\
**School:** SPŠE Ječná\
**Project Type:** School Project 

---

## 1. Introduction and Requirements Specification

This project is a desktop application written in Python designed for
batch processing of images by inserting a watermark. The application
utilizes parallel processing to manage
large volumes of files.

### Functional Requirements

-   **Folder Monitoring:** The application must monitor the input folder
    (`input_images`) in real-time
-   **Image Detection:** Automatically recognizes supported image
    formats (`.jpg`, `.jpeg`, `.png`)
-   **Watermark Insertion:** Inserts a defined watermark
    (`watermark.png`) into the bottom-right corner of input images
-   **Parallel Processing:** Uses multiple threads (Producer-Consumer
    pattern) to avoid blocking during I/O operations and image
    manipulation
-   **File Management:**
    -   Save processed files to `output_watermarked`
    -   Move originals to `processed_originals`
    -   Move corrupted/invalid files to `error_files`
-   **Logging:** All actions logged to console with thread
    identification

### Non-Functional Requirements

-   **Language:** Python 3
-   **Libraries:** Standard libraries (`threading`, `queue`) + Pillow
-   **Thread-Safety:** Implemented using Locks

---

## 2. Application Architecture

Based on the Producer-Consumer design pattern.

### System Components

-   **Main (Control Logic):** Initializes environment, creates
    directories, starts threads
-   **Config:** Stores constants (paths, number of threads)
-   **Logger:** Thread-safe console output via `threading.Lock`
-   **Producer:**
    -   Runs in a separate thread\
    -   Scans input folder\
    -   Pushes file paths into `task_queue`\
-   **Task Queue:** FIFO queue (`queue.Queue`) connecting Producer and
    Workers\
-   **Workers (Consumers):**
    -   Thread pool (default: 4)\
    -   Process images and move files\
-   **Image Processing:** Uses PIL for image manipulation

---

## 3. Application Behavior

### Activity Cycle

1.  **Start:** Run `start.py` → calls `main.py`.\
2.  **Initialization:** `ensure_directories()` creates folders, checks
    watermark.\
3.  **Thread Launch:** Starts 1 Producer + N Worker threads.\
4.  **Producer Loop:** Scans input folder every 1 sec → pushes tasks to
    queue.\
5.  **Worker Loop:**
    -   Wait for queue\
    -   Load image → apply watermark → save result\
    -   Move original to processed/error\
6.  **Termination:**
    -   User presses ENTER → `running = False` → threads finish tasks.

---

## 4. Interfaces and Third-Party Libraries

### Built-in Python Libraries

-   `os, sys, shutil`
-   `threading`
-   `queue`
-   `unittest`
-   `time`

### Third-Party Libraries

-   **Pillow (PIL Fork)**
    -   Image opening, conversion, watermarking, saving
    -   Recommended version: **9.0.0+**

---

## 5. Licensing Aspects


-   **Copyright:** Sebastian Janíček


---

## 6. Configuration

Stored in `src/config.py`.

### Editable Parameters

-   `BASE_DIR`
-   Folders:
    -   `INPUT_FOLDER = input_images`
    -   `OUTPUT_FOLDER = output_watermarked`
    -   `PROCESSED_FOLDER = processed_originals`
    -   `ERROR_FOLDER = error_files`
-   `WATERMARK_FILE = watermark.png`
-   `NUM_WORKERS = 4` (adjustable)

---

## 7. Installation and Execution

### Requirements

-   Python 3.5+
-   `pip`

### Installation Steps

``` bash
pip install Pillow
```

Ensure `watermark.png` exists in the root folder

### Run Application

``` bash
python start.py
```

Folders will be created automatically

---

## 8. Error States and Solutions

  ---
  Code/Error  ,             Description   ,             Solution
  
  Missing watermark   ,     `watermark.png` not found ,  Insert the file into
                                                      the root folder

  UnidentifiedImageError ,  Invalid image (fake .jpg),  File auto-moved to
                                                      `error_files`

  OSError       ,           Permissions issue  ,        Run terminal as
                                                      admin

  KeyboardInterrupt,        User ended program,         Safe shutdown,
  

---

## 9. Testing and Validation

Tests using `unittest`.

### Implemented Tests (`test_app.py`)

-   **`test_paths_exist`** -- Validates config paths
-   **`test_worker_count`** -- Ensures thread count \> 1
-   **`test_corrupt_file_handling`** -- Ensures invalid file is moved to
    error folder



Expected output:\
**Ran 3 tests --- OK**

------------------------------------------------------------------------

## 10. Versions and Known Bugs

### Versions

-   **v1.0.0:** Initial release with watermarking, threading, logging,
    tests

### Known Issues

-   **Watermark positioning:** Fixed offset; small images may show
    imperfect results\
-   **Scaling:** Watermark does not auto-scale yet

------------------------------------------------------------------------

## 11. Specifics (Data, Import/Export)

### Import

-   Folder: `input_images`\
-   Formats: `.jpg`, `.jpeg`, `.png`

### Export

-   Folder: `output_watermarked`\
-   Format: PNG (converted automatically)

### Archiving

-   Originals moved to `processed_originals`

### Database / Network

-   No database\
-   No network usage

------------------------------------------------------------------------


