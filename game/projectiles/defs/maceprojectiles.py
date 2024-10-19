from ..classes import Projectile

class CelestialMaceProj(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.4

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["celestialmaceproj"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity):
                entity.damage(0.2)
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "celestialmaceproj", display_topleft)

class CrystalMaceProj(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.3

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["crystalmaceproj"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity):
                entity.damage(0.2)
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)
        self.stdDraw(display, "crystalmaceproj", display_topleft)

class DarknessMaceProj(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.4

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["darknessmaceproj"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity):
                entity.damage(0.4)
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "darknessmaceproj", display_topleft)

class MoltenMaceProj(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.3

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["moltenmaceproj"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity):
                entity.damage(0.2)
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)
        self.stdDraw(display, "moltenmaceproj", display_topleft)

class ScissorBullet(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.4

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["GenericIceBullet"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity):
                entity.damage(4)
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "GenericIceBullet", display_topleft)



MACEPROJECTILES = []
MoltenMaceProj.addToGroup(MACEPROJECTILES)
DarknessMaceProj.addToGroup(MACEPROJECTILES)
CelestialMaceProj.addToGroup(MACEPROJECTILES)
CrystalMaceProj.addToGroup(MACEPROJECTILES)
ScissorBullet.addToGroup(MACEPROJECTILES)
