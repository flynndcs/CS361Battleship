from enum import Enum
import os.path
from pygame import image


class ImageLoader:

    def __init__(self):
        self.images = {}  # container of all of our loaded images

    def load_image(self, load_image):
        if load_image.name in self.images:
            # if the image was already loaded
            return self.images[load_image.name]
        else:
            # if the image has not been loaded we load it real fast
            self._retrieve_image(load_image)
            return self.images[load_image.name]

    def _retrieve_image(self, load_image):
        # loading the image from file
        if os.path.isfile(load_image.value):
            self.images[load_image.name] = image.load(load_image.value)
        else:
            self.images[load_image.name] = image.load(ImageEnum.DNE.value)

    def _delete_image(self, load_image):
        # delete the image data from our store
        del self.images[load_image]


class ImageEnum(Enum):
    # image enumerates for easily loading files without the whole file name
    TitleBackground = "res/backgrounds/Title_screen_background.png"
    DNE = "res/DNE.png"
    ARROW = "res/arrow.png"
