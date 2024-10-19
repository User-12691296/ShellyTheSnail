from ..classes import Enemy
from constants.game import TILE_SIZE, BOSS_CONDITIONS
from constants.assets import BOSS_PATH
import pygame
import random
import math
import os
from ...projectiles import PROJECTILE_CLASSES
from .darknessenemies import DarknessKnightmare1
from .swampenemies import SwampAnaconda, SwampTangler
from ...items import Item, ItemStack, Inventory
import time

class CrabBoss (Enemy):
    def __init__(self):
        super().__init__(100, 2, 8)
        self.size = (5,5)
        self.radius = 5
        self.loadInventory()

        self.attack_pattern = 0
        self.attack_progress = 0

        self.killed_melee = False

        self.x, self.y = 0,0
        self.normal_movement_speed = 8

        self.image = pygame.image.load(os.path.join(BOSS_PATH, "DIAMONDKINGCRAB.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image_rect = self.image.get_rect()

        self.loadInventory()

    def loadInventory(self):
        self.inventory = Inventory(5,1,1)
        self.inventory.setItemStack(ItemStack("crystal_armor", 1), 0)
        self.inventory.setItemStack(ItemStack("dynamite_string", 100), 1)
        self.inventory.setItemStack(ItemStack("lemon", 2), 3)
        self.inventory.setItemStack(ItemStack("bomb", 1), 4)

    def clearInventory(self):
        for i in range(self.inventory.size):
            self.inventory.throwStackInLoc(self.world, self.pos, i, 0)

    def kill(self):
        super().kill()
        if self.killed_melee:
            self.inventory.addItemStack(ItemStack("clawofcrabking", 5))
        self.clearInventory()

    @staticmethod
    def getNeededAssets():
        return ["DIAMONDKINGCRAB"]

    def isEnemy(self):
        return True
    
    def isBoss(self):
        return True

    def sumDamage(self):
        total_damage = 0

        dtt = 0

        while self.damages_this_tick:
            damage = max(self.damages_this_tick, key=lambda d: d[0])
            self.damages_this_tick.remove(damage)

            damage, source = damage
            true_damage = self.calcDamageModifiers(damage, dtt)
            total_damage += true_damage

            if total_damage >= self.getAttribute("health") and source == "slicing":
                self.killed_melee = True

            dtt += 1
        
        self.changeHealth(-total_damage)

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, self.size[0]-1):
            if not entity.isEnemy():
                entity.damage(0.1)

    def movementTick(self):
        if self.attack_pattern == 0 or self.attack_pattern == 2:
            super().movementTick()
        else:
            pass

    def tick(self):
        super().tick()
        if self.attack_pattern == 0 and not self.isCooldownActive("attack_pattern_cooldown"):
            self.attack_pattern = random.randint(1, 2)
            self.attack_progress = 1
            self.initial_player_pos = self.world.getPlayer().getPos().copy()
            
        if self.attack_pattern == 1:
            self.updatePositionForPattern1()
            self.handleAttacksForPattern1()

        if self.attack_pattern == 2:
            self.updatePositionForPattern2()

        if self.attack_progress > 0:
            self.attack_progress += 1

        # print(self.attack_progress, self.attack_pattern)

    def updatePositionForPattern1(self):
        self.x = self.initial_player_pos[0] + round(5*math.cos(math.radians(self.attack_progress*20)))
        self.y = self.initial_player_pos[1] + round(5*math.sin(math.radians(self.attack_progress*20)))
        self.setPos([self.x, self.y])
        if self.attack_progress > 360/5:
           self.attack_progress = 0
           self.attack_pattern = 0
           self.registerCooldown("attack_pattern_cooldown", 120)

    def handleAttacksForPattern1(self):
        pass

    def updatePositionForPattern2(self):
        self.setAttribute("movement_speed", self.normal_movement_speed/2)
        if self.attack_progress > 100:
            self.setAttribute("movement_speed", self.normal_movement_speed)
            self.attack_progress = 0
            self.attack_pattern = 0
            self.registerCooldown("attack_pattern_cooldown", 120)        

    def draw(self, display, display_topleft=(0, 0)):
        self.updateHitbox()
        self.radius = 5
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        # entity_texture = self.atlas.getTexture("DIAMONDKINGCRAB")
        rotated_image = pygame.transform.rotate(self.image, -self.facing_angle+90)
        final_rect = rotated_image.get_rect(center=spos)
        # final_texture = pygame.transform.scale(rotated_texture, (self.size[0]*TILE_SIZE, self.size[1]*TILE_SIZE))

        # final_rect = final_texture.get_rect(center=spos)
        display.blit(rotated_image, final_rect)

        self.drawHealthBar(display, display_topleft)


        # HELP = self.bufferPosToDisplayPos(self.world.tilePosToBufferPos(self.hitbox.topleft), display_topleft)
        # pygame.draw.rect(display, (255,0,0,0.2), pygame.rect.Rect(HELP[0], HELP[1], 5*TILE_SIZE, 5*TILE_SIZE))

class MedusaBoss (Enemy):
    def __init__(self):
        super().__init__(125, 3, 10)
        self.size = (3,3)
        self.radius = 3
        self.attack_pattern = 0
        self.attack_progress = 0

        self.x, self.y = 0,0
        self.normal_movement_speed = 8

        self.image = pygame.image.load(os.path.join(BOSS_PATH, "SwampMedusa.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image_rect = self.image.get_rect()

        self.killed_melee = False

        self.loadInventory()

    def loadInventory(self):
        self.inventory = Inventory(5,1,1)
        self.inventory.setItemStack(ItemStack("croc", 1), 0)
        self.inventory.setItemStack(ItemStack("watermelon", 4), 1)
        self.inventory.setItemStack(ItemStack("lemon", 4), 2)


    def clearInventory(self):
        for i in range(self.inventory.size):
            self.inventory.throwStackInLoc(self.world, self.pos, i, 0)

    def kill(self):
        super().kill()
        if self.killed_melee:
            self.inventory.setItemStack(ItemStack("clawofsnakequeen"), 3)
        self.clearInventory()

    @staticmethod
    def getNeededAssets():
        return ["SwampMedusa"]

    def isEnemy(self):
        return True
    
    def isBoss(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, self.size[0]-1):
            if not entity.isEnemy():
                entity.damage(0.1)

    def movementTick(self):
        super().movementTick()

    def tick(self):
        super().tick()
        if self.attack_pattern == 0 and not self.isCooldownActive("attack_pattern_cooldown"):
            self.attack_pattern = random.randint(1, 2)
            self.attack_progress = 1
            self.initial_player_pos = list(self.world.getPlayer().getPos()).copy()
            
        if self.attack_pattern == 1:
            self.updatePositionForPattern1()
            self.handleAttacksForPattern1()

        if self.attack_pattern == 2:
            self.updatePositionForPattern2()
            self.handleAttacksForPattern2()

        if self.attack_progress > 0:
            self.attack_progress += 1

        # print(self.attack_progress, self.attack_pattern)

    def clearAttributes(self, cooldown):
        self.attack_progress = 0
        self.attack_pattern = 0
        self.registerCooldown("attack_pattern_cooldown", cooldown)        

    def sumDamage(self):
        total_damage = 0

        dtt = 0

        while self.damages_this_tick:
            damage = max(self.damages_this_tick, key=lambda d: d[0])
            self.damages_this_tick.remove(damage)

            damage, source = damage
            true_damage = self.calcDamageModifiers(damage, dtt)
            total_damage += true_damage

            if total_damage >= self.getAttribute("health") and source == "slicing":
                self.killed_melee = True

            dtt += 1
        
        self.changeHealth(-total_damage)


    def updatePositionForPattern1(self):
        pass

    def handleAttacksForPattern1(self):
        if self.attack_progress % 25 == 0:
            self.x = self.initial_player_pos[0] + random.randint(5,8)*(random.randint(0,1)*2-1)
            self.y = self.initial_player_pos[1] + random.randint(5,8)*(random.randint(0,1)*2-1)
            eagle = SwampTangler()
            eagle.setPos([self.x, self.y])
            self.world.addEntity(eagle)
        if self.attack_progress > 80:
            self.clearAttributes(100)

    def handleAttacksForPattern2(self):
        if self.attack_progress % 25 == 0:
            eagle = SwampAnaconda()
            eagle.setPos([self.pos[0] + random.randint(2,5)*(random.randint(0,1)*2-1), self.pos[1]+random.randint(2,5)*(random.randint(0,1)*2-1)])
            self.world.addEntity(eagle)
        
        if self.attack_progress > 80:
            self.clearAttributes(100)



    def updatePositionForPattern2(self):
        pass    

    def draw(self, display, display_topleft=(0, 0)):
        self.updateHitbox()
        self.radius = 5
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        # entity_texture = self.atlas.getTexture("DIAMONDKINGCRAB")
        rotated_image = pygame.transform.rotate(self.image, -self.facing_angle+90)
        final_rect = rotated_image.get_rect(center=spos)
        # final_texture = pygame.transform.scale(rotated_texture, (self.size[0]*TILE_SIZE, self.size[1]*TILE_SIZE))

        # final_rect = final_texture.get_rect(center=spos)
        display.blit(rotated_image, final_rect)

        self.drawHealthBar(display, display_topleft)

        HELP = self.bufferPosToDisplayPos(self.world.tilePosToBufferPos(self.hitbox.topleft), display_topleft)
        # pygame.draw.rect(display, (255,0,0,0.2), pygame.rect.Rect(HELP[0], HELP[1], 5*TILE_SIZE, 5*TILE_SIZE))


# FINAL BOSSES
class CraneBoss (Enemy):
    def __init__(self):
        super().__init__(300, 2, 7)
        self.size = (5,5)
        self.radius = 2
        self.loadInventory()

        self.attack_pattern = 0
        self.attack_progress = 0

        self.x, self.y = 0,0
        self.normal_movement_speed = 8

        self.image = pygame.image.load(os.path.join(BOSS_PATH, "KungFuKrane.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image_rect = self.image.get_rect()

        self.initial_tick = True
        self.max_health = 300
        self.should_spawn_snail = False
        self.should_spawn_whale = False

    def loadInventory(self):
        self.inventory = Inventory(5,1,1)
        self.inventory.setItemStack(ItemStack("watermelon", 4), 0)
        self.inventory.setItemStack(ItemStack("lemon", 4), 1)

    def clearInventory(self):
        for i in range(self.inventory.size):
            self.inventory.throwStackInLoc(self.world, self.pos, i, 0)

    def kill(self):
        self.clearAttributes(0)
        BOSS_CONDITIONS.setCrane(self)

        super().kill()
        BOSS_CONDITIONS.setCraneAlive(False)
        self.clearInventory()

    @staticmethod
    def getNeededAssets():
        return ["KungFuKrane"]

    def isEnemy(self):
        return True
    
    def isBoss(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, self.size[0]-1):
            if not entity.isEnemy():
                entity.damage(0.2)

    def movementTick(self):
        if self.isCooldownActive("first_move"):
            return
        if self.attack_pattern == 0:
            super().movementTick()
        else:
            pass

    def tick(self):
        if BOSS_CONDITIONS.getBossInvincibillity():
            self.setAttribute("health", self.max_health)
        super().tick()

        if BOSS_CONDITIONS.getTrueBossFirstMove() or (BOSS_CONDITIONS.getBossFirstMove() and not BOSS_CONDITIONS.getWhaleAlive()):
            self.whale = WhaleBoss()
            print("hi")
            BOSS_CONDITIONS.setWhaleAlive(True)
            self.should_spawn_whale = True
        if BOSS_CONDITIONS.getTrueBossFirstMove() or (BOSS_CONDITIONS.getBossFirstMove() and not BOSS_CONDITIONS.getSnailAlive()):
            self.snail = EvilSnail()
            BOSS_CONDITIONS.setSnailAlive(True)
            self.should_spawn_snail = True

        if BOSS_CONDITIONS.getBossFirstMove():
            self.setAttribute("health", self.max_health)
            self.pos = [30,30]

            if BOSS_CONDITIONS.getDougSpawn():
                self.whale.setPos([self.pos[0]+10, self.pos[1]])
                self.whale.setFinalBoss()

                if self.should_spawn_whale:
                    self.world.addEntity(self.whale)
                    self.should_spawn_whale = False

            if BOSS_CONDITIONS.getSnailSpawn():
                self.snail.setPos([self.pos[0]-5, self.pos[1]])

                if self.should_spawn_snail:
                    self.world.addEntity(self.snail)
                    self.should_spawn_snail = True

            BOSS_CONDITIONS.setBossFirstMove(False)
            self.registerCooldown("first_move", 120)


        if BOSS_CONDITIONS.getTrueBossFirstMove():
            BOSS_CONDITIONS.setTrueBossFirstMove(False)

        if not self.isCooldownActive("first_move"):
            BOSS_CONDITIONS.setCooldownFirstMove(False)
        else:
            return

        if self.attack_pattern == 0 and not self.isCooldownActive("attack_pattern_cooldown"):
            self.attack_pattern = random.randint(1, 2)
            self.attack_progress = 1
            self.initial_player_pos = self.world.getPlayer().getPos().copy()
            
        if self.attack_pattern == 1:
            self.updatePositionForPattern1()
            self.handleAttacksForPattern1()

        if self.attack_pattern == 2:
            self.updatePositionForPattern2()
            self.handleAttacksForPattern2()

        if self.attack_progress > 0:
            self.attack_progress += 1

        # print(self.attack_progress, self.attack_pattern, self.getCooldownFrame("attack_pattern_cooldown"))

    def clearAttributes(self, cooldown):
        self.attack_progress = 0
        self.attack_pattern = 0
        self.registerCooldown("attack_pattern_cooldown", cooldown)        


    def updatePositionForPattern1(self):
        self.facing_angle=180
        self.x = self.initial_player_pos[0] + round(5*math.cos(math.radians(self.attack_progress*20)))
        self.y = self.initial_player_pos[1] + round(5*math.sin(math.radians(self.attack_progress*20)))
        self.setPos([self.x, self.y])
        if self.attack_progress > 360/5:
           self.attack_progress = 0
           self.attack_pattern = 0
           self.registerCooldown("attack_pattern_cooldown", 120)

    def handleAttacksForPattern1(self):
        if self.isCooldownActive("bullets"): 
            return

        number_of_bullets = 8
        for i in range(number_of_bullets):
            angle = (360/number_of_bullets)*i
            pos = self.pos
            self.projectile = PROJECTILE_CLASSES.PoisonDart(pos, angle)
            self.projectile.giveImmunity(self)
            self.world.addProjectile(self.projectile)

        self.registerCooldown("bullets", 25)

    def updatePositionForPattern2(self):
        speed = 1
        self.x = self.initial_player_pos[0]-20 + self.attack_progress//speed
        self.y = self.initial_player_pos[1]
        self.setPos([self.x, self.y])
        if self.attack_progress > 40*speed:
            self.clearAttributes(100)

    def handleAttacksForPattern2(self):
        self.handleAttacksForPattern1()
        

    def isFinalBoss(self):
        return True

    def draw(self, display, display_topleft=(0, 0)):
        self.updateHitbox()
        self.radius = 5
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        # entity_texture = self.atlas.getTexture("DIAMONDKINGCRAB")
        rotated_image = pygame.transform.rotate(self.image, -self.facing_angle+90)
        final_rect = rotated_image.get_rect(center=spos)
        # final_texture = pygame.transform.scale(rotated_texture, (self.size[0]*TILE_SIZE, self.size[1]*TILE_SIZE))

        # final_rect = final_texture.get_rect(center=spos)
        display.blit(rotated_image, final_rect)

        self.drawHealthBar(display, display_topleft)

        HELP = self.bufferPosToDisplayPos(self.world.tilePosToBufferPos(self.hitbox.topleft), display_topleft)
        # pygame.draw.rect(display, (255,0,0,0.2), pygame.rect.Rect(HELP[0], HELP[1], 5*TILE_SIZE, 5*TILE_SIZE))

class WhaleBoss (Enemy):
    def __init__(self):
        super().__init__(400, 2, 8)
        self.size = (9,9)
        self.radius = 2
        self.loadInventory()

        self.attack_pattern = 0
        self.attack_progress = 0

        self.x, self.y = 0,0
        self.normal_movement_speed = 8

        self.image = pygame.image.load(os.path.join(BOSS_PATH, "DarknessWhaleBoss.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image_rect = self.image.get_rect()

        self.final_boss = False
        self.alpha = 255

        self.max_health = 400
        self.first_move = True
        
        self.first_time = time.time()

    def kill(self):
        super().kill()
        self.clearInventory()
        if not self.isFinalBoss():
            BOSS_CONDITIONS.setDougSpawn(False)
        BOSS_CONDITIONS.setWhaleAlive(False)

    def setFinalBoss(self):
        self.final_boss = True

    @staticmethod
    def getNeededAssets(self):
        return ["DarknessWhaleBoss"]

    def loadInventory(self):
        self.inventory = Inventory(5,1,1)
        self.inventory.setItemStack(ItemStack("watermelon", 4), 0)
        self.inventory.setItemStack(ItemStack("lemon", 4), 1)

    def clearInventory(self):
        for i in range(self.inventory.size):
            self.inventory.throwStackInLoc(self.world, self.pos, i, 0)

    @staticmethod
    def getNeededAssets():
        return ["DarknessWhaleBoss"]

    def isEnemy(self):
        return True
    
    def isBoss(self):
        return True

    def damageTick(self):
        if self.active:
            for entity in self.world.getEntitiesInRangeOfTile(self.pos, self.radius+1):
                if not entity.isEnemy():
                    entity.damage(0.5)

    def movementTick(self):
        pass

    def tick(self):
        if BOSS_CONDITIONS.getBossInvincibillity() and self.isFinalBoss():
            self.setAttribute("health", self.max_health)

        super().tick()
        self.first_time = time.time()
        if self.attack_pattern == 0 and ((BOSS_CONDITIONS.getCooldownFirstMove() == False and self.final_boss == True) or not self.final_boss) and self.attack_progress == 0 and not self.isCooldownActive("attack_pattern_cooldown"):
            self.attack_pattern = 1
            self.attack_progress = 1
            self.initial_player_pos = self.world.getPlayer().getPos().copy()
            if self.attack_pattern == 1:
                self.active = False
                self.alpha = 1
                self.pos = self.initial_player_pos
                self.registerCooldown("bullets", 10)

        if self.attack_pattern == 1:
            self.updatePositionForPattern1()
            self.handleAttacksForPattern1()

        # if self.attack_pattern == 2:
        #     self.updatePositionForPattern2()
        #     self.handleAttacksForPattern2()

        if self.attack_progress > 0:
            self.attack_progress += 1

    def clearAttributes(self, cooldown):
        self.attack_progress = 0
        self.attack_pattern = 0
        self.registerCooldown("attack_pattern_cooldown", cooldown)    

    def updatePositionForPattern1(self):
        if not self.active:
            self.alpha = self.attack_progress*8

            if self.alpha > 255:
                self.alpha = 255
                self.active = True
                self.clearAttributes(20)

    def handleAttacksForPattern1(self):
        if self.isCooldownActive("bullets"): 
            return

        number_of_bullets = 8
        variance = random.randint(0,45)
        for i in range(number_of_bullets):
            angle = (360/number_of_bullets)*i+variance
            pos = self.pos
            self.projectile = PROJECTILE_CLASSES.Arrow(pos, angle)
            self.projectile.giveImmunity(self)
            self.world.addProjectile(self.projectile)
        if self.alpha % 60 == 0:
            eagle = DarknessKnightmare1()
            eagle.setPos([self.pos[0] + random.randint(5,10)*(random.randint(0,1)*2-1), self.pos[1]+random.randint(5,10)*(random.randint(0,1)*2-1)])
            self.world.addEntity(eagle)
        

        self.registerCooldown("bullets", 25)

    # def updatePositionForPattern2(self):
    #     speed = 1
    #     self.x = self.initial_player_pos[0]-20 + self.attack_progress//speed
    #     self.y = self.initial_player_pos[1]
    #     self.setPos((self.x, self.y))
    #     if self.attack_progress > 40*speed:
    #         self.clearAttributes(100)

    # def handleAttacksForPattern2(self):
    #     self.handleAttacksForPattern1()

  
    def isFinalBoss(self):
        return self.final_boss
      

    def draw(self, display, display_topleft=(0, 0)):
        self.updateHitbox()
        self.radius = 5
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        # entity_texture = self.atlas.getTexture("DIAMONDKINGCRAB")
        rotated_image = pygame.transform.rotate(self.image, -self.facing_angle+90)
        final_rect = rotated_image.get_rect(center=spos)
        # final_texture = pygame.transform.scale(rotated_texture, (self.size[0]*TILE_SIZE, self.size[1]*TILE_SIZE))
        rotated_image.set_alpha(self.alpha)
        # final_rect = final_texture.get_rect(center=spos)
        display.blit(rotated_image, final_rect)

        self.drawHealthBar(display, display_topleft)

        HELP = self.bufferPosToDisplayPos(self.world.tilePosToBufferPos(self.hitbox.topleft), display_topleft)
        # pygame.draw.rect(display, (255,0,0,0.2), pygame.rect.Rect(HELP[0], HELP[1], 5*TILE_SIZE, 5*TILE_SIZE))


class EvilSnail (Enemy):
    def __init__(self):
        super().__init__(300, 0, 35)
        self.stuck = False
        BOSS_CONDITIONS.setBossInvincibillity(True)

    @staticmethod
    def getNeededAssets():
        return ["EvilSnail"]

    def isEnemy(self):
        return True
    
    def isBoss(self):
        return True

    def isFinalBoss(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.1)

    def kill(self):
        super().kill()
        BOSS_CONDITIONS.setBossInvincibillity(False)
        BOSS_CONDITIONS.setSnailAlive(False)

    def movementTick(self):
        if self.world.changes_this_tick:
            self.calcPath()

        if self.isCooldownActive("movement"):
            return
        
        if self.stuck:
            return

        node = self.pathfinder.getNode()
        if node:
            old_pos = self.pos
            self.setPos([node[0], node[1]])
            self.movement_this_tick[1] = self.pos[1]-old_pos[1]
            self.movement_this_tick[0] = self.pos[0]-old_pos[0]

            self.setPos([old_pos[0]-self.movement_this_tick[0], old_pos[1]-self.movement_this_tick[1]])

            self.movement_this_tick[1] = -self.movement_this_tick[1]
            self.movement_this_tick[0] = -self.movement_this_tick[0]

            if self.world.getTileID(self.pos) != "grass":
                if self.movement_this_tick[0] > 1 and self.movement_this_tick[1] > 1:
                    if self.world.getTileId(old_pos[0], old_pos[1]+ self.movement_this_tick[1]) != "grass":
                        self.movement_this_tick[0] = 0
                    elif self.world.getTileId(old_pos[0]+self.movement_this_tick[0], old_pos[1]) != "grass":
                        self.movement_this_tick[1] = 0

                if self.movement_this_tick[0] == 0:
                    if self.movement_this_tick[1] > 0:
                        self.movement_this_tick[0] = 1
                    if self.movement_this_tick[1] < 0:
                        self.movement_this_tick[0] = -1
                    self.movement_this_tick[1] = 0
                if self.movement_this_tick[1] == 0:
                    if self.movement_this_tick[0] > 0:
                        self.movement_this_tick[1] = 1
                    if self.movement_this_tick[0] < 0:
                        self.movement_this_tick[1] = -1
                    self.movement_this_tick[0] = 0

            self.setPos([old_pos[0]+self.movement_this_tick[0], old_pos[1]+ self.movement_this_tick[1]])
            if self.world.getTileID(self.pos) != "grass":
                self.setPos(old_pos)
                self.stuck = True


        self.registerCooldown("movement", self.getAttribute("movement_speed"))

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("EvilSnail")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        self.drawHealthBar(display, display_topleft)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

# End Final Bosses

class DragonBoss (Enemy):
    def __init__(self):
        super().__init__(200, 2, 8)
        self.size = (5,5)
        self.radius = 2
        self.loadInventory()

        self.attack_pattern = 0
        self.attack_progress = 0

        self.x, self.y = 0,0
        self.normal_movement_speed = 8

        self.image = pygame.image.load(os.path.join(BOSS_PATH, "MoltenDragon.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image_rect = self.image.get_rect()


    def loadInventory(self):
        self.inventory = Inventory(5,1,1)
        self.inventory.setItemStack(ItemStack("dragon_hide", 1), 0)
        self.inventory.setItemStack(ItemStack("watermelon", 10), 1)
        self.inventory.setItemStack(ItemStack("lemon", 5), 2)


    def clearInventory(self):
        for i in range(self.inventory.size):
            self.inventory.throwStackInLoc(self.world, self.pos, i, 0)

    def kill(self):
        super().kill()
        self.clearInventory()

    @staticmethod
    def getNeededAssets():
        return ["MoltenDragon"]

    def isEnemy(self):
        return True
    
    def isBoss(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, self.size[0]-1):
            if not entity.isEnemy():
                entity.damage(0.2)

    def movementTick(self):
        if self.attack_pattern == 0:
            super().movementTick()
        else:
            pass

    def clearAttributes(self, cooldown):
        self.attack_progress = 0
        self.attack_pattern = 0
        self.registerCooldown("attack_pattern_cooldown", cooldown)        

    def tick(self):
        super().tick()
        if self.attack_pattern == 0 and not self.isCooldownActive("attack_pattern_cooldown"):
            self.attack_pattern = random.randint(1,2)
            self.attack_progress = 1
            self.initial_player_pos = self.world.getPlayer().getPos().copy()
            
        if self.attack_pattern == 1:
            self.updatePositionForPattern1()
            self.handleAttacksForPattern1()

        if self.attack_pattern == 2:
            self.updatePositionForPattern2()
            self.handleAttacksForPattern2()

        if self.attack_progress > 0:
            self.attack_progress += 1

        # print(self.attack_progress, self.attack_pattern, self.getCooldownFrame("attack_pattern_cooldown"))

    def updatePositionForPattern1(self):
        speed = 2
        tile_gap = 8
        if self.attack_progress < 180/speed:
            self.x = self.initial_player_pos[0] - tile_gap + round(tile_gap*2*(self.attack_progress/(180/speed)))
            self.y = self.initial_player_pos[1] - tile_gap + round(tile_gap*2*(self.attack_progress/(180/speed)))
            self.facing_angle = 360-135-180
        else:
            self.x = self.initial_player_pos[0] + tile_gap - round(tile_gap*2* (self.attack_progress-180/speed)/(180/speed))
            self.y = self.initial_player_pos[1] - tile_gap + round(tile_gap*2* (self.attack_progress-180/speed)/(180/speed))
            self.facing_angle = 180+45-90

        self.setPos([self.x, self.y])
        if self.attack_progress > 360/speed:
            self.clearAttributes(100)

    def handleAttacksForPattern1(self):
        if self.isCooldownActive("bullets"): 
            return

        number_of_bullets = 4
        offset = random.randint(0,90)
        for i in range(number_of_bullets):
            angle = (360/number_of_bullets)*i+offset
            pos = self.pos
            self.projectile = PROJECTILE_CLASSES.MoltenMaceProj(pos, angle)
            self.projectile.giveImmunity(self)
            self.world.addProjectile(self.projectile)

        self.registerCooldown("bullets", 10)

    def updatePositionForPattern2(self):
        self.facing_angle = 0
        speed = 2
        self.x = self.initial_player_pos[0]-20 + self.attack_progress//speed
        self.y = self.initial_player_pos[1]
        self.setPos([self.x, self.y])
        if self.attack_progress > 40*speed:
            self.clearAttributes(100)

    def handleAttacksForPattern2(self):
        self.handleAttacksForPattern1()
        

    def draw(self, display, display_topleft=(0, 0)):
        self.updateHitbox()
        self.radius = 5
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        # entity_texture = self.atlas.getTexture("DIAMONDKINGCRAB")
        rotated_image = pygame.transform.rotate(self.image, -self.facing_angle+90)
        final_rect = rotated_image.get_rect(center=spos)
        # final_texture = pygame.transform.scale(rotated_texture, (self.size[0]*TILE_SIZE, self.size[1]*TILE_SIZE))

        # final_rect = final_texture.get_rect(center=spos)
        display.blit(rotated_image, final_rect)
        self.drawHealthBar(display, display_topleft)
        HELP = self.bufferPosToDisplayPos(self.world.tilePosToBufferPos(self.hitbox.topleft), display_topleft)
        # pygame.draw.rect(display, (255,0,0,0.2), pygame.rect.Rect(HELP[0], HELP[1], 5*TILE_SIZE, 5*TILE_SIZE))

class WormBoss(Enemy):
    def __init__(self):
        super().__init__(250, 2, 6)
        self.size = (3,3)
        self.radius = 2
        self.loadInventory()

        self.attack_pattern = 0
        self.attack_progress = 0

        self.x, self.y = 0,0
        self.normal_movement_speed = 8

        self.image = pygame.image.load(os.path.join(BOSS_PATH, "BurrowedWorm.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image_rect = self.image.get_rect()


    def loadInventory(self):
        self.inventory = Inventory(5,1,1)
        self.inventory.setItemStack(ItemStack("watermelon", 4), 0)
        self.inventory.setItemStack(ItemStack("lemon", 4), 1)

    def clearInventory(self):
        for i in range(self.inventory.size):
            self.inventory.throwStackInLoc(self.world, self.pos, i, 0)

    def kill(self):
        super().kill()
        self.clearInventory()

    @staticmethod
    def getNeededAssets():
        return ["MoltenDragon"]

    def isEnemy(self):
        return True
    
    def isBoss(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, self.size[0]-1):
            if not entity.isEnemy():
                entity.damage(0.2)

    def movementTick(self):
        if self.attack_pattern == 0:
            super().movementTick()
        else:
            pass

    def clearAttributes(self, cooldown):
        self.attack_progress = 0
        self.attack_pattern = 0
        self.registerCooldown("attack_pattern_cooldown", cooldown)        

    def tick(self):
        super().tick()
        if self.attack_pattern == 0 and not self.isCooldownActive("attack_pattern_cooldown"):
            self.attack_pattern = random.randint(1,1)
            self.attack_progress = 1
            self.initial_player_pos = self.world.getPlayer().getPos().copy()
            
        if self.attack_pattern == 1:
            self.updatePositionForPattern1()
            self.handleAttacksForPattern1()

        if self.attack_pattern == 2:
            self.updatePositionForPattern2()
            self.handleAttacksForPattern2()

        if self.attack_progress > 0:
            self.attack_progress += 1

        # print(self.attack_progress, self.attack_pattern, self.getCooldownFrame("attack_pattern_cooldown"))

    def updatePositionForPattern1(self):
        self.setMovable(False)
        self.size = (7,7)
        self.hitbox = pygame.Rect(self.getPos(), self.size)
        self.updateHitbox()
        self.image = pygame.image.load(os.path.join(BOSS_PATH, "iceworm.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image_rect = self.image.get_rect()

        if self.attack_progress > 80:
            self.clearAttributes(100)
            self.image = pygame.image.load(os.path.join(BOSS_PATH, "BurrowedWorm.png")).convert_alpha()
            self.image = pygame.transform.scale_by(self.image, 4)
            self.image_rect = self.image.get_rect(center=self.image_rect.center)
            self.size = (3,3)
            self.hitbox = pygame.Rect(self.getPos(), self.size)
            self.updateHitbox()


    def handleAttacksForPattern1(self):
        if self.isCooldownActive("bullets"): 
            return

        number_of_bullets = 12
        offset = random.randint(0,90)
        for i in range(number_of_bullets):
            angle = (360/number_of_bullets)*i+offset
            pos = self.pos
            self.projectile = PROJECTILE_CLASSES.IceArrow(pos, angle)
            self.projectile.giveImmunity(self)
            self.world.addProjectile(self.projectile)

        self.registerCooldown("bullets", 10)

    def updatePositionForPattern2(self):
        self.facing_angle = 0
        speed = 2
        self.x = self.initial_player_pos[0]-20 + self.attack_progress//speed
        self.y = self.initial_player_pos[1]
        self.setPos([self.x, self.y])
        if self.attack_progress > 40*speed:
            self.clearAttributes(100)

    def handleAttacksForPattern2(self):
        self.handleAttacksForPattern1()
        

    def draw(self, display, display_topleft=(0, 0)):
        self.updateHitbox()
        self.radius = 5
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        # entity_texture = self.atlas.getTexture("DIAMONDKINGCRAB")
        rotated_image = pygame.transform.rotate(self.image, -self.facing_angle+90)
        final_rect = rotated_image.get_rect(center=spos)
        # final_texture = pygame.transform.scale(rotated_texture, (self.size[0]*TILE_SIZE, self.size[1]*TILE_SIZE))

        # final_rect = final_texture.get_rect(center=spos)
        display.blit(rotated_image, final_rect)

        HELP = self.bufferPosToDisplayPos(self.world.tilePosToBufferPos(self.hitbox.topleft), display_topleft)
        # pygame.draw.rect(display, (255,0,0,0.2), pygame.rect.Rect(HELP[0], HELP[1], self.size[0]*TILE_SIZE, self.size[1]*TILE_SIZE))

class MountainBoss (Enemy):
    def __init__(self):
        super().__init__(250, 2, 8)
        self.size = (5,5)
        self.radius = 2
        self.attack_pattern = 0
        self.attack_progress = 0

        self.x, self.y = 0,0
        self.normal_movement_speed = 8

        self.image = pygame.image.load(os.path.join(BOSS_PATH, "MountainDangerThunderBirdButNotReally.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image_rect = self.image.get_rect()
        self.killed_melee = False
        self.loadInventory()


    def loadInventory(self):
        self.inventory = Inventory(5,1,1)
        self.inventory.setItemStack(ItemStack("watermelon", 4), 0)
        self.inventory.setItemStack(ItemStack("lemon", 4), 1)

    def clearInventory(self):
        for i in range(self.inventory.size):
            self.inventory.throwStackInLoc(self.world, self.pos, i, 0)

    def kill(self):
        super().kill()
        self.inventory.setItemStack(ItemStack("scissors", 1), 2)
        self.clearInventory()

    @staticmethod
    def getNeededAssets():
        return ["MountainDangerThunderBirdButNotReally"]

    def isEnemy(self):
        return True
    
    def isBoss(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, self.size[0]-1):
            if not entity.isEnemy():
                entity.damage(0.2)

    def movementTick(self):
        if self.attack_pattern == 0:
            super().movementTick()
        else:
            pass

    def clearAttributes(self, cooldown):
        self.attack_progress = 0
        self.attack_pattern = 0
        self.registerCooldown("attack_pattern_cooldown", cooldown)        

    def tick(self):
        super().tick()
        if self.attack_pattern == 0 and not self.isCooldownActive("attack_pattern_cooldown"):
            self.attack_pattern = random.randint(1,2)
            self.attack_progress = 1
            self.initial_player_pos = self.world.getPlayer().getPos().copy()
            
        if self.attack_pattern == 1:
            self.updatePositionForPattern1()
            self.handleAttacksForPattern1()

        if self.attack_pattern == 2:
            self.updatePositionForPattern2()
            self.handleAttacksForPattern2()

        if self.attack_progress > 0:
            self.attack_progress += 1

        # print(self.attack_progress, self.attack_pattern, self.getCooldownFrame("attack_pattern_cooldown"))
    def sumDamage(self):
        total_damage = 0

        dtt = 0

        while self.damages_this_tick:
            damage = max(self.damages_this_tick, key=lambda d: d[0])
            self.damages_this_tick.remove(damage)

            damage, source = damage
            true_damage = self.calcDamageModifiers(damage, dtt)
            total_damage += true_damage

            if total_damage >= self.getAttribute("health") and source == "slicing":
                self.killed_melee = True

            dtt += 1
        
        self.changeHealth(-total_damage)

    def updatePositionForPattern1(self):
        speed = 2
        tile_gap = 8
        if self.attack_progress < 180/speed:
            self.x = self.initial_player_pos[0] - tile_gap + round(tile_gap*2*(self.attack_progress/(180/speed)))
            self.y = self.initial_player_pos[1] - tile_gap + round(tile_gap*2*(self.attack_progress/(180/speed)))
            self.facing_angle = 360-135-180
        else:
            self.x = self.initial_player_pos[0] + tile_gap - round(tile_gap*2* (self.attack_progress-180/speed)/(180/speed))
            self.y = self.initial_player_pos[1] - tile_gap + round(tile_gap*2* (self.attack_progress-180/speed)/(180/speed))
            self.facing_angle = 180+45-90

        self.setPos([self.x, self.y])
        if self.attack_progress > 360/speed:
            self.clearAttributes(100)

    def handleAttacksForPattern1(self):
        if self.isCooldownActive("bullets"): 
            return

        number_of_bullets = 8
        offset = random.randint(0,90)
        for i in range(number_of_bullets):
            angle = (360/number_of_bullets)*i+offset
            pos = self.pos
            self.projectile = PROJECTILE_CLASSES.Bolt(pos, angle)
            self.projectile.giveImmunity(self)
            self.world.addProjectile(self.projectile)

        self.registerCooldown("bullets", 10)

    def updatePositionForPattern2(self):
        self.facing_angle = 0
        speed = 2
        self.x = self.initial_player_pos[0]-20 + self.attack_progress//speed
        self.y = self.initial_player_pos[1]
        self.setPos([self.x, self.y])
        if self.attack_progress > 40*speed:
            self.clearAttributes(100)

    def handleAttacksForPattern2(self):
        if self.isCooldownActive("bullets"): 
            return

        number_of_bullets = 12
        offset = random.randint(0,90)
        for i in range(number_of_bullets):
            angle = (360/number_of_bullets)*i+offset
            pos = self.pos
            self.projectile = PROJECTILE_CLASSES.BlueBolt(pos, angle)
            self.projectile.giveImmunity(self)
            self.world.addProjectile(self.projectile)

        self.registerCooldown("bullets", 15)
        

    def draw(self, display, display_topleft=(0, 0)):
        self.updateHitbox()
        self.radius = 5
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        # entity_texture = self.atlas.getTexture("DIAMONDKINGCRAB")
        rotated_image = pygame.transform.rotate(self.image, -self.facing_angle+90)
        final_rect = rotated_image.get_rect(center=spos)
        # final_texture = pygame.transform.scale(rotated_texture, (self.size[0]*TILE_SIZE, self.size[1]*TILE_SIZE))

        # final_rect = final_texture.get_rect(center=spos)
        display.blit(rotated_image, final_rect)
        self.drawHealthBar(display, display_topleft)

        HELP = self.bufferPosToDisplayPos(self.world.tilePosToBufferPos(self.hitbox.topleft), display_topleft)
        # pygame.draw.rect(display, (255,0,0,0.2), pygame.rect.Rect(HELP[0], HELP[1], 5*TILE_SIZE, 5*TILE_SIZE))
    
class DarknessBoss (Enemy):
    def __init__(self):
        super().__init__(250, 2, 8)
        self.size = (5,5)
        self.radius = 2
        self.loadInventory()

        self.attack_pattern = 0
        self.attack_progress = 0

        self.x, self.y = 0,0
        self.normal_movement_speed = 8

        self.image = pygame.image.load(os.path.join(BOSS_PATH, "DarknessCorruptedSalamander.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image_rect = self.image.get_rect()


    def loadInventory(self):
        self.inventory = Inventory(5,1,1)
        self.inventory.setItemStack(ItemStack("watermelon", 4), 0)
        self.inventory.setItemStack(ItemStack("lemon", 4), 1)

    def clearInventory(self):
        for i in range(self.inventory.size):
            self.inventory.throwStackInLoc(self.world, self.pos, i, 0)

    @staticmethod
    def getNeededAssets():
        return ["DarknessCorruptedSalamander"]

    def isEnemy(self):
        return True
    
    def isBoss(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, self.size[0]-1):
            if not entity.isEnemy():
                entity.damage(0.8)

    def movementTick(self):
        if self.attack_pattern == 0:
            super().movementTick()
        else:
            pass

    def tick(self):
        super().tick()
        if self.attack_pattern == 0 and not self.isCooldownActive("attack_pattern_cooldown"):
            self.attack_pattern = 1
            self.attack_progress = 1
            angle = random.randint(0,360)
            self.facing_angle = angle
            self.initial_player_pos = self.world.getPlayer().getPos().copy()
            self.initial_x = self.initial_player_pos[0]+10*math.cos(math.radians(angle))
            self.initial_y = self.initial_player_pos[1]+10*math.sin(math.radians(angle))
            self.final_x = self.initial_player_pos[0]-10*math.cos(math.radians(angle))
            self.final_y = self.initial_player_pos[1]-10*math.sin(math.radians(angle))



        if self.attack_pattern == 1:
            self.updatePositionForPattern1()
            self.handleAttacksForPattern1()

        if self.attack_pattern == 2:
            self.updatePositionForPattern2()
            self.handleAttacksForPattern2()

        if self.attack_progress > 0:
            self.attack_progress += 1

        # print(self.attack_progress, self.attack_pattern, self.getCooldownFrame("attack_pattern_cooldown"))

    def clearAttributes(self, cooldown):
        self.attack_progress = 0
        self.attack_pattern = 0
        self.registerCooldown("attack_pattern_cooldown", cooldown)        


    def updatePositionForPattern1(self):
        self.x = round(self.initial_x + (self.final_x-self.initial_x)*(self.attack_progress/self.total_time))
        self.y = round(self.initial_y + (self.final_y-self.initial_y)*(self.attack_progress/self.total_time))
        self.setPos([self.x, self.y])
        if self.attack_progress > self.total_time:
            self.clearAttributes(20)

    def handleAttacksForPattern1(self):
        # if self.isCooldownActive("bullets"): 
        #     return

        # number_of_bullets = 4
        # for i in range(number_of_bullets):
        #     angle = (360/number_of_bullets)*i
        #     pos = self.pos
        #     self.projectile = PROJECTILE_CLASSES.Arrow(pos, angle)
        #     self.projectile.giveImmunity(self)
        #     self.world.addProjectile(self.projectile)

        # self.registerCooldown("bullets", 10)
        pass

    def updatePositionForPattern2(self):
        # speed = 1
        # self.x = self.initial_player_pos[0]-20 + self.attack_progress//speed
        # self.y = self.initial_player_pos[1]
        # self.setPos((self.x, self.y))
        # if self.attack_progress > 40*speed:
        #     self.clearAttributes(100)
        pass

    def handleAttacksForPattern2(self):
        self.handleAttacksForPattern1()
        

    def draw(self, display, display_topleft=(0, 0)):
        self.updateHitbox()
        self.radius = 5
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        # entity_texture = self.atlas.getTexture("DIAMONDKINGCRAB")
        rotated_image = pygame.transform.rotate(self.image, -self.facing_angle+90)
        final_rect = rotated_image.get_rect(center=spos)
        # final_texture = pygame.transform.scale(rotated_texture, (self.size[0]*TILE_SIZE, self.size[1]*TILE_SIZE))

        # final_rect = final_texture.get_rect(center=spos)
        display.blit(rotated_image, final_rect)
        self.drawHealthBar(display, display_topleft)

        HELP = self.bufferPosToDisplayPos(self.world.tilePosToBufferPos(self.hitbox.topleft), display_topleft)
        # pygame.draw.rect(display, (255,0,0,0.2), pygame.rect.Rect(HELP[0], HELP[1], 5*TILE_SIZE, 5*TILE_SIZE))
    
