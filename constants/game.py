import os
import pygame

#MAP
TILE_SIZE = 64
TILE_RESOLUTION = 16

MAX_BUFFER_SIZE = (1024, 1024)

CORNER_ROUNDING_ELEV_DELTA = 5
OPAQUE_TILE_ELEV_DELTA = 3
WALKING_TILE_ELEV_DELTA = 2

PLAYER_WALKING_SPEED = 5
SMOOTH_PLAYER_MOTION = True
PLAYER_INVENTORY_SIZE = 25
PLAYER_INVENTORY_WIDTH = 8

ORIGINAL_CONTROLS_KEYS = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "right": pygame.K_d,
    "left": pygame.K_a,
    "throw": pygame.K_t,
    "inventory right": pygame.K_e,
    "inventory left": pygame.K_q,
    "pause": pygame.K_RETURN
}

SOUND_VOLUMES = {
    "Music": 50,
    "Sound Effects": 50
}

CONTROLS_KEYS = ORIGINAL_CONTROLS_KEYS.copy()

ITEM_LOCATION_AROUND_PLAYER = (48, -48)

class ShouldSpawnBossAndInvincibillity():
    def __init__(self):
        self.snail_spawn = True
        self.doug_spawn = True
        self.boss_invincibillity = True
        self.first_move = True
        self.true_move = True
        self.true_first_move = True
        self.cooldown_first_move = True
        self.crane_alive = True
        self.whale_alive = True
        self.snail_alive = True
        self.crane = None

    def setSnailSpawn(self, value):
        self.snail_spawn = value

    def setDougSpawn(self, value):
        self.doug_spawn = value

    def getDougSpawn(self):
        return self.doug_spawn
    
    def getSnailSpawn(self):
        return self.snail_spawn

    def setBossInvincibillity(self, value):
        self.boss_invincibillity = value

    def getBossInvincibillity(self):
        return self.boss_invincibillity
    
    def getBossFirstMove(self):
        return self.first_move
    
    def setBossFirstMove(self, value):
        self.first_move = value
    
    def getTrueBossFirstMove(self):
        return self.true_move
    
    def setTrueBossFirstMove(self, value):
        self.true_move = value

    def getCooldownFirstMove(self):
        return self.cooldown_first_move
    
    def setCooldownFirstMove(self, value):
        self.cooldown_first_move = value

    def getCraneAlive(self):
        return self.crane_alive
    def setCraneAlive(self, value):
        self.crane_alive = value

    def getWhaleAlive(self):
        return self.whale_alive
    
    def setWhaleAlive(self, value):
        self.whale_alive = value

    def getSnailAlive(self):
        return self.snail_alive
    def setSnailAlive(self, value):
        self.snail_alive = value

    def getCrane(self):
        return self.crane
    
    def setCrane(self, value): 
        self.crane = value

    def hasWon (self):
        return not self.whale_alive and not self.snail_alive and not self.crane_alive
    
    def reset(self):
        self.snail_spawn = True
        self.doug_spawn = True
        self.boss_invincibillity = True
        self.first_move = True
        self.true_move = True
        self.true_first_move = True
        self.cooldown_first_move = True
        self.crane_alive = True
        self.whale_alive = True
        self.snail_alive = True


BOSS_CONDITIONS = ShouldSpawnBossAndInvincibillity()