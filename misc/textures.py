import pygame
import os


def getAllXFilesInFolder(folder, ext):
    files = os.listdir(folder)
    for file in files:
        if file.endswith(ext):
            yield file.removesuffix(ext)


class TextureAtlas:
    def __init__(self, path, ext, texture_size, asset_list, rescale=False, transparency=False):
        self.path = path
        self.ext = ext
        self.size = texture_size
        self.asset_list = tuple(asset_list)
        self.rescale = rescale
        self.transparency = transparency

        self.default = 0

        self.createAtlas()

    @classmethod
    def fromPreset(cls, preset):
        try:
            rescale = preset.RESCALE
        except AttributeError:
            rescale = False
        
        try:
            transparency = preset.TRANSPARENCY
        except AttributeError:
            transparency = False
        
        return cls(preset.FOLDER,
                   preset.EXT,
                   (preset.SIZE, preset.SIZE),
                   getAllXFilesInFolder(preset.FOLDER, preset.EXT),
                   rescale = rescale,
                   transparency = transparency)

    def createAtlas(self):
        flags = 0
        if self.transparency:
            flags += pygame.SRCALPHA
            
        self.atlas = pygame.Surface((self.size[0]*len(self.asset_list), self.size[1]), flags)
        self.atlas.fill((0, 0, 0, 0))

        for i, asset_name in enumerate(self.asset_list):
            path = os.path.join(self.path, asset_name+self.ext)
            self.loadTexture(i, path)
        
    def loadTexture(self, loc, filepath):
        if not self.transparency:
            texture = pygame.image.load(filepath).convert()
        else:
            texture = pygame.image.load(filepath).convert_alpha()

        if self.rescale:
            texture = pygame.transform.scale(texture, self.size)

        self.atlas.blit(texture, (loc*self.size[0], 0))

    def getAtlas(self):
        return self.atlas

    def getTextureSize(self):
        return self.size
    
    def getTextureWidth(self):
        return self.size[0]

    def getTextureHeight(self):
        return self.size[1]

    def getTextureAtLoc(self, loc):
        return self.atlas.subsurface(pygame.Rect((self.size[0]*loc, 0), self.size))

    def getTextureLoc(self, asset_name):
        try:
            loc = self.asset_list.index(asset_name)
            return loc
        except ValueError:
            return self.default

    def getTexture(self, asset_name):
        return self.getTextureAtLoc(self.getTextureLoc(asset_name))

    def drawTextureAtLoc(self, surface, pos, loc):
        surface.blit(self.getTextureAtLoc(loc), pos)

    def drawTexture(self, surface, pos, asset_name):
        surface.blit(self.getTexture(asset_name), pos)
