from .basic import BasicTile

class BarrierTile(BasicTile):
    def __init__(self):
        super().__init__("barrier", "barrier", False)
