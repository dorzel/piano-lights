class BaseEffect:
    """this is the base class for all effects, and all effects much inherit
    from this class. An effect has a function that takes in a list of integer
    [r,g,b] values and transforms them according to the effect desired,
    returning a new list of [r.g,b] values. When the effect is done (doneness
    is monitored by the function), it returns None.
    """
    def __init__(self):
        self._done = False

    def effect_func(self, rgb_in):
        pass


class ReduceEffect(BaseEffect):
    """the reduce effect simply reduces each rgb value every time it is
    looped through, ending when all values are zero.
    """
    def effect_func(self, rgb_in):
        if not all(comp == 0 for comp in rgb_in):
            return [comp - 6 if comp > 0 and comp - 6 > 0 else 0 for comp in
                    rgb_in]
        else:
            # all components are 0, ending the effect
            return None
