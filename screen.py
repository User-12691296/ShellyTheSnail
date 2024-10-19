# Create the fullscreen window which locks the game into 16:9 aspect ratio
import pygame
import ctypes
import platform
import os

if platform.system() == "Windows":
    ctypes.windll.user32.SetProcessDPIAware()

class Screen:
    def __init__(self, aspect, resolution):
        self.screen = pygame.display.set_mode((aspect*resolution, resolution), pygame.FULLSCREEN | pygame.SCALED | pygame.NOFRAME)
        pygame.display.set_caption("Shelly the Snail's Great Adventure")
        pygame.display.set_icon(pygame.image.load(os.path.join("assets", "menus", "flame.png")).convert())
        
        self.aspect = aspect
        self.screen_aspect = self.screen.get_width()/self.screen.get_height()

        self.resolution = resolution

        self._buffer_size = list(self.screen.get_size())
        
        if (self.screen_aspect-self.aspect)>0.01:
            self._buffer_size[1] = self.screen.get_height()
            self._buffer_size[0] = round(self._buffer_size[1]*aspect)
            
        elif (self.screen_aspect-self.aspect)<-0.01:
            self._buffer_size[0] = self.screen.get_width()
            self._buffer_size[1] = round(self._buffer_size[0]/aspect)

        self.buffer = pygame.Surface((self.resolution*aspect, self.resolution))

        self.center_delta = (self.screen.get_rect().centerx - self._buffer_size[0]//2,
                             self.screen.get_rect().centery - self._buffer_size[1]//2)
        
    def get(self):
        return self.buffer

    def get_size(self):
        return self.buffer.get_size()

    def update(self):
        self.screen.blit(self.buffer, self.center_delta)
        pygame.display.update()

    def translatePointFromScreen(self, point):
        temp = list(point)

        # Handle edge blackspace
        temp[0] -= self.center_delta[0]
        temp[1] -= self.center_delta[1]

        # Handle resolution diff
        res_delta = self.resolution/self._buffer_size[1]
        temp[0] *= res_delta
        temp[1] *= res_delta

        # Truncate decimals
        temp[0] = round(temp[0])
        temp[1] = round(temp[1])
        
        return temp

    def translatePointToScreen(self, point):
        temp = list(point)

        # Handle resolution diff
        res_delta = self.resolution/self._buffer_size[1]
        temp[0] /= res_delta
        temp[1] /= res_delta

        # Handle edge blackspace
        temp[0] += self.center_delta[0]
        temp[1] += self.center_delta[1]

        # Truncate decimals
        temp[0] = round(temp[0])
        temp[1] = round(temp[1])
        
        return temp
