from ..classes import Item
from misc import animations
import math
import time
from constants import GAME

FRUIT_HUNGER_RESTORATION = 0.1

class Fruit(Item):
    #Note to self, add healing effect thru init
    # Fruits give a special status effect TBD
    def __init__(self, itemid, tex_name, size, heal_amount, effect_duration = 60):
        super().__init__(itemid, tex_name, True, size)
        self.heal_amount = heal_amount
        
        self.ticker = 0

        self.effect_time = 0
        self.effect_duration = effect_duration

    def effect(self, player, world, tile, tile_pos):
        pass

    def reverse_effect(self, player, world, tile, tile_pos):
        pass

    def onLeft(self, data, player, world, tile, tile_pos):
        player.changeHealth(self.heal_amount)
        self.effect(player, world, tile, tile_pos)
        player.changeHunger(FRUIT_HUNGER_RESTORATION)
        fruit = player.inventory.getItemStack(player.inventory.selected_slot)
        fruit.consume()


    def tick(self, data, player, world):
        data["animations"].tick()

class Watermelon (Item):
    def __init__(self, itemid, tex_name, size):
        super().__init__(itemid, tex_name, size)

    def onLeft(self, data, player, world, tile, tile_pos):
        insulation = player.getAttribute("thermal_insulation")
        insulation *= 1.2
        player.setAttribute("thermal_insulation", insulation)
        player.changeHunger(FRUIT_HUNGER_RESTORATION)
        fruit = player.inventory.getItemStack(player.inventory.selected_slot)
        fruit.consume()

class Lemon (Fruit):
    def __init__(self, itemid, tex_name, size, heal_amount, effect_duration):
        super().__init__(itemid, tex_name, size, heal_amount, effect_duration)

    def effect(self, player, world, tile, tile_pos):
        player.setMovementSpeed(GAME.PLAYER_WALKING_SPEED*0.5)
        player.giveEffect("speed", self.effect_duration, lambda x, y, z:None, self.reverse_effect)
        # player.giveEffect("testing", self.effect_duration+40, lambda x,y,z: print("hi"), lambda x,y,z:print("done"))

    def reverse_effect(self, player, world, player_tile_pos):
        player.setMovementSpeed(GAME.PLAYER_WALKING_SPEED)

class SilverFruit(Fruit):
    def __init__(self, itemid, tex_name, size, heal_amount, effect_duration, armor_points):
        super().__init__(itemid, tex_name, size, heal_amount, effect_duration)
        self.armor_points = armor_points
        self.original_armor_value = None
        self.original_dmg_threshold = None

    def effect(self, player, world, tile, tile_pos):
        self.original_armor_value = player.getArmorValues()[0]
        self.original_dmg_threshold = player.getArmorValues()[1]
        new_armor_value = self.original_armor_value + self.armor_points 
        player.setArmorValues(new_armor_value, self.original_dmg_threshold)

        player.giveEffect("defense", self.effect_duration, lambda x, y, z:None, self.reverse_effect)

    def reverse_effect(self, player, world, tile_pos):
        player.setArmorValues(self.original_armor_value, self.original_dmg_threshold)

FRUITS = []
Fruit("orange", "orange", 0, 1).addToGroup(FRUITS)
Fruit("banana", "banana", 0, 1).addToGroup(FRUITS)
Watermelon("watermelon", "watermelon", 0).addToGroup(FRUITS)
Fruit("apple", "apple", 0, 3).addToGroup(FRUITS)
Lemon("lemon", "lemon", 0, 1, 100).addToGroup(FRUITS)
SilverFruit("silver_apple", "silver_apple", 1, 100, 100, 10).addToGroup(FRUITS)
