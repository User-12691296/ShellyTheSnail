import pygame

from misc.textures import TextureAtlas
from misc import events
from misc import animations

from constants import GAME

class Item(events.EventAcceptor):
    def __init__(self, itemid, tex_name, stackable=True, size=0):
        self.itemid = itemid
        self.tex_name = tex_name
        self.tex_size = size
        self.size = size
        self.stackable = stackable

        self.pivot_tc = GAME.ITEM_LOCATION_AROUND_PLAYER

        self._atlas_given = False

    def initData(self, stack):
        data = {"stack": stack,
                "rot": 0,
                "rarity": 0, # Level from 1-5, 1-3 is upgradable, 4 is craftable, 5 is endgame loot
                "animations": animations.Animated()}
        
        return data

    def addToGroup(self, group):
        group.append(self)

    def register(self, registry):
        registry.addItem(self)

    def setAtlas(self, atlas):
        self.atlas = atlas

        self.tex_loc = self.atlas.getTextureLoc(self.tex_name)

        self.pivot_tc = list(self.pivot_tc)
        self.pivot_tc[0] += self.atlas.getTextureWidth()//4
        self.pivot_tc[1] -= self.atlas.getTextureHeight()//4

        self._atlas_given = True

    def isStackable(self):
        return self.stackable

    def isUpgradeable(self):
        return False

    def getItemID(self):
        return self.itemid

    def tick(self, data, player, world): pass
    def damageTick(self, data, player, world): pass
    def finalTick(self, data, player, world): pass
    def select(self, data): pass
    def deSelect(self, data):
        data["animations"].clear()
    
    def onLeft(self, data, player, world, tile, tile_pos): return False
    def onRight(self, data, player, world, tile, tile_pos): return False
    def onMiddle(self, data, player, world, tile, tile_pos): return False

    def draw(self, surface, center):
        if self._atlas_given:
            item_drawing_bounds = pygame.Rect((0, 0), self.atlas.getTextureSize())
            item_drawing_bounds.center = center

            self.atlas.drawTextureAtLoc(surface, item_drawing_bounds.topleft, self.tex_loc)

    def drawRotated(self, surface, rot, center):
        tex = self.atlas.getTextureAtLoc(self.tex_loc)
        
        tex_rect = tex.get_rect(center=center)
        rot_pivot_tc = pygame.math.Vector2(self.pivot_tc).rotate(-rot)
        
        tbd = pygame.transform.rotate(tex, rot)
        tbd_rect = tbd.get_rect(center=(tex_rect.center[0]+rot_pivot_tc[0], tex_rect.center[1]+rot_pivot_tc[1]))
        
        surface.blit(tbd, tbd_rect.topleft)

    def isArmor(self):
        return False

    def drawInWorld(self, data, surface, center):
        self.drawRotated(surface, data.get("rot", 0), center)


class ItemStack:
    REGISTRY = None
    ITEM_COUNTER_FONT = pygame.font.SysFont("Courier New", 40)
    
    def __init__(self, itemid, count):
        self.item = self.REGISTRY.getItem(itemid)
        self.count = count

        self.initInstanceData()

    def initInstanceData(self):
        self.data = self.item.initData(self)

    @classmethod
    def setRegistry(self, registry):
        self.REGISTRY = registry

    def getItemID(self):
        return self.item.getItemID()

    def getCount(self):
        return self.count

    def isEmpty(self):
        return self.getCount()<=0

    def setCount(self, count):
        self.count = count

    def changeCount(self, delta):
        self.count += delta

    def consume(self):
        self.changeCount(-1)

    def tick(self, player, world):
        self.item.tick(self.data, player, world)

    def damageTick(self, player, world):
        self.item.damageTick(self.data, player, world)

    def finalTick(self, player, world):
        self.item.finalTick(self.data, player, world)

    def select(self):
        self.item.select(self.data)
    def deSelect(self):
        self.item.deSelect(self.data)

    def getRarity(self):
        return self.data.get("rarity", 0)
    
    def setRarity(self, rarity):
        self.data["rarity"] = rarity
        
    def upgradeRarity(self):
        if self.item.isUpgreadable():
            rarity = self.getRarity()
            
            if rarity < 3:
                rarity = rarity + 1
                
            self.setRarity(rarity)

    def onLeft(self, player, world, tile, tile_pos):
        return self.item.onLeft(self.data, player, world, tile, tile_pos)
    
    def onRight(self, player, world, tile, tile_pos):
        return self.item.onRight(self.data, player, world, tile, tile_pos)
    
    def onMiddle(self, player, world, tile, tile_pos):
        return self.item.onMiddle(self.data, player, world, tile, tile_pos)

    def isStackableWith(self, stack):
        if stack == None:
            return False
        
        if not self.item.isStackable():
            return False
        if not stack.item.isStackable():
            return False
        
        if self.getItemID() != stack.getItemID():
            return False

        return True

    def stackWith(self, stack):
        if self.isStackableWith(stack):
            self.count += stack.count

            return True

        else:
            return False

    def duplicateStack(self):
        new_stack = self.__class__(self.getItemID(), self.getCount())

        return new_stack

    def drawAsStack(self, surface, center):
        self.item.draw(surface, center)
        
        stack_amount = self.ITEM_COUNTER_FONT.render(str(self.count), True, (255, 255, 255))
        surface.blit(stack_amount, center)

    def drawInWorld(self, surface, center):
        self.item.drawInWorld(self.data, surface, center)
        

class Inventory(events.EventAcceptor):
    ItemEntityClass = None
    
    def __init__(self, size, width, grid_size, armor_slot = 24):
        self.size = size
        self.width = width
        self.height = round(self.size/self.width+0.4999999999)
        self.grid_size = grid_size
        self.armor_slot = armor_slot

        self.active_stack = None

        self.item_stacks = [None] * self.size

        self.thrown_stacks = []

    @classmethod
    def setItemEntityClass(cls, iecls):
        cls.ItemEntityClass = iecls

    def setItemStack(self, stack, loc):
        if self.size == 25:
            if self.getItemStack(loc) != None:
                if self.getItemStack(loc).item.isArmor():
                    self.getItemStack(loc).item.unequip(self.player) 

            if stack != None:  
                if loc == self.armor_slot and not stack.item.isArmor(): 
                    self.setActiveStack(stack)
                    return False
                
                elif loc == self.armor_slot and stack.item.isArmor():
                    stack.item.equip(self.player)
                    self.item_stacks[loc] = stack
                    return True
            
        self.item_stacks[loc] = stack

    def addItemStack(self, stack):
        if stack == None:
            return True
        
        added = False
        
        for stack_loc in range(self.size):
            if self.getItemStack(stack_loc) == None:
                self.setItemStack(stack, stack_loc)
                added = True
                break

            elif self.getItemStack(stack_loc).stackWith(stack):
                added = True
                break

        if added:
            return True
        else:
            self.thrown_stacks.append(stack)
            return False

    def getItemStack(self, loc):
        return self.item_stacks[loc]

    def isActiveStackClear(self):
        return self.getActiveStack() == None

    def isStackClear(self, loc):
        return self.getItemStack(loc) == None

    def getActiveStack(self):
        return self.active_stack

    def setActiveStack(self, stack):
        self.active_stack = stack

    def swapActiveWithStack(self, loc):
        temp = self.getActiveStack()
        self.setActiveStack(self.getItemStack(loc))
        self.setItemStack(temp, loc)

    def stackActiveWithStack(self, loc):
        stack = self.getItemStack(loc)

        if stack == None:
            self.swapActiveWithStack(loc)

        else:
            if stack.stackWith(self.getActiveStack()):
                self.setActiveStack(None)

            else:
                self.swapActiveWithStack(loc)

    def splitStackIntoActive(self, loc):
        # Get the current stack
        stack = self.getItemStack(loc)
        total_count = stack.getCount()

        # Calculate the amount before and after split
        remaining_count = total_count//2
        active_count = total_count - remaining_count

        if active_count > 0:
            active_stack = stack.duplicateStack()
            active_stack.setCount(active_count)
            self.setActiveStack(active_stack)
        
        if remaining_count > 0:            
            stack.setCount(remaining_count)
        else:
            self.setItemStack(None, loc)

    def getPosOfStack(self, loc, topleft):
        # Grid position of item stack
        grid = [0, 0]
        grid[0] = loc %  self.width
        grid[1] = loc // self.width

        # Position of item stack relative to square one
        rel_pos = [0, 0]
        rel_pos[0] = grid[0]*self.grid_size[0]
        rel_pos[1] = grid[1]*self.grid_size[1]

        # Position of item stack relative to top left of inventory
        rel_pos[0] += self.grid_size[0] // 2
        rel_pos[1] += self.grid_size[1] // 2

        # Absolute position of item stack
        pos = [0, 0]
        pos[0] = rel_pos[0] + topleft[0]
        pos[1] = rel_pos[1] + topleft[1]

        return pos

    def onMouseDown(self, ipos, button):
        # If mouse click outside of inventory bounds, quit
        if (ipos[0] < 0) or (ipos[1] < 0):
            return False
        if (ipos[0] >= self.width*self.grid_size[0]) or (ipos[1] >= self.height*self.grid_size[1]):
            return False

        # Get stack clicked on
        grid = [0, 0]
        grid[0] = ipos[0]//self.grid_size[0]
        grid[1] = ipos[1]//self.grid_size[1]

        stack_loc = grid[0] + self.width*grid[1]

        if stack_loc >= self.size:
            return False

        # If a split is possible, split, otherwise swap stack and active
        if button == pygame.BUTTON_RIGHT and self.isActiveStackClear() and not self.isStackClear(stack_loc):
            self.splitStackIntoActive(stack_loc)

        else:
            # Bring it to the active stack
            self.stackActiveWithStack(stack_loc)
        
        return True

    def tick(self, player, world):
        for stack in self.item_stacks:
            if stack:
                stack.tick(player, world)

    def damageTick(self, player, world):
        while self.thrown_stacks:
            self.throwStack(world, player.pos, self.thrown_stacks.pop(), 3)
            
        for stack in self.item_stacks:
            if stack:
                stack.damageTick(player, world)

    def finalTick(self, player, world):
        for stack in self.item_stacks:
            if stack:
                stack.finalTick(player, world)

        self.cullEmptyStacks()

    def cullEmptyStacks(self):
        for loc, stack in enumerate(self.item_stacks):
            if stack:
                 if stack.isEmpty():
                     self.setItemStack(None, loc)

    def close(self):
        self.addItemStack(self.active_stack)
        self.setActiveStack(None)

    def throwStack(self, world, pos, stack, throw_distance):
        stack_entity = self.ItemEntityClass(stack)
        stack_entity.placeInWorld(world, pos, throw_distance)

    def throwStackInLoc(self, world, pos, stack_loc, throw_distance):
        stack = self.getItemStack(stack_loc)
        
        if stack:
            self.throwStack(world, pos, stack, throw_distance)
            self.setItemStack(None, stack_loc)

    def draw(self, surface, topleft):
        for stack_loc in range(self.size):
            pos = self.getPosOfStack(stack_loc, topleft)
            
            pygame.draw.circle(surface, (100, 50, 50), pos, 40)

            stack = self.getItemStack(stack_loc)
            if stack:
                stack.drawAsStack(surface, pos)

    def drawActiveStack(self, surface, pos):
        if self.getActiveStack() != None:
            self.getActiveStack().drawAsStack(surface, pos)


class PlayerInventory(Inventory):
    def __init__(self):
        super().__init__(GAME.PLAYER_INVENTORY_SIZE, GAME.PLAYER_INVENTORY_WIDTH, (100, 100))

        self.selected_slot = 0

        sstack = self.getSelectedStack()
        if sstack: sstack.select()

    def setPlayer(self, player):
        self.player = player

    def getSelectedStack(self):
        return self.getItemStack(self.selected_slot)

    def changeSelectedStack(self, ds):
        sstack = self.getSelectedStack()
        if sstack: sstack.deSelect()
        
        self.selected_slot += ds
        self.selected_slot %= self.size

        sstack = self.getSelectedStack()
        if sstack: sstack.select()

    def throwSelectedStack(self, world, pos):
        self.throwStackInLoc(world, pos, self.selected_slot, 3)

    def onMouseDown(self, pos, button, inv_pos):
        ipos = [pos[0], pos[1]]
        ipos[0] -= inv_pos[0]
        ipos[1] -= inv_pos[1]

        if super().onMouseDown(ipos, button):
            return True

        sstack = self.getSelectedStack()
        if sstack:
            bpos = self.player.manager.screenPosToBufferPos(pos)
            tpos = self.player.world.bufferPosToTilePos(bpos)

            click_used = False
            if button == pygame.BUTTON_LEFT:
                click_used = sstack.onLeft(self.player, self.player.world, tpos, self.player.world.getTile(tpos))
                
            elif button == pygame.BUTTON_RIGHT:
                click_used = sstack.onRight(self.player, self.player.world, tpos, self.player.world.getTile(tpos))

            elif button == pygame.BUTTON_MIDDLE:
                click_used = sstack.onMiddle(self.player, self.player.world, tpos, self.player.world.getTile(tpos))


            if click_used:
                return True
        return False

    def draw(self, surface, topleft):
        for stack_loc in range(self.size):
            pos = self.getPosOfStack(stack_loc, topleft)

            color = ((100, 50, 50) if stack_loc != self.selected_slot else (150, 250, 80))
            
            pygame.draw.circle(surface, color, pos, 40)

            stack = self.getItemStack(stack_loc)
            if stack:
                stack.drawAsStack(surface, pos)
