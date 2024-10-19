import pygame

class BasicTile:
    def __init__(self, tileid, tex_name, rscat=True):
        self.tileid = tileid
        self.tex_name = tex_name
        self.rscat = rscat

        self._atlas_given = False

    def addTileToList(self, tile_list):
        tile_list.append(self)

    def setAtlas(self, atlas):
        self.atlas = atlas

        self.tex_loc = self.atlas.getTextureLoc(self.tex_name)

        self._atlas_given = True

    def shouldRotationScatter(self):
        return self.rscat

    def getTileID(self):
        return self.tileid

    def onLeft(self, world, tile_pos): pass
    def onRight(self, world, tile_pos): pass
    def onWalk(self, world, tile_pos): pass

    def draw(self, surface, pos):
        if self._atlas_given:
            self.atlas.drawTextureAtLoc(surface, pos, self.tex_loc)

    def getDrawable(self):
        if self._atlas_given:
            return self.atlas.getTextureAtLoc(self.tex_loc)

        else:
            return pygame.Surface((1, 1))
