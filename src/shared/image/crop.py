import cv2
import matplotlib.pyplot as plt
import numpy as np

from .color import *


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


def crop_image_px(image, top, right, bottom, left):
    cropped = image.crop(
        (
            left,
            top,
            right,
            bottom,
        )
    )
    return cropped
