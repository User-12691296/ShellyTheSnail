from .basic import BasicTile

SPEEDY_MAGMA_WALKING = "red_protection"

class WalkableVoidTile(BasicTile):
    def __init__(self):
        super().__init__("walkablevoid", "black", True)

    def onWalk(self, world, tile_pos):
        stack = world.getPlayer().inventory.getSelectedStack()

        if stack != None:
            if stack.getItemID() == SPEEDY_MAGMA_WALKING:
                world.getPlayer().setAttribute("movement_speed", 2)

class DeathVoidTile(BasicTile):
    def __init__(self):
        super().__init__("deathvoid", "deathvoid", True)

    def onWalk(self, world, tile_pos):
        player = world.getPlayer()

        player.kill()
