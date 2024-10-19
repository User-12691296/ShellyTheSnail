from .basic import BasicTile
from ...entities import ENTITY_CLASSES
from ...projectiles import PROJECTILE_CLASSES

class SandDarkTile(BasicTile):
    def __init__(self):
        super().__init__("sanddark", "sanddark")