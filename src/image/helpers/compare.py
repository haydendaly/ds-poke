from .color import *


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
