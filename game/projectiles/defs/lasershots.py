from ..classes import Projectile

class CrystalLaserShot(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.4

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["lasershotcrystal"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity) and not entity.isEnemy():
                entity.damage(1)
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "lasershotcrystal", display_topleft)

LASERSHOTS = []
CrystalLaserShot.addToGroup(LASERSHOTS)
