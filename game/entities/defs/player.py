import pygame
import math

from misc import events
from ..classes import Entity, Creature, Enemy
from ...items import PlayerInventory, ItemStack
from .bosses import CraneBoss

from constants import GAME

INITIAL_PLAYER_HEALTH = 10

class Player(Creature):    
    def __init__(self):
        super().__init__(INITIAL_PLAYER_HEALTH)

        self.loadHUD()
        self.loadInventory()
        self.initAttributes()

        self.pos = [461,470]
        self.biome = []

        self.disp = False

    def loadHUD(self):
        self.hud = PlayerHUD(self)

    def loadInventory(self):
        self.inventory = PlayerInventory()
        self.inventory.setPlayer(self)
        self.inventory.setItemStack(ItemStack("golf_club", 1), 0)
        self.inventory.setItemStack(ItemStack("rusty_mirror",1), 1)
        self.inventory.setItemStack(ItemStack("apple", 3), 2)

    def initAttributes(self):
        # Frames per movement
        self.defineAttribute("movement_speed", GAME.PLAYER_WALKING_SPEED)
        self.setAttribute("movement_speed", GAME.PLAYER_WALKING_SPEED)

        self.defineAttribute("projectile_rate_modifier", 1)
        self.setAttribute("projectile_rate_modifier", 1)

        # Magma speed boost
        self.defineAttribute("magma_speed_boost", False)
        self.setAttribute("magma_speed_boost", False)

        # Range of vision
        self.defineAttribute("vision_range", 12)
        self.setAttribute("vision_range", 12)

        # Damage output modifier
        self.defineAttribute("damage_modifier", 1)
        self.setAttribute("damage_modifier", 1)

        # Decimal number, outside -1 to +1 range causes problems, -5 to +5 is fatal
        self.defineAttribute("temperature", 0)
        self.setAttribute("temperature", 0)
        self.defineAttribute("thermal_insulation", 12)
        self.setAttribute("thermal_insulation", 12)

        # Integer part represents its place in the bar chart
        # Rational part represents fullness
        self.defineAttribute("vibes", 2.0)
        self.setAttribute("vibes", 2.0)

        # 0 to 1
        # < 0.2 halves movement speed
        # < 0.1 causes screen shaking
        self.defineAttribute("hunger", 0)
        self.setAttribute("hunger", 1)
        self.defineAttribute("hunger_consumption_speed", 1) # Slower/faster than default of 600 seconds

        # 0 to 1
        # < 0.8 fatal
        self.defineAttribute("oxygen", 1)
        self.setAttribute("oxygen", 1)

        # Integer from 0 to 5
        # 1 - Half movement speed
        # 2 - Half damage
        # 3 - No movement
        # 4 - No damage
        # 5 - Fatal
        self.defineAttribute("fatigue", 0)
        self.setAttribute("fatigue", 0)
        self._most_recent_fatigue_level_reached = 0
        self._resting_tick_counter = 0

        # 0 to 1
        # > 0.4 plays funny sound
        # > 1.0 teleports you to the final boss, half movement, controls flipped
        self.defineAttribute("insanity", 0)
        self.setAttribute("insanity", 0)
        self.defineAttribute("insanity_progress_speed", 40) #seconds
        self.defineAttribute("insanity_regen_speed", 8) #seconds

        # 0 to 1
        # 0 fatal
        self.defineAttribute("thirst", 1)
        self.setAttribute("thirst", 1)

    @staticmethod
    def getNeededAssets():
        return ["player1"]

    def setManager(self, manager):
        self.manager = manager

    def isPlayer(self):
        return True

    def setVisionRange(self, range):
        self.setAttribute("vision_range", range)
        
    def getVisionRange(self):
        return self.getAttribute("vision_range")

    def getTemperatureBarData(self):
        temp = self.getAttribute("temperature")
        percent = (temp+5)/10
        percent = min(1, max(0, percent))
        return percent, (255*percent, 255*percent, 255*(1-percent))

    def getVibesBarData(self):
        return self.getAttribute("vibes")%1, (0, 255, 255)

    def getHungerBarData(self):
        return self.getAttribute("hunger"), (150, 20, 20)

    def getOxygenBarData(self):
        return self.getAttribute("oxygen"), (0, 250, 100)

    def getFatigueBarData(self):
        return self.getAttribute("fatigue")/5, (0, 150, 0)

    def getInsanityBarData(self):
        return self.getAttribute("insanity"), (0, 0, 0)

    def getThirstBarData(self):
        return self.getAttribute("thirst"), (255, 100, 100)

    def getBarDataGetters(self):
        return [lambda: (self.getHealthPercentage(), (255, 0, 0)),
                     self.getTemperatureBarData,
                     self.getVibesBarData,
                     self.getHungerBarData,
                     self.getOxygenBarData,
                     self.getFatigueBarData,
                     self.getInsanityBarData,
                     self.getThirstBarData]

    def temperatureTick(self):
        extern_temp = 0
        
        # Bring self temperature closer to biome temperature
        for biome_temp in self.world.getTileExtrasFromGroups(self.pos, "temperature", 0):
            extern_temp += biome_temp
            
        intern_temp = self.getAttribute("temperature")

        temp_delta = extern_temp - intern_temp

        if abs(temp_delta) > 0.1:
            # Temperature changes by 0.1 in the direction of temp_change
            temp_change = max(1/60/self.getAttribute("thermal_insulation"),
                              abs(temp_delta)/60/self.getAttribute("thermal_insulation"))

            self.setAttribute("temperature", intern_temp + math.copysign(temp_change, temp_delta))

        # Die when too hot or too cold
        if abs(self.getAttribute("temperature")) > 5:
            self.damage((abs(self.getAttribute("temperature"))-5)**2)

    def vibesTick(self):
        vibes = self.getAttribute("vibes")
        vibes += 1

        self.setAttribute("vibes", vibes + math.sin(vibes)/10)

    def hungerTick(self):
        hunger = self.getAttribute("hunger")

        # 600 seconds till hunger depletes fully
        hunger -= 1/60/600 * self.getAttribute("hunger_consumption_speed")

        self.setAttribute("hunger", hunger)

        # Die when hunger drops to 0
        if hunger <= 0:
            self.damage(0.2)
        if hunger > 1:
            self.damage(hunger-1)
            self.setAttribute("hunger", 1)
    def changeHunger(self, delta):
        self.setAttribute("hunger", self.getAttribute("hunger")+delta)

    def oxygenTick(self):
        pass

    def fatigueTick(self):
        fatigue = self.getAttribute("fatigue")

        if "mountains" in self.world.getGroupsWithTile(self.pos):
            self.tire(0.01)

        if fatigue < self._most_recent_fatigue_level_reached:
            self._most_recent_fatigue_level_reached = fatigue

        if fatigue >= 1 and self._most_recent_fatigue_level_reached < 1:
            self.setAttribute("movement_speed", self.getAttribute("movement_speed")*2)
            self._most_recent_fatigue_level_reached = 1

            self._resting_tick_counter += 1

        if fatigue >= 2 and self._most_recent_fatigue_level_reached < 2:
            self.setAttribute("damage_modifier", self.getAttribute("damage_modifier")/2)
            self._most_recent_fatigue_level_reached = 2

        if fatigue >= 3:
            self.setMovable(False)
            self._most_recent_fatigue_level_reached = 3

        if fatigue >= 4:
            self.setAttribute("damage_modifier", 0)
            self._most_recent_fatigue_level_reached = 4

        if fatigue >= 5:
            self.kill()

        if self._resting_tick_counter > 60*60 and fatigue > 0:
            self.setAttribute("fatigue", fatigue-1)
            self._resting_tick_counter = 0

    def tire(self, fatigue_delta):
        self.setAttribute("fatigue", self.getAttribute("fatigue")-fatigue_delta)
        self._resting_tick_counter = 0

    def FOVobstruction (self):
        if "deepdark" in self.world.getGroupsWithTile(self.pos):
            if self.inventory.getSelectedStack() != None:
                if self.inventory.getSelectedStack().getItemID() == "lantern":
                    self.setVisionRange(12)
                else:
                    self.setVisionRange(3)
        else: 
            if self.inventory.getSelectedStack() != None:
                if self.inventory.getSelectedStack().getItemID() == "lantern":
                    self.setVisionRange(14)
                else:
                    self.setVisionRange(12)

    def checkBiome (self):
        if "lobby" in self.world.getGroupsWithTile(self.getPos()) and "lobby" not in self.biome:
            self.biome.append("lobby")
            pygame.event.post(pygame.event.Event(events.RUN_TUTORIAL, stage=0))
        
        elif "crystal" in self.world.getGroupsWithTile(self.getPos()) and "crystal" not in self.biome: 
            self.biome.append("crystal")
            pygame.event.post(pygame.event.Event(events.RUN_TUTORIAL, stage=1))

        elif "swamp" in self.world.getGroupsWithTile(self.getPos()) and "swamp" not in self.biome: 
            self.biome.append("swamp")
            pygame.event.post(pygame.event.Event(events.RUN_TUTORIAL, stage=3))

        elif ("desert" in self.world.getGroupsWithTile(self.getPos()) or 
        "cooldesert" in self.world.getGroupsWithTile(self.getPos()) or 
        "hotdesert" in self.world.getGroupsWithTile(self.getPos()) or 
        "volcano" in self.world.getGroupsWithTile(self.getPos())) and "desert" not in self.biome:
            self.biome.append("desert")
            pygame.event.post(pygame.event.Event(events.RUN_TUTORIAL, stage=4))

        elif "mountain" in self.world.getGroupsWithTile(self.getPos()) and "mountain" not in self.biome: 
            self.biome.append("mountain")
            pygame.event.post(pygame.event.Event(events.RUN_TUTORIAL, stage=5))

        elif "arctic" in self.world.getGroupsWithTile(self.getPos()) and "arctic" not in self.biome: 
            self.biome.append("arctic")
            pygame.event.post(pygame.event.Event(events.RUN_TUTORIAL, stage=6))    

        elif "deepdark" in self.world.getGroupsWithTile(self.getPos()) and "deepdark" not in self.biome: 
            self.biome.append("deepdark")
            pygame.event.post(pygame.event.Event(events.RUN_TUTORIAL, stage=7))    

        elif "void" in self.world.getGroupsWithTile(self.getPos()) and "void" not in self.biome: 
            self.biome.append("void")
            pygame.event.post(pygame.event.Event(events.RUN_TUTORIAL, stage=8))    


    def insanityTick(self):
        intern_insanity = self.getAttribute("insanity")
        extern_insanity = 0
        
        for insanity_level in self.world.getTileExtrasFromGroups(self.pos, "insanity_level", 0):
            extern_insanity += insanity_level

        if extern_insanity > intern_insanity:
            # insanity goes up to full in 20 seconds
            self.setAttribute("insanity", intern_insanity + 1/60/self.getAttribute("insanity_progress_speed"))

        if extern_insanity < intern_insanity:
            # insanity drops in 5 seconds
            self.setAttribute("insanity", intern_insanity - 1/60/self.getAttribute("insanity_regen_speed"))

    def thirstTick(self):
        pass

    def getAttributeTickers(self):
        return [self.temperatureTick,
                self.vibesTick,
                self.hungerTick,
                self.oxygenTick,
                self.fatigueTick,
                self.insanityTick,
                self.thirstTick]

    def tickAllAttributes(self):
        for attribute_ticker in self.getAttributeTickers():
            attribute_ticker()

    def tick(self):
        super().tick()
        self.inventory.tick(self, self.world)
        # print(self.pos)
        self.tickAllAttributes()

    def movementTick(self):
        super().movementTick()
        
        self.FOVobstruction()
        self.handleMotion()
        self.updateFacing()
        
    def damageTick(self):
        super().damageTick()

        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 2):
            if entity.isItemEntity():
                self.inventory.addItemStack(entity.stack)
                entity.kill()
            
        self.inventory.damageTick(self, self.world)
        
    def finalTick(self):
        super().finalTick()
        
        self.checkBiome()

        self.inventory.finalTick(self, self.world)
        
    def move(self, delta):
        super().move(delta)
        
        self.world.registerChange()

    def getMovementSpeed(self):
        return self.getAttribute("movement_speed")

    def setMovementSpeed(self, speed):
        self.setAttribute("movement_speed", speed)

    def handleMotion(self):
        if self.isCooldownActive("movement_input"):
            return

        self.prev_pos = [self.pos[0], self.pos[1]]

        moved = False

        pressed = pygame.key.get_pressed()
        if pressed[GAME.CONTROLS_KEYS["up"]]:
            self.move(( 0, -1))
            moved = True
        if pressed[GAME.CONTROLS_KEYS["left"]]:
            self.move((-1,  0))
            moved = True
        if pressed[GAME.CONTROLS_KEYS["down"]]:
            self.move(( 0,  1))
            moved = True
        if pressed[GAME.CONTROLS_KEYS["right"]]:
            self.move(( 1,  0))
            moved = True

        if not self.world.isTileValidForWalking(self.pos):
            self.pos = self.prev_pos
            return

        if moved:
            self.registerCooldown("movement_input", self.getMovementSpeed())
            self.world.setMovingAnimation(self.movement_this_tick, lambda:self.getCooldownFrame("movement_input"))

    def updateFacing(self):
        if self.movable:
            mouse_loc = self.world.bufferPosToTilePos(self.manager.screenPosToBufferPos(pygame.mouse.get_pos()))
            angle = math.atan2(mouse_loc[1]-self.pos[1], mouse_loc[0]-self.pos[0])-45

            self.facing = math.degrees(angle)

    def getFacing(self):
        return self.facing

    def onKeyDown(self, key, unicode, mod):
        if key == GAME.CONTROLS_KEYS["inventory right"]:
            self.inventory.changeSelectedStack(1)
        if key == GAME.CONTROLS_KEYS["inventory left"]:
            self.inventory.changeSelectedStack(-1)
        if key == GAME.CONTROLS_KEYS["throw"]:
            self.inventory.throwSelectedStack(self.world, self.pos)
            
    def onMouseDown(self, pos, button):
        # If anything uses the button, player will hog mouse input
        used = 0
        
        used += int(self.hud.onMouseDown(pos, button))
        
        return bool(used)

    def worldClosed(self):
        self.inventory.close()
        
    def kill(self):
        self.alive = False
        # pass
        # pygame.event.post(pygame.event.Event(events.RETURN_TO_MAIN_MENU))
        GAME.BOSS_CONDITIONS.setBossFirstMove(True)
        GAME.BOSS_CONDITIONS.setCooldownFirstMove(True)
        if self.manager.getWorld().world_name == "bossarena" and GAME.BOSS_CONDITIONS.getCraneAlive() == False:
            crane = GAME.BOSS_CONDITIONS.getCrane()
            crane.setPos([30,30])

        self.manager.changeWorld("overworld")
        self.setPos([461, 470])

        self.initAttributes()
            
    def getMapDelta(self):
        bpos = self.getBufferPos()
        return (-bpos[0], -bpos[1])

    def draw(self, display):
        pos = self.manager.bufferPosToScreenPos(self.getBufferPos())
        player_texture = self.atlas.getTexture("player1")

        rotated_texture = pygame.transform.rotate(player_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=pos)
        display.blit(rotated_texture, rotated_rect.center)

        self.hud.draw(display)
        

class PlayerHUD(events.EventAcceptor):
    TOPLEFT_BAR_BOUNDS = pygame.Rect((10, 10), (400, 30))
    INVENTORY_POS = (1600, 100)
    BAR_BACKGROUND = (40, 40, 40)
    
    def __init__(self, player):
        self.player = player

        self.item_rot = 0

    def onMouseDown(self, pos, button):
        used = 0
        
        # Inventory
        used += int(self.player.inventory.onMouseDown(pos, button, self.INVENTORY_POS))

        return bool(used)

    def drawBars(self, surface):
        topleft = self.TOPLEFT_BAR_BOUNDS

        x, y = self.TOPLEFT_BAR_BOUNDS.topleft
        
        for bar_data in self.player.getBarDataGetters():
            fullness, colour = bar_data()

            self.drawBar(surface, fullness, colour, (x, y))

            y += topleft.height

    def drawBar(self, surface, fullness, colour, pos):
        size = self.TOPLEFT_BAR_BOUNDS.size

        fullness = min(1, max(0, fullness))

        # Background
        pygame.draw.rect(surface, self.BAR_BACKGROUND, (pos, size))

        # Bar
        pygame.draw.rect(surface, colour, pygame.Rect(pos, (size[0]*fullness, size[1])))

    def drawInventory(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        self.player.inventory.draw(surface, self.INVENTORY_POS)
        self.player.inventory.drawActiveStack(surface, mouse_pos)

        self.drawHandHeld(surface)

    def drawHandHeld(self, surface):
        stack = self.player.inventory.getSelectedStack()

        if stack:
            pos = self.player.manager.bufferPosToScreenPos(self.player.getBufferPos())
            stack.drawInWorld(surface,
                                   (pos[0]+self.player.world.TILE_SIZE[0]//2,
                                    pos[1]+self.player.world.TILE_SIZE[1]//2))
        
    def draw(self, surface):
        self.drawBars(surface)
        self.drawInventory(surface)
