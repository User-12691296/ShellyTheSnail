from .slowing import SlowTile
from ...items.classes import ItemStack
from ...entities import ENTITY_CLASSES
from ...projectiles import PROJECTILE_CLASSES
from constants.game import BOSS_CONDITIONS


class SwampWater(SlowTile):
    def __init__(self):
        super().__init__("swampwater", "swampwater", 2)

    def onLeft(self, world, tile_pos):
        player=world.getPlayer()
        if player.inventory.getSelectedStack() != None:
            if player.inventory.getSelectedStack().getItemID() == "rusty_mirror":
                player.inventory.setItemStack(None, player.inventory.selected_slot)
                player.inventory.addItemStack(ItemStack("purifying_mirror", 1))
                BOSS_CONDITIONS.setSnailSpawn(False)
                BOSS_CONDITIONS.setBossInvincibillity(False)
                
##            player.inventory.setItemStack((ItemStack("purifying_mirror", 1), player.inventory.selected_slot))
####            player.inventory.addItemStack(ItemStack("purifying_mirror", 1))

    
