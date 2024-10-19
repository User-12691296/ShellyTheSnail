import pygame
import os
import json

from pygame.constants import BUTTON_LEFT as BUTTON_LEFT
import pygame

from .world import LOADABLE_WORLDS
from misc import events
from .items import initialiseItems
from .entities import initialiseEntities, ENTITY_CLASSES
from .projectiles import initialiseProjectiles, PROJECTILE_CLASSES
from .world import initialiseWorlds

from constants import GAME
from constants import assets


ASSETS = os.path.join("assets", "game")

PAUSE_FONT = pygame.font.Font(os.path.join(assets.FONT_PATH, assets.NOTABLE_FONT), 70)
PAUSE_TITLE_FONT = pygame.font.Font(os.path.join(assets.FONT_PATH, assets.NOTABLE_FONT), 100)
RETURN_FONT = pygame.font.Font(os.path.join(assets.FONT_PATH, assets.NOTABLE_FONT), 40)


class ExitButton(events.ButtonShell):
    def __init__(self, action, button=pygame.BUTTON_LEFT):
        super().__init__(action, button)
        self.font = PAUSE_FONT.render("Exit to Menu", False, "white")
        self.name = "Exit to Menu"
        self.rect = self.font.get_rect()
        self.font = PAUSE_FONT

    def draw(self, surface):
        self.rect.center = (surface.get_width()/2, surface.get_height()/2+100)
        option_text = self.font.render(self.name, False, (255,255,255))
        if self.hovered:
            option_text = self.font.render(self.name, False, (220,220,220))
        if self.pressed:
            option_text = self.font.render(self.name, False, (100,100,100))
        surface.blit(option_text, (self.rect.topleft))


DEFAULT_WORLD = "overworld"
# world_set = [["overworld", [1,1]], ["level_1", [1,1]], ["crystal_level", [10,50]], ["deep_dark_level", [125,15]], ["maze_level", [1,1]], ["level_3", [1,1]]]
world_set = [["overworld", [1,1]], ["level_1", [1,1]], ["crystal_level", [10,50]], ["deep_dark_level", [125,15]], ["level_3", [100,10]], ["bossarena", [10,10]]]

class GameManager(events.Alpha):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        initialiseItems(ENTITY_CLASSES.ItemEntity)
        initialiseEntities()
        initialiseProjectiles()
        initialiseWorlds()
        
        self.loadBgs()
        self.loadWorlds()
        self.loadPlayer()
        self.finaliseWorlds()

        self.paused = False
        self.pause_exit = ExitButton(self.exitButtonAction)
        self.died = False

        self.first = True

        self.won = False

    def exitButtonAction(self):
        if self.won:
            GAME.BOSS_CONDITIONS.reset()
        self.paused = False
        self.player.setAttribute("health", self.player.getAttribute("max_health"))
        self.died = False
        self.won = False
        self.player.kill()
        self.player.alive = True
        self.first_tick()

        pygame.event.post(pygame.event.Event(events.RETURN_TO_MAIN_MENU))

    def loadWorlds(self):
        self.worlds = {}
        for world in LOADABLE_WORLDS:
            self.worlds[world.world_name] = world()
        
        self.active_world = DEFAULT_WORLD

    def loadBgs(self):
        self.bg = pygame.Surface(self.screen_size)
        self.bg.fill((0, 0, 0))

    def loadPlayer(self):
        self.player = ENTITY_CLASSES.Player()
        self.player.setManager(self)
        self.player.setWorld(self.getWorld())

    def finaliseWorlds(self):
        for world in self.worlds.values():
            world.setPlayer(self.player)

    def getWorld(self):
        return self.worlds[self.active_world]

    def changeWorld(self, world_name):
        self.active_world = world_name
        self.player.setWorld(self.getWorld())
        if world_name == "bossarena" and not GAME.BOSS_CONDITIONS.getCraneAlive():
            self.player.world.addEntity(GAME.BOSS_CONDITIONS.getCrane())
            GAME.BOSS_CONDITIONS.setCraneAlive(True)



    ## HELPER
    def getScreenBufferDelta(self):
        player_delta = self.player.getMapDelta()
        center_delta = (self.screen_size[0]//2, self.screen_size[1]//2)
        return (player_delta[0]+center_delta[0], player_delta[1]+center_delta[1])
    
    def screenPosToBufferPos(self, spos):
        delta = self.getScreenBufferDelta()
        return (spos[0]-delta[0], spos[1]-delta[1])

    def bufferPosToScreenPos(self, bpos):
        delta = self.getScreenBufferDelta()
        return (bpos[0]+delta[0], bpos[1]+delta[1])

    def switchPause(self):
        self.paused = not self.paused

    ## TICK
    def first_tick(self):
        self.player.tick()
        self.getWorld().tick()
    
    def main_tick(self):
        if not self.paused:
            self.player.movementTick()
            self.getWorld().movementTick()

            self.player.damageTick()
            self.getWorld().damageTick()

            self.player.finalTick()
            self.getWorld().finalTick()
            if not self.player.alive:
                self.died = True
                self.paused = True

            self.won = GAME.BOSS_CONDITIONS.hasWon()
            if self.won:
                self.paused = True
    
    ## EVENTS
    def start(self):
        print("Game starting!")
        self.won = False
        
        self.player.setAttribute("health", self.player.getAttribute("max_health"))
        self.player.alive = True
        self.first_tick()

        if self.first:
            self.runTutorial(0) #Initial
            self.first = False

    def runTutorial(self, stage):
        pygame.event.post(pygame.event.Event(events.RUN_TUTORIAL, stage=stage))

    def onKeyDown(self, key, unicode, mod):
        global world_set, world_counter

        if key == GAME.CONTROLS_KEYS["pause"] and not self.died:
            self.switchPause()

        if not self.paused:
            
            self.player.onKeyDown(key, unicode, mod)
            self.getWorld().onKeyDown(key, unicode, mod)

                
    def onKeyUp(self, key, unicode, mod):
        if self.paused:
            return
        self.player.onKeyUp(key, unicode, mod)
        self.getWorld().onKeyUp(key, unicode, mod)
        
    def onMouseMotion (self, spos):
        if self.paused:
            self.pause_exit.onMouseMotion(spos)

    def onMouseDown(self, spos, button):      
        if self.paused:
            self.pause_exit.onMouseDown(spos, button)
            return  
        used = self.player.onMouseDown(spos, button)
        if not used:
            bpos = self.screenPosToBufferPos(spos)
            self.getWorld().onMouseDown(bpos, button)

    def onMouseUp(self, spos, button):    
        if self.paused:
            self.pause_exit.onMouseUp(spos, button)
            return    
        used = self.player.onMouseUp(spos, button)
        if not used:
            bpos = self.screenPosToBufferPos(spos)
            self.getWorld().onMouseUp(bpos, button)

    def close(self):
        self.player.worldClosed()
    
    ## DRAW
    def draw(self, surface):
        if self.won:
            self.drawVictoryScreen(surface)
            return
        elif self.died:
            self.drawDeathMenu(surface)
            return
        elif self.paused:
            self.drawPauseMenu(surface)
            return
        self.drawBg(surface)
        self.drawWorld(surface)
        self.drawPlayer(surface)

    def drawBg(self, surface):
        surface.blit(self.bg, (0, 0))

    def drawPauseMenu(self, surface):
        surface.blit(PAUSE_TITLE_FONT.render("Paused", True, (255,255,255)), (surface.get_width()/2-PAUSE_TITLE_FONT.size("Paused")[0]/2, (surface.get_height()/2-PAUSE_TITLE_FONT.size("Paused")[1]/2-100)))
        message = f'Please Press {pygame.key.name(GAME.CONTROLS_KEYS["pause"])} to unpause.'
        surface.blit(RETURN_FONT.render(message, True, "white"), (surface.get_width()/2-RETURN_FONT.size(message)[0]/2,surface.get_height()-100))
        self.pause_exit.draw(surface)

    def drawDeathMenu(self, surface):
        message = "YOU'VE LOST, PLEASE EXIT THE GAME"
        surface.blit(PAUSE_TITLE_FONT.render(message, True, (255,255,255)), (surface.get_width()/2-PAUSE_TITLE_FONT.size(message)[0]/2, (surface.get_height()/2-PAUSE_TITLE_FONT.size(message)[1]/2-100)))
        self.pause_exit.draw(surface)

    def drawVictoryScreen (self, surface):
        message = "YOU'VE WON!! PLEASE EXIT THE GAME!!"
        surface.blit(PAUSE_TITLE_FONT.render(message, True, (255,255,255)), (surface.get_width()/2-PAUSE_TITLE_FONT.size(message)[0]/2, (surface.get_height()/2-PAUSE_TITLE_FONT.size(message)[1]/2-100)))
        self.pause_exit.draw(surface)


    def drawWorld(self, surface):
        viewing_rect = pygame.Rect(self.getScreenBufferDelta(), self.screen_size)
        self.getWorld().draw(surface, viewing_rect)

    def drawPlayer(self, surface):
        self.player.draw(surface)

