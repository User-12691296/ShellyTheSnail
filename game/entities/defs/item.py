import random

from ..classes import Entity, ItemStack

from constants import GAME

class ItemEntity(Entity):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

    @staticmethod
    def getNeededAssets():
        return []

    def isItemEntity(self):
        return True

    def placeInWorld(self, world, pos, scat=0):
        real_pos = [*pos]
        real_pos[0] += random.choice([1, 0, -1])*scat
        real_pos[1] += random.choice([1, -1] if real_pos[0]==pos[0] else [1, 0, -1])*scat
        self.setPos(real_pos)

        world.addEntity(self)
        if self.world.getTileID(self.pos) == "volcanolava" and self.stack.getItemID() == "dynamite_string":
            self.stack = ItemStack("dynamite", self.stack.getCount())


    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        bcenter = self.world.tilePosToBufferPos(self.pos)
        dcenter = self.bufferPosToDisplayPos(bcenter, display_topleft)

        dtopleft = [coord + GAME.TILE_SIZE//2 for coord in dcenter]
        
        self.stack.drawAsStack(display, dtopleft)
