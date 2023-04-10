from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
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


def display_image(image):
    plt.imshow(image)
    plt.show()


def get_dominant_color(image):
    colors = image.convert("RGB").getcolors(image.size[0] * image.size[1])
    most_frequent_color = max(colors, key=lambda x: x[0])[1]
    return most_frequent_color


def color_distance(color1, color2):
    return np.sqrt(
        (color1[0] - color2[0]) ** 2
        + (color1[1] - color2[1]) ** 2
        + (color1[2] - color2[2]) ** 2
    )


def find_closest_image(image, sample_images):
    image_color = get_dominant_color(image)
    closest_sample = None
    min_distance = float("inf")

    for i, sample in enumerate(sample_images):
        sample_color = get_dominant_color(sample)
        distance = color_distance(image_color, sample_color)

        if distance < min_distance:
            min_distance = distance
            closest_sample = i

    return closest_sample
