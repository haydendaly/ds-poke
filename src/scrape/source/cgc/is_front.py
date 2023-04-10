from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

from ....image import crop_image, find_closest_image


def crop_cgc_hologram(image):
    width, height = image.size
    return crop_image(image, top=0.1, right=0.55, bottom=0.75, left=0.2)


# TODO: SWITCH TO TRADITIONAL CLASSIFICATION MODEL
def is_front(image):
    cropped_image = crop_cgc_hologram(image)

    sample_front = crop_cgc_hologram(Image.open("./db/sample/cgc_front.jpg"))
    sample_back = crop_cgc_hologram(Image.open("./db/sample/cgc_back.jpg"))
    is_front = find_closest_image(cropped_image, [sample_front, sample_back]) == 0

    return is_front
