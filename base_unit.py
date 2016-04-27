import pygame, sys, bmpfont
from pygame.sprite import Sprite

SIZE = 20

class Base_Unit(Sprite):
    """
Base unit for our towers and wave
    """
    
    active_units = pygame.sprite.LayeredUpdates()
    
    # load image for unit text
    unit_font = bmpfont.BitmapFont("images/unitfont.png", 6, 7, 48)
    
    def __init__(self,
                 tile_x = None,
                 tile_y = None,
                 angle = 0,
                 activate = False,
                 **keywords):

        Sprite.__init__(self)
        
        #Default unit stats
        self._angle = angle
        self._active = False
        self.tile_x = tile_x
        self.tile_y = tile_y
        self._angle = angle
        
        #set required pygame things.
        self.image = None
        self.rect = pygame.Rect(0, 0, SIZE, SIZE)
        self._update_image()
        
        if activate:
            self.activate()
                
    def _update_image(self):
        """
        Re-renders the unit's image.
        """
        # rect
        subrect = pygame.Rect(0,
                              0,
                              self.rect.w,
                              self.rect.h)
        # surface
        subsurf = self._base_image.subsurface(subrect)
        # Rotate the sprite
        self.image = pygame.transform.rotate(subsurf, self._angle)

        # Render the unit text.
        if self.type == 'minion': # render health
            text_surf = Base_Unit.unit_font.render(str(int(self.health)))
        if self.type == 'tower':
            text_surf = Base_Unit.unit_font.render(str(int(self.damage)))
        # Move the text to the bottom-right of the image.
        image_rect = self.image.get_rect()
        text_rect = text_surf.get_rect()
        text_rect.move_ip(image_rect.w - text_rect.w,
                            image_rect.h - text_rect.h)
        # Draw the health on to the image.
        self.image.blit(text_surf, text_rect)
        
    def activate(self):
        """
        Adds this unit to the active roster.
        """
        if not self._active:
            self._active = True
            Base_Unit.active_units.add(self)
    
    def deactivate(self):
        """
        Removes this unit from the active roster.
        """
        if self._active:
            self._active = False
            Base_Unit.active_units.remove(self)
