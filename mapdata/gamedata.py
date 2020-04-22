from .jsondata import JSONData
from .tiledata import TileData

class GameData(object):
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