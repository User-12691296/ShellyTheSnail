import pygame
import numpy as np
import random
import os
import json
import math

from constants import ASSETS, GAME
from misc import events
from .fovcalcs import FOVCalculator
from misc.textures import TextureAtlas

from ..tilegroups import GROUP_MANAGER, SPAWNING_REGISTRY

from ...entities import *

DEFAULT_WORLD = "overworld"

class Map:
    class MAP_TILES_TEXTURE_PRESETS:
        FOLDER  = os.path.join(ASSETS.GAME_PATH, "tiles")
        SIZE    = GAME.TILE_SIZE
        EXT     = ".png"
        RESCALE = True

    CORNER_ROUNDING_ELEV_DELTA = GAME.CORNER_ROUNDING_ELEV_DELTA
        
    def __init__(self, map_size, tile_size):
        self.map_size = map_size
        self.tile_size = tile_size
        self.total_size = (map_size[0]*tile_size[0], map_size[1]*tile_size[1])
        self.initFOV()
        self.initBuffers()

        self.tileAtlas = TextureAtlas.fromPreset(self.MAP_TILES_TEXTURE_PRESETS)
        self.default_tile = self.tileAtlas.default
        
    def initFOV(self):
        self.shown_tiles = np.empty((self.map_size[1], self.map_size[0]), dtype=np.int8)

        self.fov_calc = FOVCalculator(self.map_size, self.shown_tiles)

    def initBuffers(self):
        self.FULL_SIZE_BUFFERS = (self.total_size[0]//GAME.MAX_BUFFER_SIZE[0],
                                self.total_size[1]//GAME.MAX_BUFFER_SIZE[1])

        right_edge_buffer_width = self.total_size[0]%GAME.MAX_BUFFER_SIZE[0]
        bottom_edge_buffer_height = self.total_size[1]%GAME.MAX_BUFFER_SIZE[1]

        # Put > 0 for buffer loading just in case the dimensions are multiples of 16 
        self.MAX_BUFFERS = (self.FULL_SIZE_BUFFERS[0] + (1 if right_edge_buffer_width > 0 else 0),
                            self.FULL_SIZE_BUFFERS[1] + (1 if bottom_edge_buffer_height > 0 else 0))
        
        self.loaded_buffers = np.empty((self.MAX_BUFFERS[1], self.MAX_BUFFERS[0]), dtype="bool")

        self.buffers = {}

        self.buffers_used_this_frame = []

    def getBufferSize(self, buffer_loc):
        right_edge_buffer_width = self.total_size[0]%GAME.MAX_BUFFER_SIZE[0]
        bottom_edge_buffer_height = self.total_size[1]%GAME.MAX_BUFFER_SIZE[1]
        
        if buffer_loc[0] < self.MAX_BUFFERS[0]:
            width = GAME.MAX_BUFFER_SIZE[0]

        if buffer_loc[0] == self.MAX_BUFFERS[0]:
            width = right_edge_buffer_width

        if buffer_loc[1] < self.MAX_BUFFERS[1]:
            height = GAME.MAX_BUFFER_SIZE[1]

        if buffer_loc[1] == self.MAX_BUFFERS[1]:
            height = bottom_edge_buffer_height

        return (width, height)
        
    def loadBuffer(self, buffer_loc):
        # Cleaning input data
        buffer_loc = tuple(buffer_loc)

        # Gathering data about buffer
        topleft = self.bufferLocToVirtualPos(buffer_loc)
        tile_topleft = (topleft[0]//self.tile_size[0], topleft[1]//self.tile_size[1])
        
        size = self.getBufferSize(buffer_loc)
        size_tiles = (size[0]//self.tile_size[0], size[1]//self.tile_size[1])
        
        # Build buffer and draw tiles to it
        self.buffers[buffer_loc] = pygame.Surface(size)

        for x in range(tile_topleft[0], tile_topleft[0]+size_tiles[0]):
            for y in range(tile_topleft[1], tile_topleft[1]+size_tiles[1]):
                self.regenTile((x, y))
        
        self.loaded_buffers[buffer_loc[1]][buffer_loc[0]] = True

    def startBufferGC(self):
        self.buffers_used_this_frame = []

    def markBufferUsed(self, buffer_loc):
        self.buffers_used_this_frame.append(buffer_loc)

    def bufferGC(self):
        loaded_buffers = (*self.buffers.keys(),)
        for buffer_loc in loaded_buffers:
            if not buffer_loc in self.buffers_used_this_frame:
                self.unloadBuffer(buffer_loc)

    def unloadBuffer(self, buffer_loc):
        self.loaded_buffers[buffer_loc[1]][buffer_loc[0]] = False

        del self.buffers[buffer_loc]

    def getBufferAtLoc(self, buffer_loc):
        return self.buffers.get(buffer_loc, None)

    def getBufferLoadIfUnloaded(self, buffer_loc):
        buffer = self.getBufferAtLoc(buffer_loc)

        self.markBufferUsed(buffer_loc)

        if buffer != None:
            return buffer

        else:
            self.loadBuffer(buffer_loc)
            return self.getBufferAtLoc(buffer_loc)

    def bufferLocToVirtualPos(self, buffer_loc):
        return (GAME.MAX_BUFFER_SIZE[0]*buffer_loc[0],
                GAME.MAX_BUFFER_SIZE[1]*buffer_loc[1])

    def getRelevantBuffers(self, rect):
        # Keep errant inputs within bounds
        clamp = lambda x, mn, mx: mn if x < mn else mx if x > mx else x
        
        left_bound = clamp(rect.left//GAME.MAX_BUFFER_SIZE[0], 0, self.MAX_BUFFERS[0]-1)
        right_bound = clamp(-(rect.right//-GAME.MAX_BUFFER_SIZE[0]), 0, self.MAX_BUFFERS[0]-1) # Ceil div
        top_bound = clamp(rect.top//GAME.MAX_BUFFER_SIZE[1], 0, self.MAX_BUFFERS[1]-1)
        bottom_bound = clamp(-(rect.bottom//-GAME.MAX_BUFFER_SIZE[1]), 0, self.MAX_BUFFERS[1]-1)

        relevant_buffers = [(x, y)
                            for x in range(left_bound, right_bound+1)
                            for y in range(top_bound, bottom_bound+1)]

        
        return relevant_buffers

    def getRelevantTilesAsRect(self, rect):
        clamp = lambda x, mn, mx: mn if x < mn else mx if x > mx else x
        
        left_bound = clamp(rect.left//self.tile_size[0], 0, self.map_size[0])
        right_bound = clamp(-(rect.right//-self.tile_size[0]), 0, self.map_size[0]) # Ceil div
        top_bound = clamp(rect.top//self.tile_size[1], 0, self.map_size[1])
        bottom_bound = clamp(-(rect.bottom//-self.tile_size[1]), 0, self.map_size[1])

        relevant_tiles = pygame.Rect(left_bound, top_bound, right_bound-left_bound, bottom_bound-top_bound)
        
        return relevant_tiles

    def blit(self, source, dest):
        rect = source.get_rect()
        rect.topleft = dest

        relevant_buffers = self.getRelevantBuffers(rect)

        for buffer_loc in relevant_buffers:
            delta = self.bufferLocToVirtualPos(buffer_loc)

            buffer = self.getBufferAtLoc(buffer_loc)

            if buffer != None:
                buffer.blit(source, (dest[0]-delta[0], dest[1]-delta[1]))
        
    def setWorld(self, world):
        self.world = world

##    def getMap(self):
##        return self.buffer

    def bindTileAtlas(self, tile_class):
        tile_class.setAtlas(self.tileAtlas)

    def regenTile(self, tile_pos):
        getTile = lambda x, y: self.world.getTile((tile_pos[0]+x, tile_pos[1]+y))
        tile = getTile(0, 0)

        tbd = tile.getDrawable().copy()

        if tile.shouldRotationScatter():
            flip_key = (math.cos(((math.sin(tile_pos[0]*12.9898 + tile_pos[1]*78.233)*6.71432)**2)//1)*1.97+2)//1
            if flip_key == 1:
                tbd = pygame.transform.rotate(tbd, 90)
            if flip_key == 2:
                tbd = pygame.transform.rotate(tbd, 180)
            if flip_key == 3:
                tbd = pygame.transform.rotate(tbd, 270)
        
        shading = pygame.Surface(tbd.get_rect().size, pygame.SRCALPHA)
        shading.fill(255)
        
        getElev = lambda x, y: self.world.getTileElevation((tile_pos[0]+x, tile_pos[1]+y))
        deltaElev = lambda x, y: getElev(0, 0)-getElev(x, y)
        minElevDeltaOnCorner = lambda x, y: min((deltaElev(x, 0), deltaElev(x, y), deltaElev(0, y)))
        maxElevDeltaOnCorner = lambda x, y: max((deltaElev(x, 0), deltaElev(x, y), deltaElev(0, y)))

        rounding_pixel_size = (self.tile_size[0]//GAME.TILE_RESOLUTION, self.tile_size[1]//GAME.TILE_RESOLUTION)
        # Corner shading, if elevation is high then round corner
        # Topleft corner
        if minElevDeltaOnCorner(-1, -1) > self.CORNER_ROUNDING_ELEV_DELTA or maxElevDeltaOnCorner(-1, -1) < -self.CORNER_ROUNDING_ELEV_DELTA:
            left_col = getTile(-1, 0).getDrawable().get_at((self.tile_size[0]-1, rounding_pixel_size[1]))
            corn_col = getTile(-1, -1).getDrawable().get_at((self.tile_size[0]-1, self.tile_size[1]-1))
            top_col  = getTile(0, -1).getDrawable().get_at((rounding_pixel_size[0], self.tile_size[1]-1))

            pygame.draw.rect(tbd, left_col, pygame.Rect((0, rounding_pixel_size[1]), rounding_pixel_size))
            pygame.draw.rect(tbd, corn_col, pygame.Rect((0, 0), rounding_pixel_size))
            pygame.draw.rect(tbd, top_col, pygame.Rect((rounding_pixel_size[0], 0), rounding_pixel_size))

        # Topright
        if minElevDeltaOnCorner(1, -1) > self.CORNER_ROUNDING_ELEV_DELTA or maxElevDeltaOnCorner(1, -1) < -self.CORNER_ROUNDING_ELEV_DELTA:
            right_col = getTile(1, 0).getDrawable().get_at((0, self.tile_size[1]-rounding_pixel_size[1]))
            corn_col = getTile(1, -1).getDrawable().get_at((0, self.tile_size[1]-1))
            top_col  = getTile(0, -1).getDrawable().get_at((self.tile_size[0]-rounding_pixel_size[0], self.tile_size[1]-1))

            pygame.draw.rect(tbd, right_col, pygame.Rect((self.tile_size[0]-rounding_pixel_size[0], rounding_pixel_size[1]), rounding_pixel_size))
            pygame.draw.rect(tbd, corn_col, pygame.Rect((self.tile_size[0]-rounding_pixel_size[0], 0), rounding_pixel_size))
            pygame.draw.rect(tbd, top_col, pygame.Rect((self.tile_size[0]-rounding_pixel_size[0]*2, 0), rounding_pixel_size))

        # Bottomright
        if minElevDeltaOnCorner(1, 1) > self.CORNER_ROUNDING_ELEV_DELTA or maxElevDeltaOnCorner(1, 1) < -self.CORNER_ROUNDING_ELEV_DELTA:
            right_col = getTile(1, 0).getDrawable().get_at((0, self.tile_size[1]-rounding_pixel_size[1]))
            corn_col = getTile(1, 1).getDrawable().get_at((0, 0))
            bot_col  = getTile(0, 1).getDrawable().get_at((self.tile_size[0]-rounding_pixel_size[0], 0))

            pygame.draw.rect(tbd, right_col, pygame.Rect((self.tile_size[0]-rounding_pixel_size[0], self.tile_size[1]-rounding_pixel_size[1]*2), rounding_pixel_size))
            pygame.draw.rect(tbd, corn_col, pygame.Rect((self.tile_size[0]-rounding_pixel_size[0], self.tile_size[1]-rounding_pixel_size[1]), rounding_pixel_size))
            pygame.draw.rect(tbd, bot_col, pygame.Rect((self.tile_size[0]-rounding_pixel_size[0]*2, self.tile_size[1]-rounding_pixel_size[1]), rounding_pixel_size))

        # Bottomleft
        if minElevDeltaOnCorner(-1, 1) > self.CORNER_ROUNDING_ELEV_DELTA or maxElevDeltaOnCorner(-1, 1) < -self.CORNER_ROUNDING_ELEV_DELTA:
            left_col = getTile(-1, 0).getDrawable().get_at((self.tile_size[0]-1, rounding_pixel_size[1]))
            corn_col = getTile(-1, 1).getDrawable().get_at((self.tile_size[0]-1, 0))
            bot_col  = getTile(0, 1).getDrawable().get_at((self.tile_size[0]-rounding_pixel_size[0], 0))

            pygame.draw.rect(tbd, left_col, pygame.Rect((0, self.tile_size[1]-rounding_pixel_size[1]*2), rounding_pixel_size))
            pygame.draw.rect(tbd, corn_col, pygame.Rect((0, self.tile_size[1]-rounding_pixel_size[1]), rounding_pixel_size))
            pygame.draw.rect(tbd, bot_col, pygame.Rect((rounding_pixel_size[0], self.tile_size[1]-rounding_pixel_size[1]), rounding_pixel_size))
        
        self.blit(tbd, self.world.tilePosToBufferPos(tile_pos))

    def calcFOV(self, origin, range=None):
        if range:
            self.fov_calc.setRange(range)
        self.fov_calc.genOpaquesFromElevCutoff(self.world.world_tile_elevations, self.world.OPAQUE_TILE_ELEV_DELTA)
        self.fov_calc.calcFOV(origin)

    def drawMap(self, surface, visible_rect, screen_rect=None):
        self.startBufferGC()

        area_visible = pygame.Rect((-visible_rect.left, -visible_rect.top),
                                                               visible_rect.size)
        if screen_rect:
            area_visible.left = -screen_rect.left
            area_visible.top = -screen_rect.top
            
        relevant_buffers = self.getRelevantBuffers(area_visible)
                    
        for buffer_loc in relevant_buffers:
            v_pos = self.bufferLocToVirtualPos(buffer_loc)

            buffer = self.getBufferLoadIfUnloaded(buffer_loc)

            if buffer != None:
                surface.blit(self.getBufferLoadIfUnloaded(buffer_loc),
                                 (visible_rect.left+v_pos[0], visible_rect.top+v_pos[1]))

        self.bufferGC()

    def occlude(self, surface, visible_rect, screen_rect=None):
        area_visible = pygame.Rect((-visible_rect.left, -visible_rect.top),
                                                               visible_rect.size)
        if screen_rect:
            area_visible.left = -screen_rect.left
            area_visible.top = -screen_rect.top

        relevant_tiles = self.getRelevantTilesAsRect(area_visible)

        visible_darkness = self.shown_tiles.T[relevant_tiles.left:relevant_tiles.right,
                                            relevant_tiles.top:relevant_tiles.bottom]
        
        edge_darkness = np.array(visible_darkness >= 2, dtype=np.int16)*255

        tile_topleft = self.world.tilePosToBufferPos(relevant_tiles.topleft)
        edge_darkness_delta = [tile_topleft[0]-area_visible.left, tile_topleft[1]-area_visible.top]
        if (relevant_tiles.left<=0 or relevant_tiles.top<=0 or relevant_tiles.right>=self.map_size[0]-1 or relevant_tiles.top>=self.map_size[1]-1):
            edge_darkness = np.pad(edge_darkness, [(1, 1), (1, 1)], mode="constant", constant_values=0)

            edge_darkness_delta[0] -= self.tile_size[0]
            edge_darkness_delta[1] -= self.tile_size[1]
            
        edge_blocking = pygame.surfarray.make_surface(edge_darkness)
        edge_blocking = pygame.transform.scale_by(edge_blocking, self.tile_size)
        edge_blocking.set_colorkey(255)


        center_darkness = np.array(np.absolute(visible_darkness-63) > 62, dtype=np.int16)*255
        
        center_blocking = pygame.surfarray.make_surface(center_darkness)
        center_blocking = pygame.transform.scale_by(center_blocking, self.tile_size)
        center_blocking.set_colorkey(255)

        #print(visible_rect.topleft, area_visible, pos_delta, tile_topleft)
        
        surface.blit(edge_blocking, (edge_darkness_delta))
        surface.blit(center_blocking, (tile_topleft[0] + visible_rect.left, tile_topleft[1] + visible_rect.top))


class World(events.EventAcceptor):
    TILE_SIZE = (GAME.TILE_SIZE, GAME.TILE_SIZE)

    VOID_TILEID = "void"
    ERROR_TILEID = "error"

    OPAQUE_TILE_ELEV_DELTA = GAME.OPAQUE_TILE_ELEV_DELTA
    WALKING_TILE_ELEV_DELTA = GAME.WALKING_TILE_ELEV_DELTA
    
    def __init__(self, tileClasses):
        self.size = (0, 0)
        
        self.loadWorld()

        self.map = Map(self.size, self.TILE_SIZE)
        self.map.setWorld(self)

        self.moving_anim_direction = [0, 0]
        self.moving_anim_delta = [0, 0]
        self.moving_anim_frame_getter = lambda:0

        self.tiles = {}
        for tileClass in tileClasses:
            self.map.bindTileAtlas(tileClass)
            self.tiles[tileClass.getTileID()] = tileClass

        self.entities = []
        self.spawned_entities = [] 

        self.projectiles = []

        self.first_tick = True
        self.changes_this_tick = False

    def loadWorld(self):
        with open("game\\world\\worldefs\\levels.json") as levels_file:
            world = self.__dict__.get("world_name", DEFAULT_WORLD)
            self.loadWorldFromFile(levels_file, world)

    def loadWorldFromFile(self, file, world_name):
        all_worlds = json.load(file)
        world_info = all_worlds[world_name]
        
        self.size = world_info["size"]

        self.loadWorldDataFromDict(world_info['tiles'])

    @staticmethod
    def splitRowDataIntoTileData(row_data, row_length):
        return row_data.split(";")[:row_length]

    @staticmethod
    def splitTileDataIntoTileInfo(tile_data):
        return tile_data.split(",")

    def loadWorldDataFromDict(self, rows):
        self.world_tile_ids = np.empty((self.size[1], self.size[0]), dtype="<U32")
        self.world_tile_elevations = np.empty((self.size[1], self.size[0]), dtype=np.int32)
        default_row = "grass,0;"*self.size[0]
        
        for row_index in range(self.size[1]):
            row_name = str(row_index)

            row_data = rows.get(row_name, default_row)

            tile_data_in_row = self.splitRowDataIntoTileData(row_data, self.size[0])

            for tile_index, tile_data in enumerate(tile_data_in_row):
                tileid, elevation = self.splitTileDataIntoTileInfo(tile_data)

                if tileid == self.ERROR_TILEID:
                    print("Error tile loaded at: ", (tile_index, row_index))
                
                self.world_tile_ids[row_index][tile_index] = tileid
                self.world_tile_elevations[row_index][tile_index] = int(elevation)
                
        self.genOpaquesFromElevCutoff(GAME.WALKING_TILE_ELEV_DELTA)

    def doFixedSpawning(self):
        instructions = SPAWNING_REGISTRY.getFixedSpawningInstructions(self.world_name)

        for inst in instructions:
            self.spawnFromInstruction(inst)

    def spawnFromInstruction(self, inst):
        entity = inst["class"]()
        entity.setPos(inst["loc"])
        self.addEntity(entity)
        
    def setPlayer(self, player):
        self.player = player

    def getPlayer(self):
        return self.player

    def getTileID(self, tile_pos):
        if (tile_pos[0] < 0 or tile_pos[1] < 0):
            return self.VOID_TILEID
        
        try:
            return self.world_tile_ids[tile_pos[1]][tile_pos[0]]
        except IndexError:
            return self.VOID_TILEID

    def getTile(self, tile_pos):
        tileid = self.getTileID(tile_pos)

        return self.tiles[tileid]

    def getGroupsWithTile(self, tile_pos):
        return GROUP_MANAGER.getGroupsWithTile(self.getTileID(tile_pos))

    def getTileExtrasFromGroups(self, tile_pos, extra, default):
        for group in self.getGroupsWithTile(tile_pos):
            yield GROUP_MANAGER.getExtras(GROUP_MANAGER.getGroup(group)).get(extra, default)
    
    def getTileElevation(self, tile_pos, elev=0):
        # If out of bounds, assume 0 elevation. This gives a raised bevel effect to borders
        if tile_pos[0] < 0 or tile_pos[1] < 0:
            return 0
        if tile_pos[0] >= self.size[0] or tile_pos[1] >= self.size[1]:
            return 0
        
        return self.world_tile_elevations[tile_pos[1]][tile_pos[0]] - elev

    def genOpaquesFromElevCutoff(self, cutoff):
        self.opaques = np.array(self.world_tile_elevations > cutoff, dtype=np.int32)

    def getOpaques(self):
        return self.opaques

    def setTileElevation(self, tile_pos, elevation):
        self.world_tile_elevations[tile_pos[1]][tile_pos[0]] = elevation

    def isTileOpaque(self, tile_pos, curelev=0):
        return self.getTileElevation(tile_pos)-curelev > self.OPAQUE_TILE_ELEV_DELTA

    def isTileValidForWalking(self, tile_pos, curelev=0):
        # Inside map
        border_check = (tile_pos[0] >= 0 and tile_pos[1] >= 0) and \
                       (tile_pos[0] < self.size[0] and tile_pos[1] < self.size[1])
        
        # If elevations are valid
        elev_check = (self.getTileElevation(tile_pos) - curelev) <= self.WALKING_TILE_ELEV_DELTA

        # Can't walk over entities
        entity_check = len(self.getEntitiesOnTile(tile_pos)) == 0
        
        return border_check and elev_check and entity_check

    def getTileRect(self, tile_pos):
        rect = pygame.Rect(self.tilePosToBufferPos(tile_pos),
                           self.TILE_SIZE)

        return rect

    def getWidth(self):
        return self.size[0]

    def getHeight(self):
        return self.size[1]

    def updateTile(self, tile_pos):
        self.map.regenTile(tile_pos)

    def updateTilesAroundTile(self, tile_pos):
        for x in range(-1, 2):
            for y in range(-1, 2):
                self.updateTile((tile_pos[0]+x, tile_pos[1]+y))

    def setTileID(self, tile_pos, tile_id):
        if (tile_pos[0] < 0 or tile_pos[1] < 0):
            return None
        
        if not tile_id in self.tiles.keys():
            return None

        try:
            self.world_tile_ids[tile_pos[1]][tile_pos[0]] = tile_id
            self.updateTilesAroundTile(tile_pos)
            self.registerChange()
            
        except IndexError:
            return None

    def getAllEntities(self):
        return self.entities + [self.player]

    def addEntity(self, entity):
        self.entities.append(entity)
        entity.setWorld(self)
        entity.setOpaques(self.opaques)
        entity.onSpawn()

    def killEntity(self, entity):
        self.entities.remove(entity)

    def getEntitiesOnTile(self, tile_pos):
        return [entity for entity in self.getAllEntities() if entity.collidesWith(tile_pos) and entity.active]

    def getEntitiesInRangeOfTile(self, tile_pos, range):
        r = int(range**2)
        
        return [entity for entity in self.getAllEntities() if entity.distanceTo2(tile_pos) <= r]

    def getEntitiesInDiagToTile(self, tile_pos, range):
        return [entity for entity in self.getAllEntities() if entity.diagonalTo(tile_pos) <= range]

    def getTickableEntities(self):
        return [entity for entity in self.entities if entity.distanceTo2(self.player.pos) <= 400 or entity.isFinalBoss()]

    def addProjectile(self, projectile):
        self.projectiles.append(projectile)
        projectile.setWorld(self)

    def killProjectile(self, projectile):
        self.projectiles.remove(projectile)
        
    def registerChange(self):
        self.changes_this_tick = True
    
    def cullOutOfRangeSpawns(self):
        for spawn in self.spawned_entities:
            if spawn.distanceTo2(self.player.pos) > 400:
                self.spawned_entities.remove(spawn)
                try:
                    self.entities.remove(spawn)
                except ValueError:
                    pass
    
    def wipeSpawns(self):
        for spawn in self.spawned_entities:
            self.entities.remove(spawn)
        self.spawned_entities = []

    def tick(self):
        self.genOpaquesFromElevCutoff(GAME.WALKING_TILE_ELEV_DELTA)
        
        for entity in self.getTickableEntities():
            entity.setOpaques(self.opaques)
            entity.tick()

        for projectile in self.projectiles:
            projectile.tick()

         # debug spawning
        spawns = len(self.spawned_entities)

        if spawns < 15:
            spawn_poll = random.random()
            if spawn_poll > 0.95:
                entities = SPAWNING_REGISTRY.getBiomeSpawn(self.getBiomeAtTile(self.player.pos), self.world_name, 2)
                for entity in entities:
                    ppos = self.player.pos
                    x = ppos[0] + random.randrange(-15, 15)
                    y = ppos[1] + random.randrange(-15, 15)

                    if (0 <= x < self.size[0]) and (0 <= y < self.size[1]):
                        entity = entity()
                        entity.setPos((x, y))
                        self.addEntity(entity)
                        self.spawned_entities.append(entity)
        

        self.changes_this_tick = self.first_tick

        self.moving_anim_delta = [0, 0]

    def getBiomeAtTile(self, player_pos):
        if "crystal" in self.getGroupsWithTile(player_pos): 
            return "crystal"

        elif "swamp" in self.getGroupsWithTile(player_pos): 
            return "swamp"

        elif ("desert" in self.getGroupsWithTile(player_pos) or 
        "cooldesert" in self.getGroupsWithTile(player_pos) or 
        "hotdesert" in self.getGroupsWithTile(player_pos) or 
        "volcano" in self.getGroupsWithTile(player_pos)):
            return "desert"

        elif "mountain" in self.getGroupsWithTile(player_pos): 
            return "mountain"

        elif "arctic" in self.getGroupsWithTile(player_pos): 
            return "arctic"

        elif "deepdark" in self.getGroupsWithTile(player_pos): 
            return "deepdark"

        elif "void" in self.getGroupsWithTile(player_pos): 
            return "void"

    def movementTick(self):
        for entity in self.getTickableEntities():
            entity.movementTick()

        for projectile in self.projectiles:
            projectile.movementTick()

        self.getTile(self.player.getPos()).onWalk(self, self.player.getPos())

        if self.changes_this_tick:
            self.map.calcFOV((int(self.getPlayer().pos[0]), int(self.getPlayer().pos[1])), self.getPlayer().getVisionRange())

    def damageTick(self):
        for entity in self.getTickableEntities():
            entity.damageTick()

        for projectile in self.projectiles:
            projectile.damageTick()
    
    def finalTick(self):
        for entity in self.getTickableEntities():
            entity.finalTick()

        for projectile in self.projectiles:
            projectile.finalTick()

        self.cullDeadEntities()
        self.cullDeadProjectiles()
        self.cullOutOfRangeSpawns()

        if GAME.SMOOTH_PLAYER_MOTION:
            self.updateMovingAnimation()

        if self.first_tick:
            self.doFixedSpawning()
            self.first_tick = False

    def cullDeadEntities(self):
        self.entities = [entity for entity in self.entities if entity.isAlive()]

    def cullDeadProjectiles(self):
        self.projectiles = [projectile for projectile in self.projectiles if projectile.exists(self.player.getPos())]
        
    def onMouseDown(self, mouse_pos, button):
        world_pos = self.bufferPosToTilePos(mouse_pos)

        clicked_tile = self.getTile(world_pos)

        if clicked_tile != None:
            if button == pygame.BUTTON_LEFT:
                clicked_tile.onLeft(self, world_pos)
                # print(clicked_tile)

            elif button == pygame.BUTTON_RIGHT:
                clicked_tile.onRight(self, world_pos)

    def bufferPosToTilePos(self, bpos):
        return (int(bpos[0]//self.TILE_SIZE[0]), int(bpos[1]//self.TILE_SIZE[1]))
    
    def tilePosToBufferPos(self, tpos):
        return (tpos[0]*self.TILE_SIZE[0], tpos[1]*self.TILE_SIZE[1])

    def tilePosToBufferPosOfCenter(self, tpos):
        return (tpos[0]*self.TILE_SIZE[0] + self.TILE_SIZE[0]//2, tpos[1]*self.TILE_SIZE[1] + self.TILE_SIZE[1]//2)

    def setMovingAnimation(self, direction, get_frame):
        self.moving_anim_direction = direction
        self.moving_anim_frame_getter = get_frame

    def updateMovingAnimation(self):
        frame = self.moving_anim_frame_getter()
        
        self.moving_anim_delta[0] += (self.moving_anim_direction[0]*GAME.TILE_SIZE*frame)//self.player.getMovementSpeed()
        self.moving_anim_delta[1] += (self.moving_anim_direction[1]*GAME.TILE_SIZE*frame)//self.player.getMovementSpeed()

    def draw(self, display, visible_rect):
        # Adjust for smooth motion animation
        world_visible = pygame.Rect(visible_rect)
        world_visible.left += self.moving_anim_delta[0]
        world_visible.top += self.moving_anim_delta[1]

        # Map
        self.map.drawMap(display, world_visible, visible_rect)

        # Projectiles
        for projectile in self.projectiles:
            projectile.draw(display, world_visible.topleft)

        # Entities
        for entity in self.getEntitiesInRangeOfTile(self.player.getPos(), 12):
            if not entity.isPlayer():
                entity.draw(display, world_visible.topleft)

        # FOV
        self.map.occlude(display, world_visible, visible_rect)
