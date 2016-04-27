import sys, pygame, random
from gui import GUI
from pygame.locals import *

def main_loop():
	### initialization ###

	# pygame initialization
	pygame.init() # initialize pygame
	pygame.display.set_caption('PythonTD') # window name

	# game fps clock
	game_gui = GUI() # game
	FPS = 60 # fps variable
	fpsClock = pygame.time.Clock() # update clock
	
	# load map
	argv = sys.argv[1:] # load argument
	level = "tdmap" # default
	if len(argv) > 0:
	    level = argv[0]
	game_gui.load_level("maps/" + level + ".lvl") # load map

	# main game loop
	while 1:
		# user input
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # quit
				pygame.display.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pygame.display.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONUP:
				game_gui.on_click(event)
		# render
		game_gui.update() # update assets
		game_gui.draw() # draws
		fpsClock.tick(FPS) # fps (default 60)

main_loop()
