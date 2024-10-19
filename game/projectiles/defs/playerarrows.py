from ..classes import Projectile
from constants import GAME

class Arrow(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.4

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["arrow"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity):
                entity.damage(2.5)
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "arrow", display_topleft)

class BasicProjectileWithEffects(Arrow):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.4
        self.png_name = ""

        self.init_effect = placeholderFunction
        self.tick_effect = placeholderFunction
        self.reverse_effect = placeholderFunction

        self.effect_name = ""
        self.effect_duration = 60
    
    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity):
                entity.damage(2)
                self.kill()
                
                if not entity.isItemEntity():
                    self.effect(entity, self.world, tpos)

    def effect(self, entity, world, tile_pos):
        self.init_effect(entity, world, tile_pos)
        entity.giveEffect(self.effect_name, self.effect_duration, self.tick_effect, self.reverse_effect)


def placeholderFunction (x, y, z):
    return None


# Template arrow
class MoltenArrow(BasicProjectileWithEffects):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.4
        
        self.init_effect = placeholderFunction
        self.tick_effect = self.molten_tick_effect
        self.reverse_effect = placeholderFunction

        self.effect_name = "Molten"
        self.effect_duration = 50

    def getNeededAssets():
        return ["MoltenArrow"]

    def molten_tick_effect(self, entity, world, tile_pos):
        entity.damage(0.2)

    def draw(self, display, display_topleft=(0, 0)):    
        super().draw(display, display_topleft)

        self.stdDraw(display, "MoltenArrow", display_topleft)

class IceArrow(BasicProjectileWithEffects):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.3
        self.normalspeed=None
        
        self.init_effect = placeholderFunction
        self.tick_effect = self.ice_tick_effect
        self.reverse_effect = self.reverse_ice_effect

        self.effect_name = "Ice"
        self.effect_duration = 8

    def getNeededAssets():
        return ["IceArrow"]

    def ice_tick_effect(self, entity, world, tile_pos):
        entity.setMovable(False)

    def reverse_ice_effect(self,entity,world,tile_pos):
        entity.setMovable(True)

    def draw(self, display, display_topleft=(0, 0)):    
        super().draw(display, display_topleft)

        self.stdDraw(display, "IceArrow", display_topleft)



PLAYERARROWS = []
Arrow.addToGroup(PLAYERARROWS)
BasicProjectileWithEffects.addToGroup(PLAYERARROWS)
MoltenArrow.addToGroup(PLAYERARROWS)
IceArrow.addToGroup(PLAYERARROWS)
