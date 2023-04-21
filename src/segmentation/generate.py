from PIL import Image, ImageDraw, ImageFont


class ImageGeneration:
    def __init__(self, df):
        self.df = df
        self.images_and_coords = []

    def generate_image(self, num_cards=5):
        # need to take n cards and put them randomly onto a 500-2000 x 500-2000 image
        # should be different angles, sometimes overalapping, and use fake shadows (not consistent should vary)
        # random background color with noise

        img = Image()
        card_coords = []

        for i in range(num_cards):
            pass

        return (img, card_coords)

    def generate_images(self, n=1):
        for _ in range(n):
            self.images_and_coords.append(self.generate_image())
