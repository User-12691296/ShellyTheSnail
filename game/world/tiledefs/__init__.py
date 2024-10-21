from .basic import BasicTile
from .grass import GrassTile
from .barrier import BarrierTile
from .sanddark import SandDarkTile
from .damaging import DamageTile
from .slowing import SlowTile
from .cactus import Cactus
from .void import WalkableVoidTile, DeathVoidTile
from .swampwater import SwampWater
from .lavaforge import VolcanoLava
from .lavaforge import VolcanoMolten
from .worldswitcher import WorldSwitcher


OVERWORLD_TILES = []
GrassTile().addTileToList(OVERWORLD_TILES)
BarrierTile().addTileToList(OVERWORLD_TILES)
SandDarkTile().addTileToList(OVERWORLD_TILES)
SwampWater().addTileToList(OVERWORLD_TILES)
VolcanoLava("volcanolava").addTileToList(OVERWORLD_TILES)
VolcanoLava("volcanomolten").addTileToList(OVERWORLD_TILES)
BasicTile("bloodstone", "bloodstone").addTileToList(OVERWORLD_TILES)
BasicTile("lobbyfloor", "lobbyfloor", False).addTileToList(OVERWORLD_TILES)
BasicTile("lobbywall", "lobbywall", False).addTileToList(OVERWORLD_TILES)


#texname and id is switched im sorry
WorldSwitcher("portal", "bossarena", "bossarena", [10,10], False).addTileToList(OVERWORLD_TILES)
WorldSwitcher("portal", "crystalwarp", "crystal_level", [10,50], False).addTileToList(OVERWORLD_TILES)
WorldSwitcher("portal", "snowwarp", "level_3", [100,10], False).addTileToList(OVERWORLD_TILES)
WorldSwitcher("portal", "deepdarkwarp", "deep_dark_level", [125,15], False).addTileToList(OVERWORLD_TILES)
WorldSwitcher("portal", "overworldwarp", "overworld", [461,470], False).addTileToList(OVERWORLD_TILES)
# 9999 turns into nothing, they js gonna go back to where they came from.

BasicTile("sand", "sand").addTileToList(OVERWORLD_TILES)
BasicTile("sandlight", "sandlight").addTileToList(OVERWORLD_TILES)
SlowTile("sandoasis", "sandoasis",2, False).addTileToList(OVERWORLD_TILES)
Cactus("sandcactus", "sandcactus", 0.1, 2).addTileToList(OVERWORLD_TILES)


BasicTile("kr1stal", "kr1stal").addTileToList(OVERWORLD_TILES)
BasicTile("kr1stalfloor", "kr1stalfloor").addTileToList(OVERWORLD_TILES)
BasicTile("kr1stalrunes", "kr1stalrunes").addTileToList(OVERWORLD_TILES)

BasicTile("snow", "snow").addTileToList(OVERWORLD_TILES)
BasicTile("snow2", "snow2", False).addTileToList(OVERWORLD_TILES)

BasicTile("swamp", "swamp").addTileToList(OVERWORLD_TILES)
BasicTile("swampaccent", "swampaccent").addTileToList(OVERWORLD_TILES)
##SlowTile("swampwater", "swampwater",2).addTileToList(OVERWORLD_TILES)

BasicTile("deepdark", "deepdark", False).addTileToList(OVERWORLD_TILES)
BasicTile("darkwall", "darkwall", False).addTileToList(OVERWORLD_TILES)

BasicTile("mountain", "mountain").addTileToList(OVERWORLD_TILES)
BasicTile("mountainlight", "mountainlight").addTileToList(OVERWORLD_TILES)
BasicTile("mountainmoss", "mountainmoss").addTileToList(OVERWORLD_TILES)
BasicTile("mountainsnowmoss", "mountainsnowmoss").addTileToList(OVERWORLD_TILES)
BasicTile("mountainsnow", "mountainsnow").addTileToList(OVERWORLD_TILES)
BasicTile("shadowbrick", "shadowbrick", False).addTileToList(OVERWORLD_TILES)
BasicTile("icewall", "icewall", False).addTileToList(OVERWORLD_TILES)

BasicTile("volcano", "volcano").addTileToList(OVERWORLD_TILES)
# DamageTile("volcanolava", "volcanolava", 0.2, False).addTileToList(OVERWORLD_TILES)
# DamageTile("volcanomolten", "volcanomolten", 0.1).addTileToList(OVERWORLD_TILES)

WalkableVoidTile().addTileToList(OVERWORLD_TILES)
DeathVoidTile().addTileToList(OVERWORLD_TILES)

BasicTile("void", "barrier").addTileToList(OVERWORLD_TILES)
BasicTile("black", "black").addTileToList(OVERWORLD_TILES)


ALL_TILES = []
ALL_TILES += OVERWORLD_TILES
