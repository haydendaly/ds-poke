from PIL import Image
import numpy as np
from collections import Counter


def crop_image(image, top, right, bottom, left):
    width, height = image.size
    cropped = image.crop(
        (
            left * width,
            top * height,
            (1 - right) * width,
            (1 - bottom) * height,
        )
    )
    return cropped


def extract_color_histogram(image, bins=(8, 8, 8)):
    hist = cv2.calcHist([image], [0, 1, 2], None,
                        bins, [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()
