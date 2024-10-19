from .item import ItemEntity
from ...entities import classes

class LanternEntity(ItemEntity):
    def __init__(self):
        super().__init__(classes.ItemStack("lantern", 1))
    