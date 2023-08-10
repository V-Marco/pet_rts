import pygame
import pygame.locals as locals
import sys
from map import Map
import colors

fps = 60

class LMBSelection:

    def __init__(self):
        self.rect = None
        self.surface = None

    def update(self, mouse_start, mouse_end):

        width = abs(mouse_end[0] - mouse_start[0])
        height = abs(mouse_end[1] - mouse_start[1])
        
        left, top = None, None
        if (mouse_start[0] <= mouse_end[0]) & (mouse_start[1] <= mouse_end[1]):
            left, top = mouse_start[0], mouse_start[1]
        elif (mouse_start[0] <= mouse_end[0]) & (mouse_start[1] > mouse_end[1]):
            left, top = mouse_start[0], mouse_start[1] - height
        elif (mouse_start[0] > mouse_end[0]) & (mouse_start[1] <= mouse_end[1]):
            left, top = mouse_start[0] - width, mouse_start[1]
        elif (mouse_start[0] > mouse_end[0]) & (mouse_start[1] > mouse_end[1]):
            left, top = mouse_start[0] - width, mouse_start[1] - height
        
        self.rect = pygame.Rect(left, top, width, height)
        self.surface = pygame.Surface([width, height])
        self.surface.fill(colors.dark_green)
        self.surface.set_alpha(255 * 0.3)
        pygame.draw.rect(self.surface, colors.green, pygame.Rect(1, 1, width - 2, height - 2))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)
    
    def clear(self):
        self.rect = None
        self.surface = None

class DestinationPointer:

    def __init__(self):
        self.rect = None
        self.surface = None

    def update(self, position):
        radius = 10
        self.surface = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        self.surface.set_alpha(255 * 0.3)
        self.rect = self.surface.get_rect()
        self.rect.left = position[0] - radius
        self.rect.top = position[1] - radius
        pygame.draw.circle(self.surface, colors.yellow_orange, (radius, radius), radius)

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

class Unit(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 20])
        self.image.fill(colors.red)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def main():

    fps_timer = pygame.time.Clock()
    global fps

    map = Map()

    mouse_selection_start_pos = None
    lmb_select_box = LMBSelection()
    
    dest_pos = DestinationPointer()

    while True:

        map.refresh()

        for event in pygame.event.get():
            if event.type == locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left button
                if event.button == 1: 
                    mouse_selection_start_pos = event.pos
                # Right button
                if event.button == 3:
                    dest_pos.update(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                if mouse_selection_start_pos:
                    lmb_select_box.update(mouse_selection_start_pos, event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if mouse_selection_start_pos: 
                        mouse_selection_start_pos = None
                        lmb_select_box.clear()

        if lmb_select_box.rect:         
            lmb_select_box.draw(map.surface)
        if dest_pos.rect:
            dest_pos.draw(map.surface)

        pygame.display.update()
        fps_timer.tick(fps)
    

if __name__ == "__main__":
    pygame.init()
    main()