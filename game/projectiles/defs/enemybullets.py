from ..classes import Projectile
## INCLUDES POISON DART, FEATHER
class PoisonDart(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.3

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["poison_dart"]

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

        self.stdDraw(display, "poison_dart", display_topleft)

class Feather(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.3

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["feather_bullet"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity) and not entity.isEnemy():
                entity.damage(1)
                ##player.setAttribute("movement_speed", 10)                
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "feather_bullet", display_topleft)
        
class SwampBullet(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.3

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["GenericSwampBullet"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity) and not entity.isEnemy():
                entity.damage(0.4)
                ##player.setAttribute("movement_speed", 10)                
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "GenericSwampBullet", display_topleft)

class DesertBullet(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.3

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["GenericDessertBullet"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity) and not entity.isEnemy():
                entity.damage(0.5)
                ##player.setAttribute("movement_speed", 10)                
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "GenericDessertBullet", display_topleft)

class DarknessBullet(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.3

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["GenericDarknessBullet"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity) and not entity.isEnemy():
                entity.damage(1)
                ##player.setAttribute("movement_speed", 10)                
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "GenericDarknessBullet", display_topleft)

class IceBullet(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.3

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
            # self.init_effect = lambda x, y, z: None

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity) and not entity.isEnemy():
                entity.damage(0.8)
                ##player.setAttribute("movement_speed", 10)                
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "GenericIceBullet", display_topleft)
        
class CrystalBullet(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.3

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["GenericSilverBullet"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity) and not entity.isEnemy():
                entity.damage(0.4)
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "GenericSilverBullet", display_topleft)

ENEMYBULLETS = []
CrystalBullet.addToGroup(ENEMYBULLETS)  
IceBullet.addToGroup(ENEMYBULLETS)
DarknessBullet.addToGroup(ENEMYBULLETS)
DesertBullet.addToGroup(ENEMYBULLETS)
SwampBullet.addToGroup(ENEMYBULLETS)
PoisonDart.addToGroup(ENEMYBULLETS)
Feather.addToGroup(ENEMYBULLETS)
