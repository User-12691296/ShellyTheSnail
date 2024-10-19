import json
import os
import random
from ...entities import ENTITY_CLASSES as EC



SPAWNING_IDS = {"lava_knight": EC.DessertKnight,
                "desert_raiders": EC.DessertRaider,
                "desert_sandwurm": EC.DessertSandWurm,
                "desert_slime": EC.DessertSlime,
                
                "darknessbronze_barrel": EC.DarknessBronze,
                "darknesssilver_barrel": EC.DarknessSilver,
                "darknessgold_barrel": EC.DarknessGold,
                "darknessplatinum_barrel": EC.DarknessPlat,
                "frozenbronze_barrel": EC.FrozenBronze,
                "frozensilver_barrel": EC.FrozenSilver,
                "frozengold_barrel": EC.FrozenGold,
                "frozenplatinum_barrel": EC.FrozenPlat,
                "crystalbronze_barrel": EC.CrystalBronze,
                "crystalsilver_barrel": EC.CrystalSilver,
                "crystalgold_barrel": EC.CrystalGold,
                "crystalplatinum_barrel": EC.CrystalPlat,
                "dessertbronze_barrel": EC.DessertBronze,
                "dessertsilver_barrel": EC.DessertSilver,
                "dessertgold_barrel": EC.DessertGold,
                "dessertplatinum_barrel": EC.DessertPlat,
                "mountainbronze_barrel": EC.MountainBronze,
                "mountainsilver_barrel": EC.MountainSilver,
                "mountaingold_barrel": EC.MountainGold,
                "mountainplatinum_barrel": EC.MountainPlat,
                "swampbronze_barrel": EC.SwampBronze,
                "swampsilver_barrel": EC.SwampSilver,
                "swampgold_barrel": EC.SwampGold,
                "swampplatinum_barrel": EC.SwampPlat,

                "crystal_golem": EC.CrystalGolem,
                "crystal_knight": EC.CrystalKnight,
                "crystal_scorpion": EC.CrystalScorpion,
                "crystal_slime": EC.CrystalSlime,
                "crystal_bat": EC.CrystalBat,

                "darkness_ghost": EC.DarknessGhost,
                "darkness_gravetrapper": EC.DarknessGraveTrapper,
                "darkness_jumpscare": EC.DarknessJumpscare,
                "darkness_knightmare1": EC.DarknessKnightmare1,
                "darkness_knightmare2": EC.DarknessKnightmare2,
                "darkness_spreader": EC.DarknessSpreader,
                "darkness_bat": EC.DarknessBat,

                "frozen_knight": EC.FrozenKnight,
                "frozen_pufferfish": EC.FrozenPuffer,
                "frozen_troll": EC.FrozenTroll,
                "frozen_slime": EC.FrozenSlime,
                "frozen_wolf": EC.FrozenWolf,

                "swamp_anaconda": EC.SwampAnaconda,
                "swamp_otter": EC.SwampOtter,
                "swamp_tangler": EC.SwampTangler,
                "swamp_slime": EC.SwampSlime,
                
                "crab_boss": EC.CrabBoss,
                "medusa": EC.MedusaBoss,
                "dragon_boss": EC.DragonBoss,
                "worm_boss": EC.WormBoss,
                "mountain_boss": EC.MountainBoss,
                "darkness_boss": EC.DarknessBoss,

                "evil_snail": EC.EvilSnail,
                "whale_boss": EC.WhaleBoss,
                "crane_boss": EC.CraneBoss,
                "hunger_crystal": EC.HungerCrystal,

                "mountain_eagle": EC.MountainEagle,
                "mountain_slime": EC.MountainSlime,
                "mountain_goat": EC.MountainGoat,
                "mountain_golem": EC.MountainGolem,
                "mountain_troll": EC.MountainTroll,

                "lantern": EC.LanternEntity
}

SPAWNING_TABLES_FILE = os.path.join("game", "world", "tilegroups", "spawning.json")

def initialiseSpawning():
    with open(SPAWNING_TABLES_FILE) as file:
        SPAWNING_REGISTRY.setSpawningTables(json.load(file))

class SpawningRegistry:
    def __init__(self):
        self.tables = {}

    def setSpawningTables(self, tables):
        self.tables = tables

    def getEntityClass(self, spawning_id):
        return SPAWNING_IDS[spawning_id]

    def createSpawningInstructions(self, spawning_id, loc):
        inst = {}
        inst["loc"] = loc
        inst["class"] = self.getEntityClass(spawning_id)
        return inst

    def getWorldTable(self, world_name):
        return self.tables.get(world_name, {})

    def getFixedSpawningInstructions(self, world_name, general=True):
        instructions = []

        world = self.getWorldTable(world_name).get("fixed", {})

        for spawning_id in world.keys():
            for loc in world[spawning_id]:
                instructions.append(self.createSpawningInstructions(spawning_id, loc))
        
        if general:
            all_ = self.getWorldTable("all").get("fixed", {})

            for spawning_id in all_.keys():
                for loc in all_[spawning_id]:
                    instructions.append(self.createSpawningInstructions(spawning_id, loc))

        return instructions

    def getBiomeSpawn(self, biome, world_name, general=True, n=1):
        classes = []

        world = self.getWorldTable(world_name).get("biome", {})
        biome_data = world.get(biome, None)

        entities = {}

        if biome_data != None:            
            for spawning_id in biome_data.keys():
                entities[spawning_id] = entities.get(spawning_id, 0) + biome_data[spawning_id]['chance']

        if general:
            all_ = self.getWorldTable("all").get("biome", {})
            biome_data = all_.get(biome, None)

            if biome_data != None:
                for spawning_id in biome_data.keys():
                    entities[spawning_id] = entities.get(spawning_id, 0) + biome_data[spawning_id]['chance']


        if entities.keys():
            choices = random.choices([*entities.keys()], [*entities.values()], k=n)

            for choice in choices:
                classes.append(SPAWNING_IDS[choice])

        return classes

SPAWNING_REGISTRY = SpawningRegistry()
