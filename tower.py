import pygame, sys
from base_unit import Base_Unit

class Tower(Base_Unit):
    """
    Basic Tower
    Has a damage and cost
    """
    # sprites for diff towers
    sprite1 = pygame.image.load("images/basic_tower.png")
    sprite2 = pygame.image.load("images/med_tower.png")
    sprite3 = pygame.image.load("images/heavy_tower.png")
    
    def __init__(self,t_type,**keywords):
        # load the image and other properties for the base class.
        self.type = 'tower'
        if t_type == 1:
            self._base_image = Tower.sprite1
            self.damage = 3
            self.price = 500
            self.range = 20
        if t_type == 2:
            self._base_image = Tower.sprite2
            self.damage = 5
            self.price = 1000
            self.range = 20
        if t_type == 3:
            self._base_image = Tower.sprite3
            self.damage = 10
            self.price = 1500
            self.range = 20
        # Load the base class
        super().__init__(**keywords)


