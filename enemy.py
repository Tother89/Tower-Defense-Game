import pygame, sys
from base_unit import Base_Unit

class Enemy(Base_Unit):
    """
    Basic attacking unit
    Moves on the path toward the nexus on its own
    When it reaches the nexus will causing damage
    Will do 1 dmg to health if reaches the nexus
    Speed: Normal
    """
    sprite = pygame.image.load("images/enemy_yellow.png")

    def __init__(self,add_health,**keywords):
        #load the image for the base class.
        self._base_image = Enemy.sprite
        # unit stats
        self.type = 'minion'
        self.health = 8 + add_health
        self.speed = 5
        self.attack = 1
        # Load the base class
        super().__init__(**keywords)