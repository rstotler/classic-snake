import pygame, random, Global, DataPlayer
from pygame import *

class Load:

	def __init__(self):
	
		self.screenMain = pygame.display.set_mode([Global.SCREEN_SIZE[0] * Global.CELL_SIZE, Global.SCREEN_SIZE[1] * Global.CELL_SIZE])
		self.fontDict = {16:pygame.font.Font("CodeNewRomanB.otf", 16), 32:pygame.font.Font("CodeNewRomanB.otf", 32)}
		self.clock = pygame.time.Clock()
		self.map = self.loadMap()
		self.dataPlayer = DataPlayer.Load(self.map)
		self.foodList = []
		
		loadFoodPiece(self.map, self.foodList, self.dataPlayer, [20, 14])
	
	def loadMap(self):
	
		map = []
		
		for xNum in range(Global.SCREEN_SIZE[0]):
			map.append([])
			for yNum in range(Global.SCREEN_SIZE[1]):
				map[-1].append(None)
		
		return map
				
	def update(self):
	
		self.clock.tick(Global.FPS)
		self.processInput()
		if Global.GAME_STATE == "Play" : self.dataPlayer.update(self.map, self.foodList)
		
		self.drawScreen()
		
	def processInput(self):
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
				raise SystemExit
			elif event.type == pygame.KEYDOWN and event.key in [K_UP, K_RIGHT, K_DOWN, K_LEFT]:
				
				# Reset Game #
				if Global.GAME_STATE == "Game Over":
					self.dataPlayer.targetMoveDir = "Right"
					self.dataPlayer.moveDir = "Right"
					self.dataPlayer.bodySegmentList = [[10, 14]]
					self.dataPlayer.score = 0
					self.map = self.loadMap()
					self.dataPlayer.updateSnakeMap(self.map)
					self.foodList = []
					loadFoodPiece(self.map, self.foodList, self.dataPlayer, [20, 14])
					Global.GAME_STATE = "Play"
		
				if event.key == K_UP and (not self.dataPlayer.moveDir == "Down" or Global.GAME_STATE in ["New Game", "Start Over"]):
					self.dataPlayer.targetMoveDir = "Up"
				elif event.key == K_RIGHT and (not self.dataPlayer.moveDir == "Left" or Global.GAME_STATE in ["New Game", "Start Over"]):
					self.dataPlayer.targetMoveDir = "Right"
				elif event.key == K_DOWN and (not self.dataPlayer.moveDir == "Up" or Global.GAME_STATE in ["New Game", "Start Over"]):
					self.dataPlayer.targetMoveDir = "Down"
				elif event.key == K_LEFT and (not self.dataPlayer.moveDir == "Right" or Global.GAME_STATE in ["New Game", "Start Over"]):
					self.dataPlayer.targetMoveDir = "Left"
				
				if Global.GAME_STATE == "New Game" : Global.GAME_STATE = "Play"
	
	def drawScreen(self):
	
		self.screenMain.fill([0, 0, 0])
	
		for bodySegment in self.dataPlayer.bodySegmentList:
			pygame.draw.rect(self.screenMain, [0, 50, 0], [bodySegment[0] * Global.CELL_SIZE, bodySegment[1] * Global.CELL_SIZE, Global.CELL_SIZE, Global.CELL_SIZE])
		for foodPiece in self.foodList:
			pygame.draw.rect(self.screenMain, [50, 0, 0], [foodPiece[0] * Global.CELL_SIZE, foodPiece[1] * Global.CELL_SIZE, Global.CELL_SIZE, Global.CELL_SIZE])
	
		# Score Strings #
		stringScore = "Score: " + str(self.dataPlayer.score)
		drawString(stringScore, ["Left", "Top"], [200, 200, 200], self.fontDict[32], self.screenMain)
	
		# Screen State Strings #
		if Global.GAME_STATE in ["New Game", "Game Over"]:
			drawString("Press Arrow Key To Start", ["Center", "Center"], [200, 200, 200], self.fontDict[32], self.screenMain)
		if Global.GAME_STATE == "Game Over":
			drawString("Game Over", ["Center", 250], [200, 200, 200], self.fontDict[32], self.screenMain)
	
		pygame.display.flip()
		
def drawString(STRING, LOCATION, COLOR, FONT, SCREEN):

	# Location Mods #
	labelSize = FONT.size(STRING)
	if isinstance(LOCATION[0], str) and LOCATION[0].lower() == "left" : LOCATION[0] = 0
	elif isinstance(LOCATION[0], str) and LOCATION[0].lower() == "right" : LOCATION[0] = SCREEN.get_width() - labelSize[0]
	elif isinstance(LOCATION[0], str) and LOCATION[0].lower() == "center" : LOCATION[0] = (SCREEN.get_width() / 2) - (labelSize[0] / 2)
	if isinstance(LOCATION[1], str) and LOCATION[1].lower() == "top" : LOCATION[1] = 0
	elif isinstance(LOCATION[1], str) and LOCATION[1].lower() == "bottom" : LOCATION[1] = SCREEN.get_height() - labelSize[1]
	elif isinstance(LOCATION[1], str) and LOCATION[1].lower() == "center" : LOCATION[1] = (SCREEN.get_height() / 2) - (labelSize[1] / 2)
	
	stringRender = FONT.render(STRING, True, COLOR)
	SCREEN.blit(stringRender, LOCATION)
	
def loadFoodPiece(MAP, FOOD_LIST, PLAYER, LOC):

	targetLoc = LOC
	if LOC == "Random":
		while targetLoc == "Random" or targetLoc in PLAYER.bodySegmentList:
			targetLoc = [random.randrange(Global.SCREEN_SIZE[0]), random.randrange(Global.SCREEN_SIZE[1])]

	if MAP[targetLoc[0]][targetLoc[1]] == None:
		MAP[targetLoc[0]][targetLoc[1]] = "Food"
		FOOD_LIST.append(targetLoc)