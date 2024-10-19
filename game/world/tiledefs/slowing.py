from .basic import BasicTile
from constants import GAME

class SlowTile(BasicTile):
    def __init__(self, tileid, tex_name, slow_value, rscat=True):
        super().__init__(tileid, tex_name, rscat)
        
        self.slow_value = slow_value
        
    def onWalk(self, world, tile_pos):
        player = world.getPlayer()
                
        player.setMovementSpeed(GAME.PLAYER_WALKING_SPEED*self.slow_value)
        player.giveEffect("slow", 5, lambda x, y, z:None, lambda x, y, z: player.setMovementSpeed(GAME.PLAYER_WALKING_SPEED))
