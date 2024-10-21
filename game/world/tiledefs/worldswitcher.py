import pygame
from misc import events
from .basic import BasicTile

FIRST_DUNGEON = False

class WorldSwitcher(BasicTile):
    def __init__(self, tex_name, tileid, world_to_change, world_position, rscat=True):
        super().__init__(tileid, tex_name, rscat)
        self.world_to_change = world_to_change
        self.world_position = world_position

    def onLeft(self, world, tile_pos):
        global FIRST_DUNGEON
        if not FIRST_DUNGEON:
            pygame.event.post(pygame.event.Event(events.RUN_TUTORIAL, stage=2))
            FIRST_DUNGEON = True
        
        world.player.manager.changeWorld(self.world_to_change)
        if self.world_position[0] != 9999:
            world.player.setPos(self.world_position)
