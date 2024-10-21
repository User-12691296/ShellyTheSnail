import pygame
import os
from misc import events
from game.entities.registry import REGISTRY as ENTITY_REGISTRY
from game.items import getRegistry as ITEM_REGISTRY_GETTER
from game.projectiles.registry import REGISTRY as PROJECTILE_REGISTRY

FOLDER = "tutorial"
FILEPATH = os.path.join(FOLDER, "tutorial.tuto")

class TutorialManager(events.Alpha):
    CHAR_LIMIT = 1
    MAX_CHARS = 10
    SHAPES_LIMIT = 4
    TILES_LIMIT = 2
    ENTITIES_LIMIT = 2
    ITEMS_LIMIT = 2
    COMMAND_LIMIT = 3
    LAYERS = 1
    LAYER_SWITCHING = False
    LAYER_SIZE = [640, 400]
    IMAGES = 0
    IMAGE_COOLDOWN = 50
    TILES_LOADED = False
    ENTITIES_LOADED = False
    ITEMS_LOADED = False
    LAYER_SHIFT_SIZE = 10
    LAYERS_FLIPPABLE = False
    LAYERS_ROTATABLE = False
    
    def __init__(self, screen_size):
        global FILEPATH

        self.LAYER_SIZE = [screen_size[0]//4, screen_size[1]//4]

        self.max_frames = 600*60

        self.pause_before_return = 0
        self.cooldown_to_return = -1

        self.fonts = [pygame.font.SysFont("monospaced", s) for s in [12, 18, 24, 36]]
        
        self.filedata = open(FILEPATH, "rt").readlines()
        self.filedata = [command.strip() for command in self.filedata]
        
        try:
            header_start = self.filedata.index("#HEADER")
            frames_start = self.filedata.index("#FRAMES")
        except ValueError:
            raise ValueError("Improper Tutorial Formatting")
            
        self.header = self.filedata[header_start:frames_start]
        self.frames = self.filedata[frames_start:]
        self.frame_counter = 0
        self.cur_frame = 0
        self.last_frame_in_stage = len(self.frames)-1

        self.stages = ["INITIAL",
                       "LOBBY",
                       "DUNGEON",
                       "SWAMP",
                       "DESERT",
                       "MOUNTAINS",
                       "ARCTIC",
                       "DARKNESS",
                       "VOID",
                       "FINAL"]

        self.packages = []
        self.package_loaders = {"clear":self.loadClear,
                                "advanced":self.loadAdvanced,
                                "elite":self.loadElite,
                                "comprehensive":self.loadComprehensive,
                                "talkative":self.loadTalkative,
                                "shapes":self.loadShapes,
                                "tiles":self.loadTiles,
                                "entities":self.loadEntities,
                                "items":self.loadItems,
                                "regions":self.loadRegions,
                                "control":self.loadControl}
        
        self.commands = {"clear":self.cmdClear,
                         "drawrect":self.cmdDrawRect,
                         "drawchar":self.cmdDrawChar,
                         "drawentity":self.cmdDrawEntity,
                         "drawitem":self.cmdDrawItem,
                         "switchlayer":self.cmdSwitchLayers,
                         "shiftlayer":self.cmdShiftLayers,
                         "drawellipse":self.cmdDrawEllipse,
                         "drawpolygon":self.cmdDrawPoly,
                         "drawtile":self.cmdDrawTile,
                         "flipdisp":self.cmdFlip,
                         "rotatedisp":self.cmdRot,
                         "clampregion":self.cmdClampRegion}

        self.parseHeader()

        self.layers = [pygame.Surface(self.LAYER_SIZE) for _ in range(self.LAYERS)]
        self.active_layer = 0
        self.layer_offset = [0, 0]

        self.chars_this_tick = 0
        self.chars_since_clear = 0
        self.shapes_this_tick = 0
        self.entities_this_tick = 0
        self.tiles_this_tick = 0
        self.items_this_tick = 0

        self.flips = [False, False]
        self.rot = 0

        self.layer_drawn_region = pygame.Rect((0, 0), self.LAYER_SIZE)

    def setGameManager(self, game_manager):
        self.game_manager = game_manager

    def start(self, stage):
        self.cooldown_to_return = -1
        self.cur_frame = self.frames.index("#" + self.stages[stage]) + 1

        if stage + 1 < len(self.stages):
            self.last_frame_in_stage = self.frames.index("#" + self.stages[stage+1]) - 1

        else:
            self.last_frame_in_stage = len(self.frames) - 1

    def returnToGame(self):
        pygame.event.post(pygame.event.Event(events.GAME_START))

    def onKeyDown(self, key, mod, unicode):
        if key == pygame.K_ESCAPE:
            self.returnToGame()
        
    def drawActiveLayerToSurface(self, surface):
        temp = self.getActiveLayer()
        temp = pygame.transform.flip(temp, *self.flips)
        temp = pygame.transform.rotate(temp, self.rot)
        region = pygame.Rect(self.layer_drawn_region.left*4,
                             self.layer_drawn_region.top*4,
                             self.layer_drawn_region.width*4,
                             self.layer_drawn_region.height*4)
        surface.blit(pygame.transform.scale_by(temp, 4), self.layer_offset, region)
        
    def draw(self, surface):
        if self.cooldown_to_return > 0:
            self.drawActiveLayerToSurface(surface)
            self.cooldown_to_return -= 1
            return
        elif self.cooldown_to_return == 0:
            self.returnToGame()
            return

        self.chars_this_tick = 0
        self.shapes_this_tick = 0
        self.entities_this_tick = 0
        self.tiles_this_tick = 0
        self.items_this_tick = 0
        
        leading_frame = self.cur_frame

        commands = []
        try:
            trailing_frame = leading_frame + self.frames[leading_frame+1:self.last_frame_in_stage+1].index("#frame")
        except ValueError:
            trailing_frame = self.last_frame_in_stage
        self.runCommands(self.frames[leading_frame+1:trailing_frame+1])

        self.drawActiveLayerToSurface(surface)

        self.cur_frame = trailing_frame + 1
        if self.cur_frame > self.last_frame_in_stage:
            self.cooldown_to_return = self.pause_before_return
        
    def parseHeader(self):
        li = 1
        for line in self.header:
            args = line.split(" ")

            if args[0] == "buy":
                try:
                    self.package_loaders[args[1]]()
                except ValueError as e:
                    raise ValueError(e + " LINE %d" % li)

            if args[0] == "pausebeforereturn":
                self.pause_before_return = int(args[1])
            
            li += 1

    def runCommands(self, commands):        
        self.frame_counter += 1
        assert self.frame_counter < self.max_frames, "Exceeded Maximum Time, Reduce Number of Frames"

        counter = 0
        for command in commands:
            counter += 1
            assert counter <= self.COMMAND_LIMIT
            
            specs = command.split(" ")
            cmd = specs[0]
            args = specs[1:]

            executable = self.commands[cmd]
            executable(*args)

    def timeCheck(self):
        if self.max_frames < 0:
            raise ValueError("No time available")

    def getActiveLayer(self):
        return self.layers[self.active_layer]

    def cmdClear(self, *args):
        if self.hasPackage("clear"):
            self.getActiveLayer().fill((int(args[0]), int(args[1]), int(args[2])))
        else:
            self.getActiveLayer().fill((0, 0, 0))

        self.chars_since_clear = 0

    def cmdDrawRect(self, *args):
        self.shapes_this_tick += 1
        assert self.shapes_this_tick <= self.SHAPES_LIMIT, "Exceeded shapes limit for this frame"
        
        bound = pygame.Rect((int(args[0]), int(args[1])),
                            (int(args[2])-int(args[0]), int(args[3])-int(args[1])))
        
        pygame.draw.rect(self.getActiveLayer(), (int(args[4]), int(args[5]), int(args[6])), bound)

    def cmdDrawChar(self, *args):
        text = args[0]

        self.chars_this_tick += len(text)
        assert self.chars_this_tick <= self.CHAR_LIMIT, "Exceeded chars limit for this frame"
        
        assert 1 <= len(text) <= self.CHAR_LIMIT , text+" not valid character sequence"

        pos = int(args[1]), int(args[2])
        if self.hasPackage("talkative"):
            font = self.fonts[int(args[3])]
            colour = [int(args[4]), int(args[5]), int(args[6])]
        else:
            font = self.fonts[1]
            colour = [int(args[3]), int(args[4]), int(args[5])]

        render = font.render(text, False, colour)
        self.getActiveLayer().blit(render, pos)

    def loadClear(self):
        self.max_frames -= 20
        self.timeCheck()

        self.packages.append("clear")
        
    def loadAdvanced(self):
        self.max_frames -= 60
        self.timeCheck()
        
        self.packages.append("advanced")

        self.LAYERS += 1
        self.LAYER_SIZE[0] = 2*self.LAYER_SIZE[0]
        self.LAYER_SIZE[1] = 2*self.LAYER_SIZE[1]
        self.PIXELS_LAYER = 2048

    def cmdSwitchLayers(self, *args):
        assert self.hasPackage("advanced"), "Package locked"

        self.active_layer = int(args[0])
        assert 0 <= self.active_layer < len(self.layers), "Not valid layer"
        self.layer_offset = [0, 0]
        self.rot = 0
        self.flips = [False, False]

        self.layer_drawn_region = pygame.Rect((0, 0), self.LAYER_SIZE)

    def cmdShiftLayers(self, *args):
        assert self.hasPackage("advanced") or self.hasPackage("control"), "Package locked"

        x = int(args[0])
        y = int(args[1])

        assert abs(x) <= self.LAYER_SHIFT_SIZE, "X shift too large"
        assert abs(y) <= self.LAYER_SHIFT_SIZE, "Y shift too large"

        self.layer_offset[0] += x
        self.layer_offset[1] += y

    def loadElite(self):
        self.max_frames -= 30
        self.timeCheck()

        self.packages.append("elite")
        
        self.LAYERS += 2
        

    def loadComprehensive(self):
        self.max_frames -= 30
        self.timeCheck()

        self.packages.append("comprehensive")

        self.COMMAND_LIMIT += 6
        

    def loadTalkative(self):
        self.max_frames -= 60
        self.timeCheck()

        self.CHAR_LIMIT += 4
        self.MAX_CHARS += 15

        self.packages.append("talkative")
        

    def loadShapes(self):
        self.max_frames -= 45
        self.timeCheck()

        self.SHAPES_LIMIT += 4

        self.packages.append("shapes")
        
    def cmdDrawEllipse(self, *args):
        assert self.hasPackage("shapes"), "Package locked"
        
        self.shapes_this_tick += 1
        assert self.shapes_this_tick <= self.SHAPES_LIMIT, "Exceeded shapes limit for this frame"

        bound = pygame.Rect((int(args[0]), int(args[1])),
                            (int(args[2])-int(args[0]), int(args[3])-int(args[1])))
        
        pygame.draw.ellipse(self.getActiveLayer(), (int(args[4]), int(args[5]), int(args[6])), bound)

    def cmdDrawPoly(self, *args):
        assert self.hasPackage("shapes"), "Package locked"
        
        self.shapes_this_tick += 1
        assert self.shapes_this_tick <= self.SHAPES_LIMIT, "Exceeded shapes limit for this frame"

        assert len(args)%2 == 1, "Poly points not valid format"
        assert len(args) >= 3, "Not enough information"

        points = [(args[i], args[i+1]) for i in range(len(args-3)//2)]

        colour_index_starts = len(args)-3
        
        pygame.draw.ellipse(self.getActiveLayer(), (int(args[colour_index_starts+0]),
                                                    int(args[colour_index_starts+1]),
                                                    int(args[colour_index_starts+2])), points)


    def loadEntities(self):
        self.max_frames -= 60
        self.timeCheck()

        self.packages.append("entities")

    def cmdDrawEntity(self, *args):
        assert self.hasPackage("entities"), "Package locked"

        self.entities_this_tick += 1
        assert self.entities_this_tick <= self.ENTITIES_LIMIT, "Exceeded entities limit for this frame"

        entity = args[0]
        pos = (int(args[1]), int(args[2]))

        ENTITY_REGISTRY.atlas.drawTexture(self.getActiveLayer(), pos, entity)


    def loadTiles(self):
        self.max_frames -= 45
        self.timeCheck()

        self.packages.append("tiles")

    def cmdDrawTile(self, *args):
        assert self.hasPackage("tiles"), "Package locked"
        
        self.tiles_this_tick += 1
        assert self.tiles_this_tick <= self.TILES_LIMIT, "Exceeded tiles limit for this frame"
        
        tile = args[0]
        pos = (int(args[1]), int(args[2]))
        
        self.game_manager.getWorld().map.tileAtlas.drawTexture(self.getActiveLayer(), pos, tile)


    def loadItems(self):
        self.max_frames -= 45
        self.timeCheck()

        self.packages.append("items")

    def cmdDrawItem(self, *args):
        assert self.hasPackage("items"), "Package locked"
        
        self.items_this_tick += 1
        assert self.items_this_tick <= self.ITEMS_LIMIT, "Exceeded items limit for this frame"

        sizes = {"small":0,
                 "s":0,
                 "medium":1,
                 "m":1,
                 "large":2,
                 "l":2}

        texsize = sizes[args[0]]
        item = args[1]
        pos = (int(args[2]), int(args[3]))
        
        ITEM_REGISTRY_GETTER().atlasses[texsize].drawTexture(self.getActiveLayer(), pos, item)


    def loadRegions(self, *args):
        self.max_frames -= 30
        self.timeCheck()

        self.packages.append("regions")

    def cmdClampRegion(self, *args):
        bound = pygame.Rect((int(args[0]), int(args[1])),
                            (int(args[2])-int(args[0]), int(args[3])-int(args[1])))
        
        self.layer_drawn_region = bound

    def loadControl(self, *args):
        self.max_frames -= 45
        self.timeCheck()
        
        self.packages.append("control")

        self.LAYER_SHIFT_SIZE += 10

    def cmdRot(self, *args):
        assert self.hasPackage("control")

        delta = float(args[0])
        assert abs(delta) < 10
        self.rot += delta

    def cmdFlip(self, *args):
        assert self.hasPackage("control")

        if args[0] == "X":
            self.flips[0] = not self.flips[0]
        if args[1] == "Y":
            self.flips[1] = not self.flips[1]
    
    def hasPackage(self, package):
        return package in self.packages
            

    
