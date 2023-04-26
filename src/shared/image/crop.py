from PIL import Image


def crop_image(image, top, right, bottom, left, rotation=0):
    if rotation != 0:
        image = image.rotate(rotation, resample=Image.BICUBIC, expand=True)

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


def crop_image_px(image, top, right, bottom, left, rotation=0):
    if rotation != 0:
        image = image.rotate(rotation, resample=Image.BICUBIC, expand=True)

    cropped = image.crop(
        (
            left,
            top,
            right,
            bottom,
        )
    )
    return cropped
