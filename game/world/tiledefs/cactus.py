from .slowing import SlowTile
from ...items.classes import Inventory

class Cactus(SlowTile):
    def __init__(self, tileid, tex_name, damage_value, slow_value, rscat=True):
        super().__init__(tileid, tex_name, rscat)
        
        self.damage_value = damage_value
        self.slow_value = slow_value 
        
    def onWalk(self, world, tile_pos):
        super().onWalk(world, tile_pos)
        player = world.getPlayer()

        damage = self.damage_value
        if player.inventory.getItemStack(24) != None:
            if player.inventory.getItemStack(-1).item.getItemID() == "croc":
                damage = 0

        player.damage(damage)
