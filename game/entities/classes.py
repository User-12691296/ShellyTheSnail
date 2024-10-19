import pygame
import numpy as np
import math
import random
import os

from misc import events
from ..items import Item, PlayerInventory, Inventory, ItemStack
from .pathfinding import PathFinder

from constants import GAME


class Entity(events.EventAcceptor):
    def __init__(self):
        self.pos = [2,10]

        self.cooldowns = {}

        self.attributes = {}

        self.movable = True
        self.movement_this_tick = [0, 0]
        
        self.alive = True
        self.active = True # Literally just used for the whale, means if you can pass through

        self.facing_angle = 0

    def setWorld(self, world):
        self.world = world

    def setOpaques(self, opaques):
        pass

    def onSpawn(self):
        pass

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    def collidesWith(self, pos):
        return (self.pos[0] == pos[0] and self.pos[1] == pos[1])

    def distanceTo2(self, pos):
        return (self.pos[0]-pos[0])**2 + (self.pos[1]-pos[1])**2

    def diagonalTo(self, pos):
        return max(abs(self.pos[0]-pos[0]), abs(self.pos[1]-pos[1]))

    def move(self, delta):
        if self.movable:
            self.pos[0] += delta[0]
            self.pos[1] += delta[1]

            self.movement_this_tick[0] += delta[0]
            self.movement_this_tick[1] += delta[1]

    def setMovable(self, val):
        self.movable = val

    @staticmethod
    def getNeededAssets():
        return []

    # All entities of the same class share the same textures, but are loaded in different places
    @classmethod
    def setAtlas(cls, atlas):
        cls.atlas = atlas

    @classmethod
    def addToGroup(cls, group):
        group.append(cls)

    def isAlive(self):
        return self.alive

    def isItemEntity(self):
        return False

    def isCreature(self):
        return False

    def isPlayer(self):
        return False
    
    def isEnemy(self):
        return False
    
    def isBoss(self):
        return False
    
    def isFinalBoss(self):
        return False

    def isEnemyTarget(self):
        return False
    
    def kill(self):
        self.alive = False

    def getBufferPos(self):
        return self.world.tilePosToBufferPos(self.pos)

    def registerCooldown(self, cooldown, frames):
        self.cooldowns[cooldown] = frames

    def getCooldownFrame(self, cooldown):
        return self.cooldowns.get(cooldown, 0)

    def isCooldownActive(self, cooldown):
        return self.cooldowns.get(cooldown, 0) > 0

    def defineAttribute(self, attribute, default):
        self.attributes[attribute] = [None, default]

    # Attributes - for values meant to change at runtime
    def setAttribute(self, attribute, value):
        attr = self.attributes.get(attribute)

        if attr:
            self.attributes[attribute][0] = value
            return value

        else:
            return None

    def getAttribute(self, attribute):
        attr = self.attributes.get(attribute)

        if not attr:
            return None

        value, default = attr

        if not value:
            return default
        else:
            return value

    def tick(self):
        for cooldown in (*self.cooldowns.keys(),):
            self.cooldowns[cooldown] -= 1
            if self.cooldowns[cooldown] <= 0:
                del self.cooldowns[cooldown]

        self.movement_this_tick = [0, 0]

    def movementTick(self): pass
    def damageTick(self): pass
    def finalTick(self): 
        if self.movement_this_tick[0] != 0 or self.movement_this_tick[1] != 0:
                self.facing_angle = math.degrees(math.atan2(self.movement_this_tick[1], self.movement_this_tick[0]))


    @staticmethod
    def bufferPosToDisplayPos(bpos, display_topleft):
        return (bpos[0] + display_topleft[0], bpos[1] + display_topleft[1])
    
    def draw(self, display, display_topleft=(0, 0)): pass

    def damage(*args): pass

class Creature(Entity):
    def __init__(self, health, size=(1, 1)):
        super().__init__()

        self.defineAttribute("max_health", 0)
        self.setAttribute("max_health", health)

        self.defineAttribute("health", 0)
        self.setAttribute("health", health)

        self.defineAttribute("general_armor", 0)
        self.defineAttribute("damage_threshold", 0)

        self.size = size

        self.hitbox = pygame.Rect((0, 0), size)
        self.radius = (self.size[0]+self.size[1])//2

        self.damages_this_tick = []

        self.effects = {}

    def onSpawn(self):
        super().onSpawn()

    def isCreature(self):
        return True

    def isEnemyTarget(self):
        return True

    def getHealth(self):
        return self.getAttribute("health")

    def getHealthPercentage(self):
        return self.getAttribute("health")/self.getAttribute("max_health")

    def changeHealth(self, delta):
        health = self.getAttribute("health")
        max_health = self.getAttribute("max_health")
        
        health += delta
        health = min(health, max_health)

        self.setAttribute("health", health)

        if health <= 0:
            self.kill()

    def updateHitbox(self):
        self.hitbox.center = self.getPos()
        self.radius = self.hitbox.width//2

    def collidesWith(self, point):
        return self.hitbox.collidepoint(point)

    def distanceTo2(self, pos):
        dx = abs(self.pos[0]-pos[0])
        dy = abs(self.pos[1]-pos[1])

        return dx**2 - (self.radius * 2*dx) + dy**2 - (self.radius * 2*dy)

    def giveEffect(self, effect_name, duration, action, reverse_action):
        self.effects[effect_name] = {
            "effect_time": 0,
            "effect_duration": duration,
            "action": action,
            "reverse_action": reverse_action,
        }

    def effectTimeUpdate(self):
        for effect in self.effects:
            self.effects[effect]["effect_time"]+=1
            self.effects[effect]["action"](self, self.world, self.pos) 
            # If the duration is less than the counter 
            if self.effects[effect]["effect_time"] > self.effects[effect]["effect_duration"]:
                self.effects[effect]["reverse_action"](self, self.world, self.pos) # Reverse Effect
                self.effects.pop(effect, None)
                break
            
    def tick(self):
        super().tick()

        self.damages_this_tick = []
        self.effectTimeUpdate()

    def movementTick(self):
        super().movementTick()
        
        self.updateHitbox()

    def damageTick(self):
        super().damageTick()

    def finalTick(self):
        super().finalTick()

        self.sumDamage()

    def damage(self, damage, source=None):
        self.damages_this_tick.append((damage, source))

    def sumDamage(self):
        total_damage = 0

        dtt = 0

        while self.damages_this_tick:
            damage = max(self.damages_this_tick, key=lambda d: d[0])
            self.damages_this_tick.remove(damage)

            damage, source = damage
            true_damage = self.calcDamageModifiers(damage, dtt)
            total_damage += true_damage

            dtt += 1
        
        self.changeHealth(-total_damage)

    def calcDamageModifiers(self, damage, dtt=0):
        general_armor = self.getAttribute("general_armor")
        dmg_threshold = self.getAttribute("damage_threshold")

        if general_armor > 0 and dmg_threshold > 0:
            if damage < dmg_threshold: 
                damage /= general_armor  # Minecraft style
                damage = max(damage, 0) 

            else:
                damage -= general_armor  # Terraria style
                damage = max(damage, 0)  

        return (damage/(2**dtt))
    
    def setArmorValues (self, armor_points, dmg_threshold): 
        self.setAttribute("general_armor", armor_points)
        self.setAttribute("damage_threshold", dmg_threshold)

    def getArmorValues(self):
        return (self.getAttribute("general_armor"), self.getAttribute("damage_threshold"))

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display)
        
        self.drawHealthBar(display, display_topleft)

    def drawHealthBar(self, display, display_topleft=(0, 0)):
        width = GAME.TILE_SIZE
        health_bar = pygame.Rect((0, 0), (width, 10))

        bpos = self.world.tilePosToBufferPos(self.getPos())
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        health_bar.left = spos[0]
        health_bar.top = spos[1] - 20

        # Background
        pygame.draw.rect(display, (255, 0, 0), health_bar)

        # Foreground
        health_bar.width = round(width*self.getHealthPercentage())
        pygame.draw.rect(display, (0, 255, 0), health_bar)

class Barrel(Creature):
    def __init__(self, health, stop_range=1, movement_speed=0):
        super().__init__(1)

        self.loadInventory()

    def isEnemy(self):
        return True
    
    def isEnemyTarget(self):
        return False

    def loadInventory(self):
        self.inventory = Inventory(5,1,1)
        self.inventory.setActiveStack(0)
        
    def kill(self):
        super().kill()
        self.dropItems()
    
    def dropItems(self):
        if self.getNeededAssets() == ["bronze"] or self.getNeededAssets() == ["plat"]:
            for i in range(2):
                current_stack_index = random.randint(0, self.inventory.size - 3)
                item_stack = self.inventory.getItemStack(current_stack_index)
                while item_stack == None:
                    current_stack_index = random.randint(0, self.inventory.size - 3)
                    item_stack = self.inventory.getItemStack(current_stack_index)
                self.inventory.throwStackInLoc(self.world, self.pos, current_stack_index, 0)

        else: 
            for i in range(1):
                current_stack_index = random.randint(0, self.inventory.size - 3)
                item_stack = self.inventory.getItemStack(current_stack_index)
                while item_stack == None:
                    current_stack_index = random.randint(0, self.inventory.size - 3)
                    item_stack = self.inventory.getItemStack(current_stack_index)
                self.inventory.throwStackInLoc(self.world, self.pos, current_stack_index, 0)

        """ for current_stack_index in range((self.inventory.size) - 2):
            self.inventory.throwStackInLoc(self.world,self.pos,current_stack_index, 0)
        self.inventory.throwStackInLoc(self.world,self.pos,current_stack_index, (random.randint(1, 5))) """
        

    
class Enemy(Creature):
    def __init__(self, health, stop_range=1, movement_speed=10):
        super().__init__(health)

        """ CODE TO ADD MOB DROPS """
        """ self.loadInventory() """ 
        self.defineAttribute("stopping_range", 0)
        self.setAttribute("stopping_range", stop_range)
        
        self.defineAttribute("movement_speed", 100)
        self.setAttribute("movement_speed", movement_speed)

    def setWorld(self, world):
        super().setWorld(world)

        self.pathfinder = PathFinder(self.world.size, self.getAttribute("stopping_range"))

    def setOpaques(self, opaques):
        super().setOpaques(opaques)

        self.pathfinder.setOpaques(opaques)

    def onSpawn(self):
        super().onSpawn()

        self.calcPath()

    def calcPath(self):
        self.pathfinder.calcPath(self.getPos(), self.world.getPlayer().getPos())

    def isEnemy(self):
        return True

    def isEnemyTarget(self):
        return False
    
    def movementTick(self):
        super().movementTick()

        if self.world.changes_this_tick:
            self.calcPath()

        if self.isCooldownActive("movement"):
            return

        node = self.pathfinder.getNode()
        if node:
            old_pos = self.pos
            self.setPos(node)
            self.movement_this_tick[1] = self.pos[1]-old_pos[1]
            self.movement_this_tick[0] = self.pos[0]-old_pos[0]

        self.registerCooldown("movement", self.getAttribute("movement_speed"))

    """ CODE TO ADD MOB DROPS """
    """ def loadInventory(self):
        self.inventory = Inventory(3,1,1)
        self.inventory.setItemStack(ItemStack("lil_sword", 1), 1)
        self.inventory.setActiveStack(1)
        
    def kill(self):
        super().kill()
        self.inventory.throwStackInLoc(self.world,self.pos,1) """
