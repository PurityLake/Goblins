"""
gamedata
This module holds all data required by the game and packages it into one place
"""

from .jsondata import JSONData
from .tiledata import TileData

class GameData(object):
    """
    GameData
    Collection of data classes regarding the interals of the games including those
    related to the map and it's generation. 
    ----
    A particular data class can be access by using a subscript with one of the following:
    "tiles" - for map tile attributes
    =====
    Methods
    get_tile_types: Gets the names of each individual tile so that the tiles can be
                    accessed much more easily
    """
    def __init__(self):
        self._tiles = dict()
        self._tile_types =[]
        self._load_tiles()

    def _load_tiles(self):
        data = JSONData("tiles.json")
        self._tile_types = data["types"]
        for t in data["types"]:
            self._tiles[t] = TileData(**data[t])

    def get_tile_types(self):
        return self._tile_types
    
    def __getitem__(self, name):
        if name == "tiles":
            return self._tiles
        raise KeyError("{} is an invalid key in GameData".format(name))