from .damaging import DamageTile
from .basic import BasicTile
from ...items.classes import ItemStack
from ...entities import ENTITY_CLASSES
from ...projectiles import PROJECTILE_CLASSES

class VolcanoLava(DamageTile):
    def __init__(self, tex_name):
        super().__init__(tex_name, tex_name, 0.2)
        self.items = {}

    def gatherAllIDS(self, world, tile_pos):
        self.items = {}
        
        for entity in world.getEntitiesInRangeOfTile(tile_pos, 5):
            if entity.isItemEntity():
                ID = entity.stack.getItemID()
                self.items[ID] = entity
                

    def onLeft(self,world, tile_pos):
        player = world.getPlayer()
        self.gatherAllIDS(world, tile_pos)
        for item_entity in self.items:

            stack = self.items[item_entity].stack
            entity = stack.item

            if entity.isUpgradeable() and player.inventory.getSelectedStack().getItemID() == "redgem" and stack.getRarity() == 0:
                stack.setRarity(1)
                gem = player.inventory.getSelectedStack()
                gem.consume()
                player.inventory.cullEmptyStacks()

            elif entity.isUpgradeable() and player.inventory.getSelectedStack().getItemID() == "greengem" and stack.getRarity() == 1:
                stack.setRarity(2)
                gem = player.inventory.getSelectedStack()
                gem.consume()
                player.inventory.cullEmptyStacks()

            elif entity.isUpgradeable() and player.inventory.getSelectedStack().getItemID() == "bluegem" and stack.getRarity() == 2:
                stack.setRarity(3)
                gem = player.inventory.getSelectedStack()
                gem.consume()
                player.inventory.cullEmptyStacks()

            
            print(stack.getRarity())

class VolcanoMolten(DamageTile):
    def __init__(self):
        super().__init__("volcanomolten", "volcanomolten", 0.1)    

    def gatherAllIDS(self, world, tile_pos):
        self.items = {}
        for entity in world.getEntitiesInRange(5):
            if entity.isItem():
                ID = entity.stack.getItemID()
                self.items[ID] = self.items.get(ID, 0) + entity.stack.getCount()
                

    def onLeft(self,world,tile_pos):
        self.gatherAllIDS(world, tile_pos)
        player = world.getPlayer()
        for item in self.items:
            entity = ItemStack(item, self.items[item])
        
            if entity.isUpgradeable() and player.inventory.getSelectedStack().getItemID() == "redgem" and entity.getRarity() == 0:
                entity.setRarity(1)
                player.inventory.getSelectedStack().change
            if entity.isUpgradeable() and player.inventory.getSelectedStack().getItemID() == "greengem" and entity.getRarity() == 1:
                entity.setRarity(2)
            if entity.isUpgradeable() and player.inventory.getSelectedStack().getItemID() == "bluegem" and entity.getRarity() == 2:
                entity.setRarity(3)
