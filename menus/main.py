#i messed with this file icl
import pygame
from misc import events
from constants import *
import os

class MainMenuOption(events.ButtonShell):
    def __init__(self, name, center, action):
        super().__init__(action)
        
        self.name = name

        self.rect = pygame.Rect(0, 0, 800, 110) #(0,0,600,100)
        self.rect.center = center
        
        self.font = pygame.font.SysFont("Times New Roman", 200)
        self.hovered_font = pygame.font.SysFont("Times New Roman", 250)

    def draw(self, surface):
        if not self.hovered:
            option_text = self.font.render(self.name, True, (175, 105, 239))
        else:
            if not self.pressed:
                option_text = self.hovered_font.render(self.name, True, (155, 95, 209))
            else:
                option_text = self.hovered_font.render(self.name, True, (80, 50, 100))
        surface.blit(option_text, (self.rect.centerx-option_text.get_rect().centerx, self.rect.centery-option_text.get_rect().centery))

class MainMenu(events.Alpha):
    def __init__(self, screen_size):
        bg = pygame.image.load(os.path.join(ASSETS.MENU_PATH, ASSETS.MAIN_MENU_BG)).convert()
        self.bg = pygame.transform.scale(bg, screen_size)
        
        self.fonts = {}

        self.fonts["title"] = pygame.font.SysFont("Times New Roman", 600)


        self.options = {}
        option_names = ("  ", "        ", "     ") # ("Play", "Settings", "Exit")
        option_actions = [lambda: pygame.event.post(pygame.event.Event(events.GAME_START)),
                          lambda: pygame.event.post(pygame.event.Event(events.OPEN_SETTINGS)),
                          lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))]

        y = 850 #400 + 200
        
        for option_name, option_action in zip(option_names, option_actions):
            self.options[option_name] = MainMenuOption(option_name, (675, y), option_action) #600
            y += 180 #100

    def onMouseDown(self, pos, button):
        for option in self.options.values():
            option.onMouseDown(pos, button)

    def onMouseUp(self, pos, button):
        for option in self.options.values():
            option.onMouseUp(pos, button)
    
    def onMouseMotion(self, pos):
        for option in self.options.values():
            option.onMouseMotion(pos)

    def draw(self, surface):
        # Background
        surface.blit(self.bg, (surface.get_rect().centerx-self.bg.get_rect().centerx, 0))

        # Title
        title_text = self.fonts["title"].render(" ", True, (0, 0, 0))
        surface.blit(title_text, (1200, 750))

        # Options
        for option in self.options.values():
            option.draw(surface)
