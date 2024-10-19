import pygame
import random


from ..classes import Barrel, ItemStack
from ...items import Inventory, ItemStack

class FrozenBronze(Barrel):
    def __init__(self):
        super().__init__(5, 0, 30)
        self.loadInventory()
        self.inventory.setItemStack(ItemStack("apple", (random.randint(3, 10))), 0)
        self.inventory.setItemStack(ItemStack("lemon", (random.randint(1, 3))), 1)
        self.inventory.setItemStack(ItemStack("orange", (random.randint(1, 3))), 2)
        

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

class FrozenSilver(Barrel):
    def __init__(self):
        super().__init__(5, 0, 30)
        self.loadInventory()
        self.inventory.setItemStack(ItemStack("ice_blade", 1), 0)
        self.inventory.setItemStack(ItemStack("celestial_mace", 1), 1)


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

class FrozenGold(Barrel):
    def __init__(self):
        super().__init__(5, 0, 30)
        self.loadInventory()
        self.inventory.setItemStack(ItemStack("arctic_armor", 1), 0)
        self.inventory.setItemStack(ItemStack("celestial_mace", 1), 1)
        self.inventory.setItemStack(ItemStack("soul_cannon", 1), 2)


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

class FrozenPlat(Barrel):
    def __init__(self):
        super().__init__(5, 0, 30)
        self.loadInventory()
        self.inventory.setItemStack(ItemStack("arctic_armor", 1), 0)
        self.inventory.setItemStack(ItemStack("celestial_mace", 1), 1)
        self.inventory.setItemStack(ItemStack("soul_cannon", 1), 2)


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
FROZENBRONZE = []
FrozenBronze.addToGroup(FROZENBRONZE)

FROZENSILVER = []
FrozenSilver.addToGroup(FROZENSILVER)

FROZENGOLD = []
FrozenGold.addToGroup(FROZENGOLD)

FROZENPLAT = []
FrozenPlat.addToGroup(FROZENPLAT)