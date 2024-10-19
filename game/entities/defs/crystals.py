import random

from ..classes import Entity

from constants import GAME

class HungerCrystal(Entity):
    def __init__(self):
        super().__init__()

    def movementTick(self):
        player = self.world.getPlayer()
        hunger = player.getAttribute("hunger")
        hunger += random.choice([-0.01,0.01])
        if hunger < 1 and hunger > 0.3:
            player.setAttribute("hunger", hunger)

class HeatCrystal(Entity):
    def __init__(self):
        super().__init__()

    def movementTick(self):
        player = self.world.getPlayer()
        temperature = player.getAttribute("temperature")
        temperature += random.choice([-0.1,0.1])
        if temperature < 1 and temperature > -1:
            player.setAttribute("temperature", temperature)

class MovementCrystal(Entity):
    def __init__(self):
        super().__init__()

    def movementTick(self):
        player = self.world.getPlayer()
        movement_speed = player.getAttribute("movement_speed")
        movement_speed += random.choice([-0.1,0.1])
        player.setAttribute("movement_speed", movement_speed)

CRYSTALS=[]

HungerCrystal.addToGroup(CRYSTALS)
HeatCrystal.addToGroup(CRYSTALS)
MovementCrystal.addToGroup(CRYSTALS)

