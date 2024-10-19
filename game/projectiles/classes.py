import pygame
import numpy as np
import math

from misc import events

from constants import GAME

PROJECTILE_CULLING_RANGE = 20

class Projectile(events.EventAcceptor):
    def __init__(self, start, angle):
        self.start = start
        self.angle = angle
        self.speed = 0

        self.pos = [start[0], start[1]]
        
        self.immune = []

        self.alive = True

    @classmethod
    def fromStartEnd(cls, start, end):
        tx = end[0] - start[0]
        ty = end[1] - start[1]
        angle = math.degrees(math.atan2(ty, tx))

        return cls(start, angle)

    def setWorld(self, world):
        self.world = world

    @classmethod
    def setAtlas(cls, atlas):
        cls.atlas = atlas

    @classmethod
    def addToGroup(cls, group):
        group.append(cls)

    @staticmethod
    def getNeededAssets():
        return []

    def giveImmunity(self, entity):
        self.immune.append(entity)

    def isValidHit(self, entity):
        return not (entity in self.immune)

    def isAlive(self):
        return self.alive

    def kill(self):
        self.alive = False

    def getTilePos(self):
        return (round(self.pos[0]), round(self.pos[1]))

    def diagonalTo(self, point):
        return max(abs(point[0] - self.pos[0]), abs(point[1] - self.pos[1]))

    def isInRangeOf(self, point):
        return self.diagonalTo(point) < PROJECTILE_CULLING_RANGE

    def exists(self, point):
        range_check = self.isInRangeOf(point)

        life_check = self.alive

        return (range_check and life_check)

    def move(self, delta):
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]

    def getMovementDelta(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))

        return (dx, dy)

    def tick(self): pass

    def movementTick(self):
        delta = self.getMovementDelta()
        self.move(delta)
        
    def damageTick(self): pass
    def finalTick(self): pass

    @staticmethod
    def bufferPosToDisplayPos(bpos, display_topleft):
        return (bpos[0] + display_topleft[0], bpos[1] + display_topleft[1])

    def draw(self, display, display_topleft=(0, 0)):
        pass

    def stdDraw(self, display, tex_name, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPosOfCenter(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        raw = self.atlas.getTexture(tex_name)
        rect = raw.get_rect()
        rect.center = spos

        rot = pygame.transform.rotate(raw, -self.angle)
        rot_rect = rot.get_rect()
        rot_rect.center = rect.center

        display.blit(rot, rot_rect.topleft)
