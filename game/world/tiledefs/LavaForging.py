from .damaging import DamageTile
from ...items.classes import ItemStack
from ...entities import ENTITY_CLASSES
from ...projectiles import PROJECTILE_CLASSES

class VolcanoLava(DamageTile):
    def __init__(self):
        super().__init__("volcanolava", "volcanolava", 0.2)

    def onLeft(self, world, tile_pos):pass
##        player=world.getPlayer()
##        if player.inventory.getSelectedStack() != None:
##            if player.inventory.getSelectedStack().getItemID() == "rusty_mirror":
##                player.inventory.setItemStack(None, player.inventory.selected_slot)
##                player.inventory.addItemStack(ItemStack("purifying_mirror", 1))
##                BOSS_CONDITIONS.setSnailSpawn(False)
                
##            player.inventory.setItemStack((ItemStack("purifying_mirror", 1), player.inventory.selected_slot))
####            player.inventory.addItemStack(ItemStack("purifying_mirror", 1))

    
class VolcanoMolten(DamageTile)
    def __init__(self):
        super().__init__("volcanomolten", "volcanomolten", 0.1)    

    def onLeft(self, world, tile_pos):pass
