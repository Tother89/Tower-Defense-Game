import sys, pygame, random, base_unit, time
from pygame.sprite import LayeredUpdates
from pygame.locals import *
from collections import namedtuple
from enemy import Enemy
from tower import Tower

# screen dim
screen_w = 800
screen_h = 600
map_h = 500 # map height
info_w = 150 # width of info box
tool_w = 500 # width of toolbar
tool_h = 100 # height of toolbar
button_y = 520 # y value of buttons
SIZE = 20 # size of tiles and units

# colors
black = (0,0,0)
white = (255,255,255)
grey = (127,127,127)
d_green = (0,100,0)
d_red = (100,0,0)
d_blue = (0,0,100)
b_green = (0,200,0)
b_red = (200,0,0)
b_blue = (0,0,200)
yellow = (200,200,0)

# text fonts
pygame.font.init()
smText = pygame.font.Font('freesansbold.ttf', 14) # for smal text
mdText = pygame.font.Font('freesansbold.ttf', 20) # for med text 
lgText = pygame.font.Font('freesansbold.ttf', 115) # for large text

class Modes: # hold game mods
	select, place, wave, sell = range(4)

Button = namedtuple('Button', ['rect', 'text', 'onClick'])

class GUI(LayeredUpdates):
	'''
	class for our GUI
	'''
	def __init__(self): # initialization
		self.dispsurf = pygame.display.set_mode((screen_w, screen_h)) # initialize screen
		# rect for map
		self.map_rect = pygame.Rect(0, 0, screen_w, map_h)
		# map surface
		self.map_bg = pygame.Surface((800,500))
		# rect for left info box
		self.l_info_rect = pygame.Rect(0, map_h, info_w, tool_h)
		# rect for right info box
		self.r_info_rect = pygame.Rect(screen_w-info_w, map_h, info_w, tool_h)
		# rect for toolbar
		self.toolbar_rect = pygame.Rect(info_w, map_h, tool_w, tool_h)
		
		# intial game mode
		self.mode = Modes.select
		# variables
		self.money = 5000 # player money
		self.health = 100 # nexus health
		self.wave = 1 # wave number
		self.tower_type = 0 # current tower type for select mode
		self.tower1_cost = 500 # cost of tower 1
		self.tower2_cost = 1000 # cost of tower 2
		self.tower3_cost = 1500 # cost of tower 3

		# This will store effects which are drawn over everything else
		self._effects = pygame.sprite.Group()

		# map dictionary, path list and asset list
		self.map_dict = {} # dictionary for all map tiles (x,y) as key, tile type as value
		self.path_list = [] # list of tiles on the map [(x,y),...,]
		self.reached_tile = set() # set of reached tiles for find_path function
		self.game_towers = []

		# intialize tiles
		# load image files
		self.t_grass = pygame.image.load("images/grass.png")
		self.t_rock = pygame.image.load("images/rock.png")
		self.t_dirt = pygame.image.load("images/dirt.png")
		self.t_water = pygame.image.load("images/water.png")
		self.t_bush = pygame.image.load("images/bush.png")
		self.t_nexus = pygame.image.load("images/nexus.png")
		self.t_cave = pygame.image.load("images/cave.png")
		# create dictionary for tile images
		self.tile_dict = {
			0 : self.t_grass,
			1 : self.t_rock,
			2 : self.t_dirt,
			3 : self.t_water,
			4 : self.t_bush}

		# initialize our buttons
		self.toolbar_buttons = [
			Button(pygame.Rect((info_w+20),button_y,60,60), 'GO!', self.setup_wave),
			Button(pygame.Rect((info_w+100),button_y,60,60), 'T1', self.place_tower),
			Button(pygame.Rect((info_w+180),button_y,60,60), 'T2', self.place_tower2),
			Button(pygame.Rect((info_w+260),button_y,60,60), 'T3', self.place_tower3),
			Button(pygame.Rect((info_w+340),button_y,60,60), '$$$', self.select_sell),
			Button(pygame.Rect((info_w+420),button_y,60,60), 'Quit', self.quit_game)]

	def update(self):
		'''
		updates active units
		'''
		base_unit.Base_Unit.active_units.update()

	def draw(self):
		'''
		render display
		'''
		# draw the toolbar and info boxes at the bottom
		self.draw_toolbar()
		if self.mode == Modes.wave:
			# blit map background
			self.dispsurf.blit(self.map_bg, (0,0)) 
		# if on placement mode
		if self.mode == Modes.place:
			cur_pos = pygame.mouse.get_pos() # cursor coords
			tile_pos = self.tile_coord(cur_pos) # convert to tile
			# blit map background
			self.dispsurf.blit(self.map_bg, (0,0)) 
			# if hovered tile is grass then display turret
			if tile_pos in self.map_dict and self.map_dict[tile_pos] == 0: 
				if self.tower_type == 1:
					turret_img = pygame.image.load("images/basic_tower.png")
				if self.tower_type == 2:
					turret_img = pygame.image.load("images/med_tower.png")
				if self.tower_type == 3:
					turret_img = pygame.image.load("images/heavy_tower.png")
				self.dispsurf.blit(turret_img, (tile_pos[0]*20, tile_pos[1]*20))
			# if not able to place in position display x ( rocks, water, nexus etc )
			if tile_pos in self.map_dict and self.map_dict[tile_pos] != 0: 
				x_img = pygame.image.load("images/x.png")
				self.dispsurf.blit(x_img, (tile_pos[0]*20, tile_pos[1]*20))
		# if in sell mode
		if self.mode == Modes.sell:
			cur_pos = pygame.mouse.get_pos()
			tile_pos = self.tile_coord(cur_pos)
			self.dispsurf.blit(self.map_bg, (0,0))
			x_img = pygame.image.load("images/x.png")
			self.dispsurf.blit(x_img, (tile_pos[0]*20, tile_pos[1]*20))
		# draw units
		for u in base_unit.Base_Unit.active_units:
			self.update_unit_rect(u)
		base_unit.Base_Unit.active_units.draw(self.dispsurf)

		# updates the screen with new visuals
		pygame.display.flip() 

	def tile_coord(self, cursor):
		''' 
		takes in tuple of cursor coords and returns tuple of tile coords
		'''
		return (cursor[0]//20, cursor[1]//20)

	def on_click(self, event):
		''' 
		respond to when a mouse clicks
		'''
		# if click on map
		if self.map_rect.collidepoint(event.pos):
			# if in placement mode
			if self.mode == Modes.place and self.map_dict[self.tile_coord(event.pos)] == 0:
				self.build_tower(event.pos, Tower)
			# if in sell mode
			if self.mode == Modes.sell:
				self.sell_tower(event.pos, Tower)

		# else if click on toolbar
		elif self.toolbar_rect.collidepoint(event.pos):
			# check which button was clicked
			for button in self.toolbar_buttons:
				if button.rect.collidepoint(event.pos):
					button.onClick()

	def draw_toolbar(self):
		''' 
		draws toolbar and buttons
		toolbar is 800x100 at the bottom of the screen
		infobox is 150x100 at bottom left of screen
		buttons are 60x60
		'''
		# draw left info box
		pygame.draw.rect(self.dispsurf, d_red, self.l_info_rect)
		# draw title text
		title_text = smText.render("Player info", True, white)
		self.dispsurf.blit(title_text, (self.l_info_rect.left+5, self.l_info_rect.top+5))
		# draw right info box
		pygame.draw.rect(self.dispsurf, d_red, self.r_info_rect)
		# draw title text
		title_text = smText.render("Selected info", True, white)
		self.dispsurf.blit(title_text, (self.r_info_rect.left+5, self.l_info_rect.top+5))

		# update money, health and wave text
		money_text = smText.render("Money: "+str(self.money), True, white)
		health_text = smText.render("Health: "+str(self.health), True, white)
		wave_text = smText.render("Wave: "+str(self.wave), True, white)
		# draw money, health and wave text
		self.dispsurf.blit(money_text, (self.l_info_rect.left+5, self.l_info_rect.top+35))	
		self.dispsurf.blit(health_text, (self.l_info_rect.left+5, self.l_info_rect.top+55))
		self.dispsurf.blit(wave_text, (self.l_info_rect.left+5, self.l_info_rect.top+75))

		# draw toolbar background
		pygame.draw.rect(self.dispsurf, grey, self.toolbar_rect)
		# draw toolbar buttons
		for button in self.toolbar_buttons:
			self.draw_button(button)

	def draw_button(self, button):
		'''
		draw buttons and their text to screen
		'''
		# check if highlighted by mouse
		mouse_pos = pygame.mouse.get_pos()
		if button.rect.collidepoint(mouse_pos):
			but_color = b_green # bright green if highlighted
			self.selected_info(button) # print selected info
		else: but_color = d_green # darker green if not highlighted
		# draw the button
		pygame.draw.rect(self.dispsurf, but_color, button.rect)
		# render button text
		button_text = mdText.render(button.text, True, white)
		# get button text rect and center in button
		text_rect = button_text.get_rect()
		text_rect.center = (button.rect.centerx, button.rect.centery)
		# draw text
		self.dispsurf.blit(button_text, text_rect)

	def selected_info(self, sel):
		'''
		print info for selected object to right info rect 
		sel is the selected object
		'''
		# if object is button then compare the text read
		try: 
			if sel.text == 'GO!':
				sel_text1 = smText.render("Send next wave", True, white)
			if sel.text == 'T1':
				sel_text1 = smText.render("Cost: 500", True, white)
				sel_text2 = smText.render("Damage: 5", True, white)
				sel_text3 = smText.render("Can Buy: "+str(self.money >= self.tower1_cost), True, white)
			if sel.text == 'T2':
				sel_text1 = smText.render("Cost: 1000", True, white)
				sel_text2 = smText.render("Damage: 10", True, white)
				sel_text3 = smText.render("Can Buy: "+str(self.money >= self.tower2_cost), True, white)
			if sel.text == 'T3':
				sel_text1 = smText.render("Cost: 1500", True, white)
				sel_text2 = smText.render("Damage: 15", True, white)
				sel_text3 = smText.render("Can Buy: "+str(self.money >= self.tower3_cost), True, white)
			if sel.text == '$$$':
				sel_text1 = smText.render("Sell a turret", True, white)
			if sel.text == 'Quit':
				sel_text1 = smText.render("Quit game", True, white)
		# if does not posses .text then not a button
		except AttributeError:
			pass

		# draw text to screen
		try:
			# line 1		
			self.dispsurf.blit(sel_text1, (self.r_info_rect.left+5, self.r_info_rect.top+35))
			# line 2 if avail
			self.dispsurf.blit(sel_text2, (self.r_info_rect.left+5, self.r_info_rect.top+55))
			# line 3 if avail
			self.dispsurf.blit(sel_text3, (self.r_info_rect.left+5, self.r_info_rect.top+75))
		# ignore referenced before assignment error for if line 2 and 3 arnt created
		except UnboundLocalError:
			pass

	def load_level(self, filename):
		'''
		Loads a map from the given filename.
		'''
		map_file = open(filename, 'r')
		# Create a dictionary that will enable us to
		# access each individual tile from the file
		for row in range(0,25):
			line = map_file.readline() # get row of numbers
			for col in range(0,40):
				tile_type = int(line[col])
				tile_img = self.tile_dict[tile_type] # get image for tile
				tileRect = tile_img.get_rect() # get bounding rect
				tileRect.left = SIZE*col # place on window and resize
				tileRect.top = SIZE*row
				self.map_bg.blit(tile_img, tileRect) # place on map
				self.map_dict[(col,row)] = tile_type # store tile and coord in map_dict
				if tile_type == 1: # if tile is 1
					self.path_list.append((col,row)) # append coords to path list
		# draw the cave
		self.map_bg.blit(self.t_cave,(0,0))
		# draw the nexus
		self.map_bg.blit(self.t_nexus,(740,400)) 
		# blit the background to the display surf
		self.dispsurf.blit(self.map_bg, (0,0))
		# update the display
		pygame.display.flip()

		map_file.close()

	def place_tower(self):
		self.mode = Modes.place # change mode to place
		self.tower_type = 1 # change tower type to 1 for mouse hovering graphic and cost
	def place_tower2(self):
		self.mode = Modes.place # change mode to place
		self.tower_type = 2 # change tower type to 2 for mouse hovering graphic and cost
	def place_tower3(self):
		self.mode = Modes.place # change mode to place
		self.tower_type = 3 # change tower type to 3 for mouse hovering graphic and cost

	def build_tower(self, pos, tower):
		tile_pos = self.tile_coord(pos)
		for tower in self.game_towers: # check if tower already exists 
			if tile_pos[0] == tower.tile_x and tile_pos[1] == tower.tile_y:
				return
		if self.money >= self.tower_type*300:
			new_tower = Tower(tile_x = tile_pos[0], tile_y = tile_pos[1], activate = True, angle = 0, t_type = self.tower_type)
			# Add the tower to the update group and set its display rect
			self.update_unit_rect(new_tower)
			new_tower._update_image()
			self.money = self.money - (500*self.tower_type)
			self.game_towers.append(new_tower) # add to list of towers

	def select_sell(self):
		self.mode = Modes.sell

	def sell_tower(self, pos, tower):
		tile_pos = self.tile_coord(pos)
		for tower in self.game_towers:
			if tile_pos[0] == tower.tile_x and tile_pos[1] == tower.tile_y and Tower.get_status(tower):
				tower.deactivate() # deactivate tower
				self.money += tower.price* # refund money






	def quit_game(self):
		'''
		quit the game
		'''
		pygame.display.quit()
		sys.exit()

	def tile_neighbour(self, coords):
		'''
		Returns the neighbouring tiles' coordiantes
		'''
		x, y = coords
		
		# The possible neighbouring tiles.
		neighbours = [
			(x, y - 1),
			(x + 1, y),
			(x - 1, y),
			(x, y + 1)
		]
		neighbour_list = []
		# Return only those which exist.
		for n in neighbours:
			if n in self.path_list:
				neighbour_list.append(n)
		return neighbour_list

	def tile_exists(self, coords):
		"""
		Returns true if a tile exists, or false if it doesn't
		"""
		return not (
			coords[0] < 0 or
			coords[0] >= 25 or
			coords[1] < 0 or
			coords[1] >= 40)

	def find_path(self, pos):
		''' 
		Finds the path from the cave to the nexus
		This will be the path the enemies will move on

		We first build a list of all the locations
		of the tiles that are walkable (rock tiles)
 
		Next we use that list to determine which direction
		to send our units in
		'''
		# Save the already reached positions in a list
		self.reached_tile.add(pos)
		# Check to see if our current position has any neighbours
		my_tile = self.tile_neighbour(pos)
		# Go to the unreached neighbours
		try:
			for tile in range(len(my_tile)):
				if my_tile[tile] not in self.reached_tile:
					next_tile = my_tile[tile] # We have not reached this tile yet so go to it
			return next_tile
		except UnboundLocalError: # out of tiles, no more unreached neighbours return (0,0)
			self.reached_tile.clear() # clear reached_tile set
			return (0,0) # return tuple of (0,0) meanung reached point with no more tiles

	def setup_wave(self):
		'''
		Setups the wave of enemies about to be released
		'''
		starting_x = 3 # starting x of sprite
		starting_y = 2 # end x of sprite
		unit_angle = 0 # set angle to 0
		self.mode = Modes.wave # switch mode to sending wave, cannot use other functions in this mode
		# Increase wave multiplier by 5 each new wave
		# wave_amount += 5
		# create new unit at beginning of path
		new_unit = Enemy(tile_x = starting_x,tile_y = starting_y,activate = True,angle = unit_angle,add_health = 2*self.wave)
		for i in range(len(self.path_list)): # for path list
			select = self.find_path((new_unit.tile_x, new_unit.tile_y)) # find next tile in path
			new_unit.tile_x = select[0] # x pos of next tile
			new_unit.tile_y = select[1] # y pos of next tile
			if select == (0,0): # if receive (0,0) means sprite reached end
				new_unit.deactivate() # deactivate the sprite
				self.health -= 1 # subtract 1 from health for reaching nexus/end of path
			self.update() # run update group
			self.draw() # run draw function
			time.sleep(0.05) # delay for movement
		self.wave += 1 # increase wave counter
		self.mode = Modes.select # switch mode back to select

	def update_unit_rect(self, unit):
		"""
		Scales a unit's display rectangle to screen coordiantes.
		"""
		x, y = unit.tile_x, unit.tile_y
		screen_x, screen_y = x*SIZE, y*SIZE
		unit.rect.x = screen_x
		unit.rect.y = screen_y
