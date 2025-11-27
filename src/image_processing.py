import os
from PIL import Image, UnidentifiedImageError

def apply_watermark(filepath, watermark_path, output_folder, filename):
    """
    Opens an image, applies a watermark to the bottom-right corner, and saves the result
    :param filepath:path to the input image
    :param watermark_path: path to the watermark image
    :param output_folder: path to the folder where the watermark image is stored
    :param filename: filename of the image
    """
    try:
        base_image = Image.open(filepath).convert("RGBA")
        watermark = Image.open(watermark_path).convert("RGBA")

        x = max(0, base_image.width - watermark.width - 20)
        y = max(0, base_image.height - watermark.height - 20)

        base_image.paste(watermark, (x, y), watermark)

        final_image = base_image.convert("RGB")
        output_path = os.path.join(output_folder, f"watermarked_{filename}")
        final_image.save(output_path, "PNG")

        base_image.close()
        watermark.close()
        return True
    except UnidentifiedImageError:
        raise ValueError("not a valid image")
    except FileNotFoundError:
        raise FileNotFoundError("watermark not found")

