import pygame
from misc import events
from constants import ASSETS, GAME
import os

SETTING_FONT = pygame.font.Font(os.path.join(ASSETS.FONT_PATH, ASSETS.NOTABLE_FONT), 60)
TITLE_FONT = pygame.font.Font(os.path.join(ASSETS.FONT_PATH, ASSETS.NOTABLE_FONT), 70)

PADDING = 150

class SettingsMenuOption(events.ButtonShell):
    def __init__(self, name, center, action, button=pygame.BUTTON_LEFT):
        super().__init__(action, button)

        self.name = name

        self.old_rect = pygame.Rect(0, 0, 1500, 100)
        self.old_rect.center = center
        
        self.rect = self.old_rect.copy()
        # self.font = pygame.font.SysFont("Calibri", 60)
        self.font = pygame.font.Font(os.path.join(ASSETS.FONT_PATH, ASSETS.NOTABLE_FONT), 60)

    def draw(self, screen):
        option_text = self.font.render(self.name, False, (255,255,255))
        if self.hovered:
            option_text = self.font.render(self.name, False, (220,220,220))
        if self.pressed:
            option_text = self.font.render(self.name, False, (100,100,100))
        screen.blit(option_text, (self.rect.left, self.rect.centery-option_text.get_rect().centery))

    def scroll_update(self, scroll_amount):
        self.rect.top = self.old_rect.top + scroll_amount


def changeControl (control, key):
    GAME.CONTROLS_KEYS[control] = pygame.key.key_code(key)


class KeyBindOption(SettingsMenuOption):
    def __init__(self, name, center, action, key):
        super().__init__(name, center, action)
        self.key = key
        self.changing = False
        self.change_this_key = lambda name,key: changeControl(name,key)
    
    def onMouseDown(self, pos, button):
        if self.button == button:
            if self.rect.collidepoint(pos):
                self.changing=True

    def onKeyUp(self, key, mod, unicode):
        if self.changing:
            self.key = (pygame.key.name(key))
            self.changing = False
            self.change_this_key(self.name.lower(), self.key)

    def draw(self, screen, top_boundary_bottom):
        option_text = self.font.render(self.name, False, (255,255,255))
        key_text = self.font.render(self.key, False, (255,255,255))

        screen.set_clip(pygame.rect.Rect(0,top_boundary_bottom,screen.get_width(), screen.get_height()-PADDING))

        screen.blit(option_text, (self.rect.left, self.rect.centery-option_text.get_height()/2))
        screen.blit(key_text, (self.rect.right-self.font.size(self.key)[0], self.rect.centery-option_text.get_height()/2))

        pygame.draw.line(screen, (255,255,255), (self.rect.bottomleft), (self.rect.bottomright), 2)
        screen.set_clip(None)


class ScrollBar (pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.pos = [x, y]
        self.height = height
        self.width = width

        self.distance = None

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 255, 255))
        
        self.rect = self.image.get_rect ()
        self.rect.topright = self.pos

        self.isScrolling = False
        self.offset = 0
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def scrollDown (self, pos):
        if self.rect.collidepoint(pos):
            self.isScrolling = True
            self.offset = pos[1]-self.rect.top

    def scrollUp(self, pos):
        self.isScrolling = False

    def getPercentage (self, screen_size):
        return ((self.rect.bottom)-(self.pos[1]+self.rect.height))/((screen_size[1] - PADDING)-(self.pos[1]+self.rect.height))

    def update (self, screen_size):
        if self.isScrolling:
            self.rect.top = pygame.mouse.get_pos()[1]-self.offset
        if self.rect.top < self.pos[1]:
            self.rect.top = self.pos[1]
        if self.rect.bottom > screen_size[1] - PADDING:
            self.rect.bottom = screen_size[1] - PADDING


def changeConstantValue(name, value):
    GAME.SOUND_VOLUMES[name] = value 


class Slider:
    def __init__(self, pos):
        self.rect_pos = pos
        self.width = 500
        self.height = 50
        self.radius = self.height/2
        self.rect = pygame.Rect(self.rect_pos[0]-self.width, self.rect_pos[1]-self.height/2, self.width, self.height)

        self.pos = [self.rect_pos[0]-self.width/2,self.rect_pos[1]]

        self.scrolling = False
    
    def update(self, container):
        if self.scrolling:
            self.pos[0] = pygame.mouse.get_pos()[0]
                
        if self.pos[0] - self.radius < self.rect.left:
            self.pos[0] = self.rect.left + self.radius
        if self.pos[0] + self.radius > self.rect.right:      
            self.pos[0] = self.rect.right - self.radius

        self.rect.top = container.rect.centery-self.height/2
        self.pos[1] = container.rect.centery

    def onMouseDown(self, pos, button):
        if self.rect.collidepoint(pos):
            self.scrolling=True
    
    def onMouseUp(self,pos, button):
        self.scrolling = False


    def getPercentage(self):
        return ((self.pos[0]-self.rect.left-self.radius)/(self.rect.right-self.rect.left-self.radius*2))  

    def draw(self, screen, top_boundary_bottom):
        screen.set_clip(pygame.rect.Rect(0,top_boundary_bottom,screen.get_width(), screen.get_height()-PADDING))
        pygame.draw.rect(screen, "white", self.rect, 3, int(self.radius))
        pygame.draw.circle(screen, "white", self.pos, self.radius)
        screen.set_clip(None)


class ScrollingOption (SettingsMenuOption):
    def __init__(self, name, center, action):
        super().__init__(name, center, action)
        self.changing = False
        self.slider = Slider((self.rect.right, self.rect.centery))
        self.slider.pos[1] += 10
        self.slider.rect.bottom += 10

        self.changeConstantValue = lambda name,value: changeConstantValue(name,value)

    def onMouseDown(self, pos, button):
        self.slider.onMouseDown(pos, button)

    def onMouseUp(self, pos, button):
        self.slider.onMouseUp(pos, button)
        self.changeConstantValue(self.name, self.slider.getPercentage()*100)

    def draw (self, screen, enter_any_key, top_boundary_bottom):
        option_text = self.font.render(self.name, True, (255,255,255))
        screen.set_clip(pygame.rect.Rect(0,top_boundary_bottom, screen.get_width(), screen.get_height()-PADDING))
        screen.blit(option_text, (self.rect.left, self.rect.centery-option_text.get_height()/2))
        if not enter_any_key:
            self.slider.update(self)
        self.slider.draw(screen, top_boundary_bottom)
        if self.rect.bottom < screen.get_height()-PADDING:
            pygame.draw.line(screen, (255,255,255), (self.rect.bottomleft), (self.rect.bottomright), 2)
        screen.set_clip(None)    

class SettingsMenu(events.Alpha):
    def __init__(self, screen_size):
        # bg = pygame.image.load(os.path.join(ASSETS.MENU_PATH, ASSETS.SETTINGS_MENU_BG)).convert()
        # self.bg = pygame.transform.scale(bg, screen_size)
        
        padding_y = 200
        gap_y=175

        self.exit = SettingsMenuOption("Exit", (0,0), lambda: pygame.event.post(pygame.event.Event(events.RETURN_TO_MAIN_MENU)))
        self.exit.rect.width = SETTING_FONT.size("Exit")[0]
        self.exit.rect.topright = (screen_size[0]-100, 100)

        self.changing_keybind_screen_darken = pygame.Surface((screen_size[0], screen_size[1]))
        self.changing_keybind_screen_darken.fill((0, 0, 0))
        self.changing_keybind_screen_darken.set_alpha(160)

        self.keybind_options_names = GAME.CONTROLS_KEYS.keys()
        self.keybind_options = {}

        for i, name in enumerate(self.keybind_options_names):
            self.keybind_options[name] = KeyBindOption(name, (screen_size[0]/2,padding_y+(i+1)*gap_y), lambda: None, pygame.key.name(GAME.CONTROLS_KEYS[name]))
            gap_from_previous = i+2

        self.scrolling_option_names = list(GAME.SOUND_VOLUMES.keys())
        #------ If you want to test scrolling, add these lines back in
        # self.scrolling_option_names.append("heiasd")
        # self.scrolling_option_names.append("askad")
        # self.scrolling_option_names.append("ffffd")
        self.scrolling_options = {}

        for i, name in enumerate(self.scrolling_option_names):
            self.scrolling_options[name] = ScrollingOption(name, (screen_size[0]/2, padding_y+(gap_from_previous+i)*gap_y), lambda: None)

        self.all_options = self.keybind_options | self.scrolling_options

        scroll_bar_dimensions = (40,190)
        self.scroll_bar = ScrollBar(self.exit.rect.right, self.keybind_options[list(self.keybind_options_names)[0]].rect.top, scroll_bar_dimensions[0], scroll_bar_dimensions[1])

        self.screen_size = screen_size


    def onMouseDown(self, pos, button):
        for keybind_option in self.keybind_options.values():
            if keybind_option.changing:
                return
            
        self.exit.onMouseDown(pos,button)
        for keybind_option in self.all_options.values():
            keybind_option.onMouseDown(pos,button)
        self.scroll_bar.scrollDown(pos)

    def onMouseUp(self, pos, button):
        for setting_option in self.keybind_options.values():
            if setting_option.changing:
                return

        self.exit.onMouseUp(pos,button)
        for setting_option in self.all_options.values():
            setting_option.onMouseUp(pos,button)
        self.scroll_bar.scrollUp(pos)

    def onMouseMotion(self, pos):
        for setting_option in self.keybind_options.values():
            if setting_option.changing:
                return

        self.exit.onMouseMotion(pos)
        for setting_option in self.keybind_options.values():
            setting_option.onMouseMotion(pos)

    def onKeyUp(self, key, mod, unicode):
        for setting_option in self.keybind_options.values():
            setting_option.onKeyUp(key,mod,unicode)

    def main_tick(self):
        self.scroll_bar.update(self.screen_size)
        
        lowest_option = self.all_options[list(self.all_options.keys())[-1]]
        highest_option = self.all_options[list(self.all_options.keys())[0]]

        max_scroll = (lowest_option.rect.bottom + 1 -highest_option.rect.top-(self.screen_size[1]-highest_option.old_rect.top-PADDING))
        if max_scroll > 0:
            scroll_distance_perhaps = max_scroll*self.scroll_bar.getPercentage(self.screen_size)
            for setting in self.all_options:
                self.all_options[setting].scroll_update(-scroll_distance_perhaps)


    def draw(self, surface):
        # surface.blit(self.bg, (surface.get_rect().centerx-self.bg.get_rect().centerx, 0))
        
        self.exit.draw(surface)
        surface.blit(TITLE_FONT.render("Settings", True, (255,255,255)), (surface.get_width()/2-TITLE_FONT.size("Settings")[0]/2, PADDING))
        enter_any_key = False
        
        self.scroll_bar.draw(surface)

        top_boundary = PADDING+TITLE_FONT.render("Settings", True, "White").get_height()+50

        for setting_option in self.keybind_options.values():
            setting_option.draw(surface,top_boundary)
            if setting_option.changing:
                enter_any_key = True
        
        for setting_option in self.scrolling_options.values():
            setting_option.draw(surface, enter_any_key,top_boundary)

        if enter_any_key:
            surface.blit(self.changing_keybind_screen_darken,(0,0))
            message_text = "Please Enter Any Key"
            message = SETTING_FONT.render(message_text, True, (255,255,255))
            surface.blit(message, (surface.get_width()/2-SETTING_FONT.size(message_text)[0]/2,surface.get_height()/2-SETTING_FONT.size(message_text)[1]/2))


