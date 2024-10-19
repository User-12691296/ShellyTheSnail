from .swords import Sword
from ...projectiles import PROJECTILE_CLASSES
from misc import animations
import math

SWING_FRAMES = 10

class SigWeapon(Sword):

    def __init__(self, itemid, tex_name, damage, size, swing_angle=60, swing_range=None, player_damage_on_hit=0, amount_of_projectiles=16, laser = PROJECTILE_CLASSES.CrystalMaceProj, cooldown=0):
        super().__init__(itemid, tex_name, damage, size, swing_angle, swing_range, player_damage_on_hit)

        self.angles = []
        self.amount_of_projectiles = amount_of_projectiles

        for i in range (self.amount_of_projectiles):
            self.angles.append((360/self.amount_of_projectiles)*i)

        self.laser = laser
        self.cooldown = cooldown

    def onLeft(self, data, player, world, tile_pos, tile):
        super().onLeft(data, player, world, tile_pos, tile)
    
        if not data["animations"].exists("cooldown"):
            for angle in self.angles:
                laser = self.laser(player.pos, -data["rot"] + angle)
                laser.giveImmunity(player)
                world.addProjectile(laser)
            data["animations"].create("cooldown", self.cooldown)
                                    
SIGWEAPONS = []
SigWeapon("clawofcrabking", "clawofcrabking", 35, 2, 360, laser=PROJECTILE_CLASSES.ScissorBullet, cooldown=20).addToGroup(SIGWEAPONS)
SigWeapon("clawofsnakequeen", "clawofsnakequeen", 35, 2, 360, laser=PROJECTILE_CLASSES.PoisonDart, cooldown=20).addToGroup(SIGWEAPONS)
SigWeapon("scissors", "scissors", 35,2,360,laser=PROJECTILE_CLASSES.ScissorBullet,cooldown=20).addToGroup(SIGWEAPONS)
