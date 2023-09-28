raise NotImplementedError

class LayerParams(object):
    def __init__(self, index, name, fancy_name, color1, color2):
        self.index = index
        self.name = name
        self.fancy_name = fancy_name
        self.color1 = color1
        self.color2 = color2
