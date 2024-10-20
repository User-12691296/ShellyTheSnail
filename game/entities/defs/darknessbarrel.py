import pygame
import random


from ..classes import Barrel, ItemStack
from ...items import Inventory, ItemStack

class DarknessBronze(Barrel):
    def __init__(self):
        super().__init__(5, 0, 30)
        self.loadInventory()
        self.inventory.setItemStack(ItemStack("banana", (random.randint(3, 10))), 0)
        self.inventory.setItemStack(ItemStack("watermelon", (random.randint(1, 3))), 1)
        self.inventory.setItemStack(ItemStack("silver_apple", (random.randint(1, 3))), 2)
        

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

class DarknessSilver(Barrel):
    def __init__(self):
        super().__init__(5, 0, 30)
        self.loadInventory()
        self.inventory.setItemStack(ItemStack("knightmare_scythe", 1), 0)
        self.inventory.setItemStack(ItemStack("cosmic_mace", 1), 1)


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

class DarknessGold(Barrel):
    def __init__(self):
        super().__init__(5, 0, 30)
        self.loadInventory()
        self.inventory.setItemStack(ItemStack("cosmic_mace", 1), 1)
        self.inventory.setItemStack(ItemStack("knightmare_scythe", 1), 2)
        self.inventory.setItemStack(ItemStack("deepdark_armor", 1), 0)

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

class DarknessPlat(Barrel):
    def __init__(self):
        super().__init__(5, 0, 30)
        self.loadInventory()
        self.inventory.setItemStack(ItemStack("deepdark_armor", 1), 0)
        self.inventory.setItemStack(ItemStack("cosmic_mace", 1), 1)
        self.inventory.setItemStack(ItemStack("knightmare_scythe", 1), 2)


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
DARKNESSBRONZE = []
DarknessBronze.addToGroup(DARKNESSBRONZE)

DARKNESSSILVER = []
DarknessSilver.addToGroup(DARKNESSSILVER)

DARKNESSGOLD = []
DarknessGold.addToGroup(DARKNESSGOLD)

DARKNESSPLAT = []
DarknessPlat.addToGroup(DARKNESSPLAT)
