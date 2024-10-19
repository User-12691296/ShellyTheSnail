from ..classes import Item
from ...projectiles import PROJECTILE_CLASSES
from misc import animations
import math

SWING_FRAMES = 10

class Gun(Item):
    def __init__(self, itemid, tex_name, size, cooldown, bullet = PROJECTILE_CLASSES.Pizza):
        super().__init__(itemid, tex_name, False, size)
        self.bullet=bullet
        self.cooldown = cooldown

    def tick(self, data, player, world):
        data["animations"].tick()

    def damageTick(self, data, player, world):
        # Handle Swing
        data["rot"] = -(player.getFacing()+90)
        data["rot"] = data["rot"] % 360

    def fireInTheHole(self, data, player, world, tile_pos, tile):
        if not data["animations"].exists("cooldown"):
            bullet = self.bullet(player.pos, -data["rot"]-45)
            bullet.giveImmunity(player)
            world.addProjectile(bullet)
            data["animations"].create("cooldown", self.cooldown)
        
    def onLeft(self, data, player, world, tile_pos, tile):
        self.fireInTheHole(data, player, world, tile_pos, tile)
        return True


GUNS = []
Gun("pizza_gun", "pizza_gun", 1, 10).addToGroup(GUNS)
Gun("soul_cannon", "soul_cannon", 1, 15, bullet=PROJECTILE_CLASSES.SoulBlast).addToGroup(GUNS)
Gun("crystal_raygun", "crystal_raygun", 2, 15, bullet=PROJECTILE_CLASSES.CrystalMaceProj).addToGroup(GUNS)
Gun("cold_barrel_gun", "cold_barrel_gun", 2, 15, bullet=PROJECTILE_CLASSES.ColdDoug).addToGroup(GUNS)
Gun("thunder_cannon", "thunder_cannon", 1, 15, bullet=PROJECTILE_CLASSES.ThunderSpark).addToGroup(GUNS)
Gun("barrel_of_doug", "barrel_of_doug", 2, 15, bullet=PROJECTILE_CLASSES.FrogBullet).addToGroup(GUNS)
Gun("dart_gun", "dart_gun", 0, 15, bullet=PROJECTILE_CLASSES.DartProjectile).addToGroup(GUNS)
Gun("cannon", "cannon", 0, 120, bullet=PROJECTILE_CLASSES.CannonBall).addToGroup(GUNS)

