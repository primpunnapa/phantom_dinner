import numpy as np
import pygame as pg

class SoundEffect:
    __instance = None

    def __init__(self):
        if SoundEffect.__instance is None:
            pg.mixer.init(frequency=44100, channels=2)
            self.__instance = self
            print("Sound Effects Initialized")
            self.__sounds = {
                "move":  self.__generate_tone(0.2, 500),
                "over": self.__generate_tone(1.0, 200),
                "press": self.__generate_tone(0.1, 400),
            }
        else:
            raise Exception("This class is singleton")

    @staticmethod
    def get_instance():
        if SoundEffect.__instance is None:
            SoundEffect.__instance = SoundEffect()
        return SoundEffect.__instance

    def __generate_tone(self, duration, f, sample_rate=44100):
        t = np.arange(0, duration, 1/sample_rate) # x-axis
        wave = np.sin(2 * np.pi * f * t) # y-axis

        bit = 16
        amp = 2 ** (bit-1) - 1 # 2 ^ 15 - 1 = 32767 output range [-32767, 32767]
        wave = amp * wave
        two_ch_wave = np.vstack([wave, wave]).reshape(-1, 2).astype(np.int16)
        sound = pg.sndarray.make_sound(two_ch_wave)
        return sound

    def play_sound(self, effect):
        if effect in self.__sounds:
            self.__sounds[effect].play()

