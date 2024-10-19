from ..classes import Item
from ...projectiles import PROJECTILE_CLASSES
from misc import animations

SWING_FRAMES = 10

class Armor(Item):
    def __init__(self, itemid, tex_name, size, armor_points, dmg_threshold, ticksthreshold=60):
        super().__init__(itemid, tex_name, False, size)
        self.armor_points = armor_points
        self.dmg_threshold = dmg_threshold
        self.tickthreshold = ticksthreshold
        self.equiped = False 
        self.ticks = 0 

    def getItemID(self):
        return self.itemid

    def equip(self, player):
        player.setArmorValues(self.armor_points, self.dmg_threshold)
        self.equiped = True

    def unequip(self, player):
        player.setArmorValues(0, 0)
        self.equiped = False

    def effect (self, data, player, world, tile_pos, tile): 
        pass

    def isArmor(self):
        return True

    def tick(self, data, player, world):
        if self.equiped:
            self.ticks += 1
            if self.ticks == self.tickthreshold:
                self.effect(data, player, world, player.pos, world.getTile(player.pos))
                self.ticks = 0

        data["animations"].tick()

class MaceArmor (Armor): 
    def __init__(self, itemid, tex_name, size, armor_points, dmg_threshold, tickthreshold=60, amount_of_projectiles=8, laser = PROJECTILE_CLASSES.DarknessMaceProj, cooldown=0):
        super().__init__(itemid, tex_name, size, armor_points, dmg_threshold)
        self.angles = []
        self.amount_of_projectiles = amount_of_projectiles

        for i in range (self.amount_of_projectiles):
            self.angles.append((360/self.amount_of_projectiles)*i)

        self.laser = laser
        self.cooldown = cooldown

    def effect (self, data, player, world, tile_pos, tile):
        if not data["animations"].exists("cooldown"):
            for angle in self.angles:
                laser = self.laser(player.pos, -data["rot"] + angle)
                laser.giveImmunity(player)
                world.addProjectile(laser)
            data["animations"].create("cooldown", self.cooldown)

ARMORS = []
Armor("iron_helmet", "iron_helmet", 0, 3.8, 10).addToGroup(ARMORS)
Armor("croc", "croc", 0, 2.4, 10).addToGroup(ARMORS)
Armor("swamp_armor", "swamp_armor", 0, 2.9, 10).addToGroup(ARMORS)
MaceArmor("crystal_armor", "crystal_armor", 0, 3.5, 10, 300, 8, PROJECTILE_CLASSES.CrystalMaceProj).addToGroup(ARMORS)
Armor("arctic_armor", "arctic_armor", 0, 4.5, 10).addToGroup(ARMORS)
MaceArmor("deepdark_armor", "deepdark_armor", 0, 4.8, 10, 300, 8, PROJECTILE_CLASSES.DarknessMaceProj).addToGroup(ARMORS)
MaceArmor("dragon_hide", "dragon_hide", 0, 5.5, 10, 300, 8, PROJECTILE_CLASSES.MoltenMaceProj).addToGroup(ARMORS)
