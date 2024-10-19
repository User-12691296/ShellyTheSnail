from .swords import Sword
from ...projectiles import PROJECTILE_CLASSES
from misc import animations
import math

SWING_FRAMES = 10

class Mace(Sword):

    def __init__(self, itemid, tex_name, damage, size, swing_angle=60, swing_range=None, player_damage_on_hit=0, amount_of_projectiles=8, laser = PROJECTILE_CLASSES.CrystalLaserShot, cooldown=0):
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
                                    
MACES = []
Mace("debug_sword", "sword", 1000, 2).addToGroup(MACES)
Mace("wood_mace", "wood_mace", 10, 0, 300, 5, cooldown=20).addToGroup(MACES)
Mace("stone_mace", "stone_mace", 10, 0, 300, 5, cooldown=10).addToGroup(MACES)
Mace("kr1stal_mace", "kr1stal_mace", 6, 1, 300, 5, cooldown=5, amount_of_projectiles=8, laser=PROJECTILE_CLASSES.CrystalMaceProj).addToGroup(MACES)
Mace("lava_mace", "lava_mace", 15, 1, 300, 5, amount_of_projectiles=20,cooldown=5, laser=PROJECTILE_CLASSES.MoltenMaceProj).addToGroup(MACES)
Mace("celestial_mace", "celestial_mace", 15, 2, 300, 5,cooldown=5, amount_of_projectiles=16, laser=PROJECTILE_CLASSES.CelestialMaceProj).addToGroup(MACES)
Mace("cosmic_mace", "cosmic_mace", 15, 2, 300, 5, cooldown=7,amount_of_projectiles=12, laser=PROJECTILE_CLASSES.DarknessMaceProj).addToGroup(MACES) #cosmic = darkness
Mace("snake_mace", "snake_mace", 15, 2, 300,5,cooldown=5, amount_of_projectiles=8,laser=PROJECTILE_CLASSES.PoisonDart).addToGroup(MACES) 

