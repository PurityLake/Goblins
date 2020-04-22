"""
jsondata:
This module encapsulates the builtin json module providing appropriate error handling
instead of having it clutter another class.
"""

import json

class JSONData(object):
    def __init__(self, filename):
        self._filename = filename
        self._data = None
        self._loaded = False
        self._load_data()
    
    def _load_data(self):
        try:
            with open(self._filename) as f:
                self._data = json.loads(f.read())
            self._loaded = True
        except IOError as e:
            print("Failed to load file '{}'".format(self._filename))
        except json.JSONDecodeError as e:
            print("Failed to decode file '{}'".format(self._filename))
            print(e.msg);
        
    def loaded_correctly(self):
        return self._loaded
    
    def __getitem__(self, name):
        val = None
        try:
            val = self._data[name]
        except KeyError as e:
            print(e.msg)
        return val
