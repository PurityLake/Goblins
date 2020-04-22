from .jsondata import JSONData

class TileData(object):
    def __init__(self, **kwargs):
        self.char = kwargs["char"]
        self.color = kwargs["color"]
        self.bgcolor = kwargs["bgcolor"]
        self.walk = kwargs["walk"]
        self.chance = kwargs["chance"]