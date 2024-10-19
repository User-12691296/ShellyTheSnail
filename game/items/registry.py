import pygame
import os

from misc.textures import TextureAtlas

from .classes import Item
from .defs import ALL_ITEM_CLASSES

ASSETS = "assets/game"

    
def registerAllItems(registry):
    for itemClass in ALL_ITEM_CLASSES:
        itemClass.register(registry)

class SMALL_ITEM_TEXTURE_PRESETS:
    FOLDER       = os.path.join(ASSETS, "items", "small")
    SIZE         = 64
    EXT          = ".png"
    RESCALE      = True
    TRANSPARENCY = True

class MEDIUM_ITEM_TEXTURE_PRESETS:
    FOLDER       = os.path.join(ASSETS, "items", "medium")
    SIZE         = 96
    EXT          = ".png"
    RESCALE      = True
    TRANSPARENCY = True

class LARGE_ITEM_TEXTURE_PRESETS:
    FOLDER       = os.path.join(ASSETS, "items", "large")
    SIZE         = 128
    EXT          = ".png"
    RESCALE      = True
    TRANSPARENCY = True

class ItemRegistry:
    def __init__(self):
        self.items = {}

        self._atlas_loaded = False

    def loadAtlas(self):
        self.atlasses = [TextureAtlas.fromPreset(SMALL_ITEM_TEXTURE_PRESETS),
                         TextureAtlas.fromPreset(MEDIUM_ITEM_TEXTURE_PRESETS),
                         TextureAtlas.fromPreset(LARGE_ITEM_TEXTURE_PRESETS)]

        self._atlas_loaded = True

    def addItem(self, item):
        if not self._atlas_loaded:
            raise RuntimeError("Item registry texture atlas not loaded yet")
        
        self.items[item.getItemID()] = item

        item.setAtlas(self.atlasses[item.tex_size])

    def addItems(self, items):
        for item in items:
            self.addItem(item)

    def getItem(self, itemid):
        return self.items.get(itemid)

