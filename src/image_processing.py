import os
from PIL import Image, UnidentifiedImageError
from src import config


def apply_watermark(filepath, watermark_path, output_folder, filename):
    """
    Opens an image, applies a watermark to the bottom-right corner, scale it, and saves the result
    :param filepath:path to the input image
    :param watermark_path: path to the watermark image
    :param output_folder: path to the folder where the watermark image is stored
    :param filename: filename of the image
    """
    try:
        base_image = Image.open(filepath).convert("RGBA")
        watermark = Image.open(watermark_path).convert("RGBA")

        target_width = int(base_image.width * config.WATERMARK_SCALE_RATIO)
        if watermark.width > target_width:
            ratio = target_width / float(watermark.width)
            new_height = int(watermark.height * ratio)

            watermark = watermark.resize((target_width, new_height), Image.Resampling.LANCZOS)

        x = base_image.width - watermark.width - config.PADDING
        y = base_image.height - watermark.height - config.PADDING

        x = max(0, x)
        y = max(0, y)

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

