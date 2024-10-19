from ..classes import Enemy

class Blob(Enemy):
    def __init__(self):
        super().__init__(5, 0, 30)

    @staticmethod
    def getNeededAssets():
        return ["blob"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(5)
                self.damage(30)

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)
        
        self.atlas.drawTexture(display, spos, "blob")


# Add Blob to a group of enemies
BLOBS = []
Blob.addToGroup(BLOBS)
