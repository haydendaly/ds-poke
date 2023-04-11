import cv2
import numpy as np
from collections import Counter


def get_dominant_color(image):
    colors = image.convert("RGB").getcolors(image.size[0] * image.size[1])
    most_frequent_color = max(colors, key=lambda x: x[0])[1]
    return most_frequent_color


def get_average_color(image):
    colors = image.convert("RGB").getcolors(image.size[0] * image.size[1])
    total_color = [0, 0, 0]
    total_pixels = 0

    for count, color in colors:
        total_color[0] += count * color[0]
        total_color[1] += count * color[1]
        total_color[2] += count * color[2]
        total_pixels += count

    average_color = tuple(channel // total_pixels for channel in total_color)
    return average_color


def color_distance(color1, color2):
    return np.sqrt(
        (color1[0] - color2[0]) ** 2
        + (color1[1] - color2[1]) ** 2
        + (color1[2] - color2[2]) ** 2
    )


def extract_color_histogram(image, bins=(8, 8, 8)):
    hist = cv2.calcHist([image], [0, 1, 2], None,
                        bins, [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()
