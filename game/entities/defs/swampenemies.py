import pygame

from ..classes import Enemy
from ...projectiles import PROJECTILE_CLASSES

class SwampAnaconda(Enemy):
    def __init__(self):
        super().__init__(5, 0, 35)

    @staticmethod
    def getNeededAssets():
        return ["swampanaconda"]

    def isEnemy(self):
        return True

    def damageTick(self):
        if self.world.player.diagonalTo(self.pos) <= 8 and not self.isCooldownActive("poisondart"):
            poisondart = PROJECTILE_CLASSES.PoisonDart.fromStartEnd(self.pos, self.world.player.getPos())
            poisondart.giveImmunity(self)
            self.world.addProjectile(poisondart)
            self.registerCooldown("poisondart", 20)
            
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if entity.isEnemyTarget():
                entity.damage(0.15)
                

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("swampanaconda")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class SwampOtter(Enemy):
    def __init__(self):
        super().__init__(4, 0, 25)

    @staticmethod
    def getNeededAssets():
        return ["swampotter"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.2)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("swampotter")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class SwampTangler(Enemy):
    def __init__(self):
        super().__init__(4, 0, 30)

    @staticmethod
    def getNeededAssets():
        return ["swamptangler"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.2)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("swamptangler")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class SwampSlime(Enemy):
    def __init__(self):
        super().__init__(6, 0, 20)

    @staticmethod
    def getNeededAssets():
        return ["swampslime"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(1)
                self.damage(20)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("swampslime")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)


# Add crystal enemies to a group of enemies
SWAMPANACONDAS = []
SwampAnaconda.addToGroup(SWAMPANACONDAS)

SWAMPOTTERS = []
SwampOtter.addToGroup(SWAMPOTTERS)

SWAMPTANGLERS = []
SwampTangler.addToGroup(SWAMPTANGLERS)

SWAMPSLIMES = []
SwampSlime.addToGroup(SWAMPSLIMES)
