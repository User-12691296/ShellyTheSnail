from .basic import BasicTile

class DamageTile(BasicTile):
    def __init__(self, tileid, tex_name, damage_value, rscat=True):
        super().__init__(tileid, tex_name, rscat)
        
        self.damage_value = damage_value
        
    def onWalk(self, world, tile_pos):
        player = world.getPlayer()
        damage = self.damage_value
        if player.inventory.getItemStack(24) != None:
            if player.inventory.getItemStack(-1).item.getItemID() == "dragon_hide" and "desert" in world.getGroupsWithTile(player.getPos()):
                damage = 0
        
        player.damage(damage)
