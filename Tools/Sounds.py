import pygame.mixer
from enum import Enum
import os.path


class SoundLoader:

    def __init__(self):

        pygame.mixer.init()

        self.sounds = {}

        self.volume = 1  # float value 0 to 1 inclusive

    def _load_image(self, sound):
        if os.path.isfile(SoundEnum.value):
            if sound not in self.sounds:
                self.sounds[sound] = pygame.mixer.Sound(SoundEnum.sound)
                self.sounds[sound].set_volume(self.volume)
        else:
            print('SOUND FILE NOT FOUND')
            self.sounds[sound] = None

    def play_sound(self, sound):

        self._load_image(sound)

        self.sounds[sound].play()

    def stop_sound(self, sound, fadeout=True):
        if fadeout:
            self.sounds[sound].fadeout()
        else:
            self.sounds[sound].stop()

    def set_volume(self, volume):
        self.volume = volume
        for sound in self.sounds:
            self.sounds[sound].set_volume(self.volume)


class SoundEnum(Enum):

    pass
