import pygame
pygame.init()

import os, sys
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

from screen import Screen
# Create the screen
ASPECT_RATIO = 8/5
RESOLUTION = 1600
SCREEN = Screen(ASPECT_RATIO, RESOLUTION)

from managers import MainWindowManager
from misc import events
from constants.game import SOUND_VOLUMES

clean_close = False


# Load music
pygame.mixer.init()
pygame.mixer.music.load(os.path.join("assets", "sounds", "mainmenu.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0)
fade_in_cooldown = 0


# Reroutes events and drawing commands through a manager to clean the main code
main_manager = MainWindowManager(SCREEN)

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    # Tick before input 
    main_manager.first_tick()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        main_manager.handleEvent(event)

    pygame.mixer.music.set_volume(min(fade_in_cooldown/300, 1)*SOUND_VOLUMES["Music"]/200)
    fade_in_cooldown += 1
    
    # Tick after input
    main_manager.main_tick()

    # Draw to screen
    SCREEN.get().fill((0, 0, 0))

    main_manager.draw(SCREEN.get())
    
    SCREEN.update()

    # FPS control
    clock.tick(60)

pygame.quit()

