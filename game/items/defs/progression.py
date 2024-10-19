from ..classes import Item

class MagmaWalker(Item):
    def __init__(self):
        super().__init__("red_protection", "red_protection", True, 0)


PROGRESSIONS = []
MagmaWalker().addToGroup(PROGRESSIONS)
