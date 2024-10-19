import pygame

from ..classes import Enemy
from ...projectiles import PROJECTILE_CLASSES


class Slime(Enemy):
    def __init__(self):
        super().__init__(5, 3, 30)

    @staticmethod
    def getNeededAssets():
        return ["slime"]

    def damageTick(self):
        if self.world.player.diagonalTo(self.pos) <= 8 and not self.isCooldownActive("lasershot"):
            lasershot = PROJECTILE_CLASSES.CrystalLaserShot.fromStartEnd(self.pos, self.world.player.getPos())
            lasershot.giveImmunity(self)
            self.world.addProjectile(lasershot)
            self.registerCooldown("lasershot", 60)
            
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if entity.isEnemyTarget():
                entity.damage(0.1)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("slime")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)


SLIMES = []
Slime.addToGroup(SLIMES)
