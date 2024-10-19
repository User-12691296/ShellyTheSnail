import pygame

from ..classes import Enemy
from ...projectiles import PROJECTILE_CLASSES

class DarknessGhost(Enemy):
    def __init__(self):
        super().__init__(4, 0, 50)

    @staticmethod
    def getNeededAssets():
        return ["darknessghost"]

    def isEnemy(self):
        return True

    def damageTick(self):
        if self.world.player.diagonalTo(self.pos) <= 8 and not self.isCooldownActive("laser"):
            laser = PROJECTILE_CLASSES.DarknessBullet.fromStartEnd(self.pos, self.world.player.getPos())
            laser.giveImmunity(self)
            self.world.addProjectile(laser)
            self.registerCooldown("laser", 50)
            
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.4)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("darknessghost")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class DarknessGraveTrapper(Enemy):
    def __init__(self):
        super().__init__(6, 0, 45)

    @staticmethod
    def getNeededAssets():
        return ["darknessgravetrapper"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.5)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("darknessgravetrapper")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class DarknessJumpscare(Enemy):
    def __init__(self):
        super().__init__(4, 0, 30)

    @staticmethod
    def getNeededAssets():
        return ["darknessjumpscare"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(2)
                self.damage(30)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("darknessjumpscare")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class DarknessKnightmare1(Enemy):
    def __init__(self):
        super().__init__(4, 0, 40)

    @staticmethod
    def getNeededAssets():
        return ["darknessknightmare1"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.2)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("darknessknightmare1")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class DarknessKnightmare2(Enemy):
    def __init__(self):
        super().__init__(4, 0, 40)

    @staticmethod
    def getNeededAssets():
        return ["darknessknightmare2"]

    def isEnemy(self):
        return True

    def damageTick(self):
        if self.world.player.diagonalTo(self.pos) <= 8 and not self.isCooldownActive("laser"):
            laser = PROJECTILE_CLASSES.DarknessBullet.fromStartEnd(self.pos, self.world.player.getPos())
            laser.giveImmunity(self)
            self.world.addProjectile(laser)
            self.registerCooldown("laser", 50)
            
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.25)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("darknessknightmare2")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class DarknessSpreader(Enemy):
    def __init__(self):
        super().__init__(5, 0, 50)

    @staticmethod
    def getNeededAssets():
        return ["darknessspreader"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.25)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("darknessspreader")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class DarknessBat(Enemy):
    def __init__(self):
        super().__init__(4, 0, 30)

    @staticmethod
    def getNeededAssets():
        return ["darknessbat"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.2)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("darknessbat")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)


# Add crystal enemies to a group of enemies
DARKNESSGHOSTS = []
DarknessGhost.addToGroup(DARKNESSGHOSTS)

DARKNESSGRAVETRAPPERS = []
DarknessGraveTrapper.addToGroup(DARKNESSGRAVETRAPPERS)

DARKNESSJUMPSCARES = []
DarknessJumpscare.addToGroup(DARKNESSJUMPSCARES)

DARKNESSKNIGHTMARE1 = []
DarknessKnightmare1.addToGroup(DARKNESSKNIGHTMARE1)

DARKNESSKNIGHTMARE2 = []
DarknessKnightmare2.addToGroup(DARKNESSKNIGHTMARE2)

DARKNESSSPREADERS = []
DarknessSpreader.addToGroup(DARKNESSSPREADERS)

DARKNESSBATS = []
DarknessBat.addToGroup(DARKNESSBATS)
