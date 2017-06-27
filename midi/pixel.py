from effect import BaseEffect


class Pixel:
    """the pixel class holds information for each pixel that is set by
    pressing a key on the keyboard
    """
    def __init__(self, num, initial_color):
        self.num = num
        self._initial_color = initial_color
        self._current_color = initial_color
        self._effect = BaseEffect()

    def reset_color(self):
        """reset the current color to the initial color"""
        self._current_color = self._initial_color

    def set_color(self, rgb_in):
        """sets the current pixel color to the rgb_in list"""
        self._current_color = rgb_in

    def set_effect(self, effect):
        """takes in an instantiated effect class and sets that as this 
        pixel's effect
        """
        self._effect = effect

    def run_effect(self):
        self._effect.effect_func(self._current_color)
