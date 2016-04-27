import sys, pygame, random
from pygame.locals import *

# screen dim
screen_width = 800
screen_height = 600

# colors
black = (0,0,0)
white = (255,255,255)

class START():
	'''
	class for our start menu
	'''
	def __init__(self): # initialization
		self.dispsurf = pygame.display.set_mode((screen_width,screen_height)) # initialize screen

	def update(self):
		'''
		updates screen 
		'''
		pygame.display.update() # update screen 

	def text_objects(self, text, font):
		'''
		renders text
		'''
		textSurface = font.render(text, True, black)
		return textSurface, textSurface.get_rect()

	def message_display(self, text):
		'''
		writes to display 
		'''
		largeText = pygame.font.Font('Arial.ttf', 115)
		TextSurf, TextRect = text_objects(text, largeText)
		TextRect.center = ((screen_width/2),(screen_height/2))
		dispsurf.blit(TextSurf, TextRect)
		pygame.display.update()

	def start_text(self):
		'''
		start menu 
		'''
		self.dispsurf.fill(white)
		largeText = pygame.font.Font('freesansbold.ttf', 115)
		TextSurf, TextRect = self.text_objects("Welcome to Python Tower Defense!", largeText)
		TextRect.center = ((display_width/2), (display_height/2))
		self.dispsurf.blit(TextSurf, TextRect)
