from .playerarrows import BasicProjectileWithEffects, placeholderFunction

class BlueBolt(BasicProjectileWithEffects):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.4
        
        self.init_effect = self.ice_init_effect
        self.tick_effect = placeholderFunction
        self.reverse_effect = self.reverse_ice_effect

        self.effect_name = "BoltFrozen"
        self.effect_duration = 10

    def getNeededAssets():
        return ["LightningBoltBlue"]

    def ice_init_effect(self, entity, world, tile_pos):
        entity.setMovable(False)

    def reverse_ice_effect(self,entity,world,tile_pos):
        entity.setMovable(True)

    def draw(self, display, display_topleft=(0, 0)):    
        super().draw(display, display_topleft)

        self.stdDraw(display, "LightningBoltBlue", display_topleft)

class Bolt (BasicProjectileWithEffects):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.4
        
        self.init_effect = placeholderFunction
        self.tick_effect = self.molten_tick_effect
        self.reverse_effect = placeholderFunction

        self.effect_name = "BoltEmber"
        self.effect_duration = 15

    def getNeededAssets():
        return ["LightningBolt"]

    def molten_tick_effect(self, entity, world, tile_pos):
        entity.damage(0.3)

    def draw(self, display, display_topleft=(0, 0)):    
        super().draw(display, display_topleft)

        self.stdDraw(display, "LightningBolt", display_topleft)
  
MOUNTAINBOLTS = []
BlueBolt.addToGroup(MOUNTAINBOLTS)
Bolt.addToGroup(MOUNTAINBOLTS)