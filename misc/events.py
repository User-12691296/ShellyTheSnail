import pygame

RETURN_TO_MAIN_MENU = pygame.USEREVENT + 0
GAME_START = pygame.USEREVENT + 1
OPEN_SETTINGS = pygame.USEREVENT + 2
RUN_TUTORIAL = pygame.USEREVENT + 3



class EventAcceptor:
    def onMouseMotion(self, pos): pass
    def onMouseDown(self, pos, button): pass
    def onMouseUp(self, pos, button): pass
    def onKeyDown(self, key, mod, unicode): pass
    def onKeyUp(self, key, mod, unicode): pass


class Alpha(EventAcceptor):
    def first_tick(self): pass
    def main_tick(self): pass
    def start(self): pass
    def close(self): pass


class ButtonShell:
    def __init__(self, action, button=pygame.BUTTON_LEFT):
        self.button = button

        self.action = action
        
        self.hovered = False
        self.pressed = False

    def onMouseMotion(self, pos):
        if self.rect.collidepoint(pos):
            self.hovered = True
        else:
            self.hovered = False
            self.pressed = False

    def onMouseDown(self, pos, button):
        if button == self.button:
            if self.rect.collidepoint(pos):
                self.pressed = True

    def onMouseUp(self, pos, button):
        if button == self.button:
            if self.rect.collidepoint(pos) and self.pressed:
                self.pressed = False
                self.action()
