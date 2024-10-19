from ..classes import Item
from misc import animations
import math

SWING_FRAMES = 10

class Geode(Item):
    def __init__(self, itemid, tex_name, size):
        super().__init__(itemid, tex_name, False, size)
    
##    def initData(self):
##        data = super().initData()
##        return data

    def tick(self, data, player, world):
        data["animations"].tick()

GEODES = []
Geode("debug_sword", "sword", 1).addToGroup(GEODES)
Geode("crystal_geode", "crystal_geode", 0).addToGroup(GEODES)
Geode("iron_geode", "iron_geode", 0).addToGroup(GEODES)
Geode("gold_geode", "gold_geode", 0).addToGroup(GEODES)
Geode("purifying_mirror", "purifying_mirror",0).addToGroup(GEODES)
Geode("rusty_mirror", "rusty_mirror",0).addToGroup(GEODES)

Geode("dynamite_string", "dynamite_string",0).addToGroup(GEODES)
Geode("lantern", "alchemycandle", 0).addToGroup(GEODES)