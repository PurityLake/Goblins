"""
tiledata
This module creates a simple structure that holds information on a potential tile
on the map of the game
"""

from .jsondata import JSONData

class TileData(object):
    """
    TileData:
    Data class that holds information on a particular potential tile.
    =====
    Data Members:
    char: the character that represents the tile on the map
    color: color of the char
    bgcolor: background color of the tile
    walk: whether an AI can pass through the tile
    chance: the likelihood of being picked by random.choice
    """

    def __init__(self, **kwargs):
        self.char = kwargs["char"]
        self.color = kwargs["color"]
        self.bgcolor = kwargs["bgcolor"]
        self.walk = kwargs["walk"]
        self.chance = kwargs["chance"]