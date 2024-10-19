from ..classes import Item
from misc import animations
import math

SWING_FRAMES = 10

class Gem(Item):
    def __init__(self, itemid, tex_name, size):
        super().__init__(itemid, tex_name, False, size)
    
##    def initData(self):
##        data = super().initData()
##        return data

    def tick(self, data, player, world):
        data["animations"].tick()

GEMS = []
Gem("redgem", "redgem", 0).addToGroup(GEMS)
Gem("bluegem", "bluegem", 0).addToGroup(GEMS)
Gem("greengem", "greengem", 0).addToGroup(GEMS)
Gem("purplegem", "purplegem",0).addToGroup(GEMS)
Gem("pinkgem", "pinkgem",0).addToGroup(GEMS)

