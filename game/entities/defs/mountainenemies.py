import pygame

from ..classes import Enemy
from ...projectiles import PROJECTILE_CLASSES

class MountainEagle(Enemy):
    def __init__(self):
        super().__init__(3, 0, 30)

    @staticmethod
    def getNeededAssets():
        return ["mountaineagle"]

    def isEnemy(self):
        return True

    def damageTick(self):
        if self.world.player.diagonalTo(self.pos) <= 8 and not self.isCooldownActive("feather"):
            feather = PROJECTILE_CLASSES.Feather.fromStartEnd(self.pos, self.world.player.getPos())
            feather.giveImmunity(self)
            self.world.addProjectile(feather)
            self.registerCooldown("feather", 50)


        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.3)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("mountaineagle")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class MountainGoat(Enemy):
    def __init__(self):
        super().__init__(4, 0, 35)

    @staticmethod
    def getNeededAssets():
        return ["mountaingoat"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(1)
                self.damage(1)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("mountaingoat")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class MountainGolem(Enemy):
    def __init__(self):
        super().__init__(10, 0, 55)

    @staticmethod
    def getNeededAssets():
        return ["mountaingolem"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(2)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("mountaingolem")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class MountainSlime(Enemy):
    def __init__(self):
        super().__init__(5, 0, 30)

    @staticmethod
    def getNeededAssets():
        return ["mountainslime"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.1)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("mountainslime")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class MountainTroll(Enemy):
    def __init__(self):
        super().__init__(4, 0, 50)

    @staticmethod
    def getNeededAssets():
        return ["mountaintroll"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.5)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("mountaintroll")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)
class MountainBat(Enemy):
    def __init__(self):
        super().__init__(5, 0, 30)

    @staticmethod
    def getNeededAssets():
        return ["mountainbat"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.2)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("mountainbat")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)


# Add crystal enemies to a group of enemies
MOUNTAINEAGLES = []
MountainEagle.addToGroup(MOUNTAINEAGLES)

MOUNTAINGOATS = []
MountainGoat.addToGroup(MOUNTAINGOATS)

MOUNTAINGOLEMS = []
MountainGolem.addToGroup(MOUNTAINGOLEMS)

MOUNTAINSLIMES = []
MountainSlime.addToGroup(MOUNTAINSLIMES)

MOUNTAINTROLLS = []
MountainTroll.addToGroup(MOUNTAINTROLLS)

MOUNTAINBATS = []
MountainBat.addToGroup(MOUNTAINBATS)

