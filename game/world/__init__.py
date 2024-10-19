from .worldefs import LOADABLE_WORLDS
from .tilegroups import GROUP_MANAGER, initialiseTileGroups, SPAWNING_REGISTRY, initialiseSpawning

def initialiseWorlds():
    initialiseTileGroups()
    initialiseSpawning()
