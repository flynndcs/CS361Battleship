import pygame.mixer
from enum import Enum
import os.path


class SoundLoader:

    def __init__(self):

        pygame.mixer.init()

        self.sound_effects = {}
        self.bgm = {}

        self.se_volume = 0.5  # float value 0 to 1 inclusive
        self.bgm_volume = 0.5

    def _load_sound(self, sound):
        if os.path.isfile(sound.value):
            if sound == SoundEnum.BGM:
                if sound not in self.bgm:
                    self.bgm[sound] = pygame.mixer.Sound(sound.value)
                    self.bgm[sound].set_volume(self.bgm_volume)
            elif sound not in self.sound_effects:
                self.sound_effects[sound] = pygame.mixer.Sound(sound.value)
                self.sound_effects[sound].set_volume(self.se_volume)
        else:
            print('SOUND FILE NOT FOUND')

    def play_sound(self, sound):

        self._load_sound(sound)
        if sound in self.sound_effects:
            self.sound_effects[sound].play()
        elif sound in self.bgm:
            self.bgm[sound].play()

    def stop_sound(self, sound, fadeout=True):
        if fadeout:
            if sound in self.sound_effects:
                self.sound_effects[sound].fadeout()
            elif sound in self.bgm:
                self.bgm[sound].fadeout()
        else:
            if sound in self.sound_effects:
                self.sound_effects[sound].fadeout()
            elif sound in self.bgm:
                self.bgm[sound].fadeout()

    def set_se_volume(self, volume):

        self.se_volume = volume
        for sound in self.sound_effects:
            self.sound_effects[sound].set_volume(self.se_volume)

    def set_bgm_volume(self, volume):
        self.bgm_volume = volume
        for sound in self.sound_effects:
            self.sound_effects[sound].set_volume(self.bgm_volume)


class SoundEnum(Enum):

    CLICK = "res/sounds/click.wav"
    EXPLOSION = "res/sounds/Explosion.wav"
    INCORRECTPLACEMENT = "res/sounds/incorrect_placement.wav"
    LOSS = "res/sounds/loss.wav"
    MISS = "res/sounds/miss.wav"
    BGM = "Victory-AShamaluevMusic.wav"
    WIN = "win.wav"
