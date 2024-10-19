##from .guns import Gun
##from ...projectiles import PROJECTILE_CLASSES
##from misc import animations
##import math
##
##SWING_FRAMES = 10
##
##class SoulCannon(Gun):
##    
##    def fire(self, data, player, world, tile_pos, tile):
##        soul_blast = PROJECTILE_CLASSES.SoulBlast(player.pos, -data["rot"]-45)
##        soul_blast.giveImmunity(player)
##        world.addProjectile(soul_blast)
##        
##    def onLeft(self, data, player, world, tile_pos, tile):
##        self.fire(data, player, world, tile_pos, tile)
##        return True
##
##
##SOULCANNON = []
##SoulCannon("debug_sword", "sword", 1).addToGroup(SOULCANNON)
##SoulCannon("soul_cannon", "soul_cannon", 1).addToGroup(SOULCANNON)
##
