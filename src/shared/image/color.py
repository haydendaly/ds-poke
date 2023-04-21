import cv2
import matplotlib.pyplot as plt
import numpy as np


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


def display_image(image):
    plt.imshow(image)
    plt.show()


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


def extract_color_histogram(image, bins=(8, 8, 8)):
    hist = cv2.calcHist([image], [0, 1, 2], None, bins, [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()


def find_closest_image(image, sample_images):
    image_color = get_average_color(image)
    closest_sample = None
    min_distance = float("inf")

    for i, sample in enumerate(sample_images):
        sample_color = get_average_color(sample)
        distance = color_distance(image_color, sample_color)

        if distance < min_distance:
            min_distance = distance
            closest_sample = i

    return closest_sample


def extract_color_histogram(image, bins=(8, 8, 8)):
    hist = cv2.calcHist([image], [0, 1, 2], None, bins, [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()


def find_closest_image(image, sample_images):
    image_color = get_average_color(image)
    closest_sample = None
    min_distance = float("inf")

    for i, sample in enumerate(sample_images):
        sample_color = get_average_color(sample)
        distance = color_distance(image_color, sample_color)

        if distance < min_distance:
            min_distance = distance
            closest_sample = i

    return closest_sample
