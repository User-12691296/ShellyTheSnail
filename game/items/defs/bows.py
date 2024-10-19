# ADD A COOLDOWN FOR THIS IN PARTICULAR
from ..classes import Item
from ...projectiles import PROJECTILE_CLASSES
from misc import animations
import math

SWING_FRAMES = 10

class Bow(Item):
    def __init__(self, itemid, tex_name, size, cooldown, arrow = PROJECTILE_CLASSES.Arrow):
        super().__init__(itemid, tex_name, False, size)
        self.cooldown = cooldown # In frames
        self.arrow=arrow

    def tick(self, data, player, world):
        data["animations"].tick()

    def damageTick(self, data, player, world):
        # Handle Swing
        data["rot"] = -(player.getFacing()+90)
        data["rot"] = data["rot"] % 360

    def isUpgradeable(self):
        return True

    def fireInTheHole(self, data, player, world, tile_pos, tile):
        if not data["animations"].exists("cooldown"):
            arrow = self.arrow(player.pos, -data["rot"]-45)
            arrow.giveImmunity(player)
            world.addProjectile(arrow)
            data["animations"].create("cooldown", self.cooldown)
        
    def onLeft(self, data, player, world, tile_pos, tile):
        self.fireInTheHole(data, player, world, tile_pos, tile)
        return True

#class Crossbow(Item):pass
# Do we need separate for crossbow?

BOWS = []
Bow("basic_crossbow", "basic_crossbow", 1, 50).addToGroup(BOWS)
Bow("desert_bow", "desert_bow", 0, 25, arrow=PROJECTILE_CLASSES.MoltenArrow).addToGroup(BOWS)
Bow("frozen_bow", "frozen_bow", 0, 20, arrow=PROJECTILE_CLASSES.IceArrow).addToGroup(BOWS)
Bow("swamp_bow", "swamp_bow", 0, 30).addToGroup(BOWS)
Bow("wood_bow", "wood_bow", 0, 60).addToGroup(BOWS)
Bow("mountain_bow", "mountain_bow", 0, 5).addToGroup(BOWS)
Bow("darkness_bow", "darkness_bow", 0, 5).addToGroup(BOWS)


