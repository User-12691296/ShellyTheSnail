import pygame
import random


from ..classes import Barrel, ItemStack
from ...items import Inventory, ItemStack

class SwampBronze(Barrel):
    def __init__(self):
        super().__init__(5, 0, 30)
        self.loadInventory()
        self.inventory.setItemStack(ItemStack("orange", (random.randint(3, 10))), 0)
        self.inventory.setItemStack(ItemStack("banana", (random.randint(1, 3))), 1)
        self.inventory.setItemStack(ItemStack("lemon", (random.randint(1, 3))), 2)
        

    @staticmethod
    def getNeededAssets():
        return ["bronze"]

    def isEnemy(self):
        return True
    
    def tick(self):
        super().tick()
        if self.getHealth() <= 0:
            self.dropItems
    
    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)
        
        self.atlas.drawTexture(display, spos, "bronze")

class SwampSilver(Barrel):
    def __init__(self):
        super().__init__(5, 0, 30)
        self.loadInventory()
        self.inventory.setItemStack(ItemStack("epic_sword", 1), 0)
        self.inventory.setItemStack(ItemStack("snake_mace", 1), 1)


    @staticmethod
    def getNeededAssets():
        return ["silver"]

    def isEnemy(self):
        return True
    
    def tick(self):
        super().tick()
        if self.getHealth() <= 0:
            self.dropAllitems
    
    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)
        
        self.atlas.drawTexture(display, spos, "silver")

class SwampGold(Barrel):
    def __init__(self):
        super().__init__(5, 0, 30)
        self.loadInventory()
        self.inventory.setItemStack(ItemStack("swamp_armor", 1), 0)
        self.inventory.setItemStack(ItemStack("snake_mace", 1), 1)
        self.inventory.setItemStack(ItemStack("pizza_gun", 1), 2)


    @staticmethod
    def getNeededAssets():
        return ["gold"]

    def isEnemy(self):
        return True
    
    def tick(self):
        super().tick()
        if self.getHealth() <= 0:
            self.dropAllitems
    
    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)
        
        self.atlas.drawTexture(display, spos, "gold")

class SwampPlat(Barrel):
    def __init__(self):
        super().__init__(5, 0, 30)
        self.loadInventory()
        self.inventory.setItemStack(ItemStack("swamp_armor", 1), 0)
        self.inventory.setItemStack(ItemStack("snake_mace", 1), 1)
        self.inventory.setItemStack(ItemStack("pizza_gun", 1), 2)


    @staticmethod
    def getNeededAssets():
        return ["plat"]

    def isEnemy(self):
        return True
    
    def tick(self):
        super().tick()
        if self.getHealth() <= 0:
            self.dropAllitems
    
    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)
        
        self.atlas.drawTexture(display, spos, "plat")

#Add crystal barrels to a group of barrels
SWAMPBRONZE = []
SwampBronze.addToGroup(SWAMPBRONZE)

SWAMPSILVER = []
SwampSilver.addToGroup(SWAMPSILVER)

SWAMPGOLD = []
SwampGold.addToGroup(SWAMPGOLD)

SWAMPPLAT = []
SwampPlat.addToGroup(SWAMPPLAT)