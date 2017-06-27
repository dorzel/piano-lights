class Pixel:
    """the pixel class holds information for each pixel that is set by
    pressing a key on the keyboard"""
    def __init__(self, num, initial_color):
        self.num = num
        self.initial_color = initial_color
        self.current_color = initial_color

    def reset_color(self):
        """reset the current color to the initial color"""
        self.current_color = self.initial_color

    def effect_func(self):
        pass
