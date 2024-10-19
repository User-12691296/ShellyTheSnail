import pygame

from ..classes import Enemy
from ...projectiles import PROJECTILE_CLASSES


class DessertKnight(Enemy):
    def __init__(self):
        super().__init__(6, 0, 40)

    @staticmethod
    def getNeededAssets():
        return ["dessertknight"]

    def isEnemy(self):
        return True

    def damageTick(self):
        if self.world.player.diagonalTo(self.pos) <= 8 and not self.isCooldownActive("laser"):
            laser = PROJECTILE_CLASSES.DesertBullet.fromStartEnd(self.pos, self.world.player.getPos())
            laser.giveImmunity(self)
            self.world.addProjectile(laser)
            self.registerCooldown("laser", 40)
            
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.15)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("dessertknight")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class DessertRaider(Enemy):
    def __init__(self):
        super().__init__(4, 0, 35)

    @staticmethod
    def getNeededAssets():
        return ["dessertraider"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.2)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("dessertraider")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class DessertSandWurm(Enemy):
    def __init__(self):
        super().__init__(3, 0, 15)

    @staticmethod
    def getNeededAssets():
        return ["dessertsandwurm"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.5)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("dessertsandwurm")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class DessertSlime(Enemy):
    def __init__(self):
        super().__init__(5, 0, 45)

    @staticmethod
    def getNeededAssets():
        return ["dessertslime"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.2)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("dessertslime")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)


# Add crystal enemies to a group of enemies
DESSERTKNIGHTS = []
DessertKnight.addToGroup(DESSERTKNIGHTS)

DESSERTRAIDERS = []
DessertRaider.addToGroup(DESSERTRAIDERS)

DESSERTSANDWURMS = []
DessertSandWurm.addToGroup(DESSERTSANDWURMS)

DESSERTSLIMES = []
DessertSlime.addToGroup(DESSERTSLIMES)
