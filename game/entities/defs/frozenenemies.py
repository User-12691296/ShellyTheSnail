import pygame

from ...projectiles import PROJECTILE_CLASSES
from ..classes import Enemy
from ...projectiles import PROJECTILE_CLASSES


class FrozenKnight(Enemy):
    def __init__(self):
        super().__init__(4, 0, 40)

    @staticmethod
    def getNeededAssets():
        return ["frozenknight"]

    def isEnemy(self):
        return True

    def damageTick(self):
        if self.world.player.diagonalTo(self.pos) <= 8 and not self.isCooldownActive("laser"):
            laser = PROJECTILE_CLASSES.IceBullet.fromStartEnd(self.pos, self.world.player.getPos())
            laser.giveImmunity(self)
            self.world.addProjectile(laser)
            self.registerCooldown("laser", 50)
            
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.25)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("frozenknight")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class FrozenPuffer(Enemy):
    def __init__(self):
        super().__init__(4, 0, 40)

    @staticmethod
    def getNeededAssets():
        return ["frozenpuffer"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.25)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("frozenpuffer")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class FrozenTroll(Enemy):
    def __init__(self):
        super().__init__(6, 0, 45)

    @staticmethod
    def getNeededAssets():
        return ["frozentroll"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.3)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("frozentroll")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class FrozenSlime(Enemy):
    def __init__(self):
        super().__init__(6, 0, 40)

    @staticmethod
    def getNeededAssets():
        return ["frozenslime"]

    def isEnemy(self):
        return True

    def damageTick(self):
        if self.world.player.diagonalTo(self.pos) <= 8 and not self.isCooldownActive("laser"):
            laser = PROJECTILE_CLASSES.IceBullet.fromStartEnd(self.pos, self.world.player.getPos())
            laser.giveImmunity(self)
            self.world.addProjectile(laser)
            self.registerCooldown("laser", 50)
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.25)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("frozenslime")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class FrozenWolf(Enemy):
    def __init__(self):
        super().__init__(5, 0, 35)

    @staticmethod
    def getNeededAssets():
        return ["wolf"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.15)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("wolf")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)


# Add crystal enemies to a group of enemies
FROZENKNIGHTS = []
FrozenKnight.addToGroup(FROZENKNIGHTS)

FROZENPUFFERS = []
FrozenPuffer.addToGroup(FROZENPUFFERS)

FROZENTROLLS = []
FrozenTroll.addToGroup(FROZENTROLLS)

FROZENSLIMES = []
FrozenSlime.addToGroup(FROZENSLIMES)

FROZENWOLVES = []
FrozenWolf.addToGroup(FROZENWOLVES)
