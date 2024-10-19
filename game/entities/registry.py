import os

from .defs import ALL_ENTITY_CLASSES
from misc.textures import TextureAtlas

ASSETS = os.path.join("assets", "game")

def initialiseEntities():
    registerAllEntities()
    REGISTRY.loadAtlas()

def registerAllEntities():
    for entity_class in ALL_ENTITY_CLASSES:
        REGISTRY.registerEntityClass(entity_class)

class EntityRegistry:
    def __init__(self):
        self.entity_classes = []

        self.assets_needed = []

        self._atlas_loaded = False

    def loadAtlas(self):
        self.atlas = TextureAtlas(os.path.join(ASSETS, "entities"),
                                  ".png",
                                  (64, 64),
                                  self.assets_needed,
                                  True,
                                  True)

        self._atlas_loaded = True

        self.loadAtlasToEntities()

    def loadAtlasToEntities(self):
        if not self._atlas_loaded:
            raise RuntimeError("Entity registry texture atlas not loaded yet")
        
        for entity in self.entity_classes:
            entity.setAtlas(self.atlas)

    def registerEntityClass(self, entity):
        self.entity_classes.append(entity)
        
        assets = entity.getNeededAssets()
        self.assets_needed += assets

REGISTRY = EntityRegistry()
