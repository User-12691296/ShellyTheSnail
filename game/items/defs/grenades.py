from ..classes import Item
from misc import animations
import math
import pygame

class Bomb(Item):
    def __init__(self):
        super().__init__("bomb", "crystal_geode", True, 0)

        self.damage = 50
        self.range = 10

    def initData(self, stack):
        data = super().initData(stack)
        
        data["detonated"] = False

        return data
    
    def tick(self, data, player, world):
        data["animations"].tick()

    def ignite(self, data, player, world, tile_pos, tile):
        data["animations"].create("explosion_progress", 18, lambda: self.markForDetonation(data))

    def markForDetonation(self, data):
        data["detonated"] = True

    def damageTick(self, data, player, world):
        if data["detonated"]:
            self.detonate(data, player, world, player.pos, world.getTileID(player.pos))
            
    def detonate(self, data, player, world, tile_pos, tile):
        for entity in world.getEntitiesInRangeOfTile(tile_pos, self.range):
            if not entity.isPlayer():
                entity.damage(self.damage)

        data["stack"].consume()
        data["detonated"] = False
    
    def onLeft(self, data, player, world, tile_pos, tile):
        self.ignite(data, player, world, tile_pos, tile)
        return True

    def drawInWorld(self, data, surface, center):
        super().drawInWorld(data, surface, center)

        if data["animations"].exists("explosion_progress"):
            pygame.draw.circle(surface, (255, 255, 255), (surface.get_width()//2, surface.get_height()//2), data["animations"].getFrame("explosion_progress")**2*2)

class Dynamite(Item):
    #make this track light colour tiles and reveal something?
    def __init__(self):
        super().__init__("dynamite", "dynamite", True, 0)

        self.damage = 20
        self.range = 10

    def initData(self, stack):
        data = super().initData(stack)
        
        data["detonated"] = False

        return data
    
    def tick(self, data, player, world):
        data["animations"].tick()

    def ignite(self, data, player, world, tile_pos, tile):
        data["animations"].create("explosion_progress", 18, lambda: self.markForDetonation(data))

    def markForDetonation(self, data):
        data["detonated"] = True

    def damageTick(self, data, player, world):
        if data["detonated"]:
            self.detonate(data, player, world, player.pos, world.getTileID(player.pos))
            
    def detonate(self, data, player, world, tile_pos, tile):
        for entity in world.getEntitiesInRangeOfTile(tile_pos, self.range):
            if not entity.isPlayer():
                entity.damage(self.damage)
        for i in range(tile_pos[0]-self.range, tile_pos[0]+self.range):
            for j in range (tile_pos[1]-self.range, tile_pos[1]+self.range):
                if world.getTileID((i,j)) == "lobbywall":
                    world.setTileID((i,j), "lobbyfloor")
                    world.setTileElevation((i,j), 0)

        data["stack"].consume()
        data["detonated"] = False
    
    def onLeft(self, data, player, world, tile_pos, tile):
        self.ignite(data, player, world, tile_pos, tile)
        return True

    def drawInWorld(self, data, surface, center):
        super().drawInWorld(data, surface, center)

        if data["animations"].exists("explosion_progress"):
            pygame.draw.circle(surface, (255, 255, 255), (surface.get_width()//2, surface.get_height()//2), data["animations"].getFrame("explosion_progress")**2*2)
        
GRENADES = []
Bomb().addToGroup(GRENADES)
Dynamite().addToGroup(GRENADES)
