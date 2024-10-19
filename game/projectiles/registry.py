import os

from .defs import ALL_PROJECTILE_CLASSES
from misc.textures import TextureAtlas

ASSETS = os.path.join("assets", "game")

def initialiseProjectiles():
    registerAllProjectiles()
    REGISTRY.loadAtlas()

def registerAllProjectiles():
    for projectile_class in ALL_PROJECTILE_CLASSES:
        REGISTRY.registerProjectileClass(projectile_class)

class ProjectileRegistry:
    def __init__(self):
        self.projectile_classes = []

        self.assets_needed = []

        self._atlas_loaded = False

    def loadAtlas(self):
        self.atlas = TextureAtlas(os.path.join(ASSETS, "projectiles"),
                                  ".png",
                                  (48, 48),
                                  self.assets_needed,
                                  True,
                                  True)

        self._atlas_loaded = True

        self.loadAtlasToProjectiles()

    def loadAtlasToProjectiles(self):
        if not self._atlas_loaded:
            raise RuntimeError("Entity registry texture atlas not loaded yet")
        
        for projectile_class in self.projectile_classes:
            projectile_class.setAtlas(self.atlas)

    def registerProjectileClass(self, projectile):
        self.projectile_classes.append(projectile)
        
        assets = projectile.getNeededAssets()
        self.assets_needed += assets

REGISTRY = ProjectileRegistry()
