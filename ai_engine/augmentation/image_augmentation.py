import os
import random
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

def augment_qcr_image(image_path: str, output_path: str, variant_type: str) -> Image.Image:
    """
    Applies an image augmentation to the target image and saves the result.
    Supported variants: 'rotation', 'brightness', 'contrast', 'blur', 'noise'
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    image = Image.open(image_path).convert("RGB")

    # 1. ROTATION
    if variant_type == "rotation":
        angle = random.uniform(-4, 4)
        image = image.rotate(
            angle,
            expand=True,
            fillcolor="white"
        )

    # 2. BRIGHTNESS
    elif variant_type == "brightness":
        factor = random.uniform(0.65, 1.35)
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(factor)

    # 3. CONTRAST
    elif variant_type == "contrast":
        factor = random.uniform(0.65, 1.35)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(factor)

    # 4. BLUR
    elif variant_type == "blur":
        radius = random.uniform(0.5, 1.5)
        image = image.filter(
            ImageFilter.GaussianBlur(radius)
        )

    # 5. GAUSSIAN NOISE
    elif variant_type == "noise":
        image_array = np.array(image).astype(np.int16)
        noise = np.random.normal(0, 8, image_array.shape)
        image_array = image_array + noise
        image_array = np.clip(image_array, 0, 255).astype(np.uint8)
        image = Image.fromarray(image_array)

    else:
        raise ValueError(f"Unsupported augmentation variant: {variant_type}")

    # Ensure parent output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    image.save(output_path, quality=90)
    return image
