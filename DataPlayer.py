import pygame, Global, DataGame
from pygame import *

class Load:

	def __init__(self, MAP):
	
		self.targetMoveDir = "Right"
		self.moveDir = "Right"
		self.bodySegmentList = [[10, 14]]#, [9, 14], [8, 14], [7, 14]]
		self.score = 0
		
		self.updateSnakeMap(MAP)
		
	def updateSnakeMap(self, MAP):
	
		for bodySegment in self.bodySegmentList:
			MAP[bodySegment[0]][bodySegment[1]] = "Snake"
		
	def update(self, MAP, FOOD_LIST):
		
		self.moveDir = self.targetMoveDir
	
		# Target Move Loc Checks #
		targetMoveLoc = [self.bodySegmentList[0][0], self.bodySegmentList[0][1]]
		if self.moveDir == "Right" : targetMoveLoc[0] += 1
		elif self.moveDir == "Down" : targetMoveLoc[1] += 1
		elif self.moveDir == "Left" : targetMoveLoc[0] -= 1
		elif self.moveDir == "Up" : targetMoveLoc[1] -= 1
		
		# Wall Collide Check #
		if targetMoveLoc[0] < 0 or targetMoveLoc[0] >= Global.SCREEN_SIZE[0] \
		or targetMoveLoc[1] < 0 or targetMoveLoc[1] >= Global.SCREEN_SIZE[1]:
			Global.GAME_STATE = "Game Over"
			
		# Snake Collide Check #
		elif MAP[targetMoveLoc[0]][targetMoveLoc[1]] == "Snake":
			Global.GAME_STATE = "Game Over"
			
		if Global.GAME_STATE == "Play":
		
			# Eat Check #
			eatCheck = False
			if MAP[targetMoveLoc[0]][targetMoveLoc[1]] == "Food":
				eatCheck = True
			
			# Add & Remove Segments #
			if len(self.bodySegmentList) > 1 or eatCheck == True:
				newSegment = [self.bodySegmentList[0][0], self.bodySegmentList[0][1]]
				self.bodySegmentList.insert(1, newSegment)
				
				if eatCheck == False:
					targetDelSegment = self.bodySegmentList[-1]
					MAP[targetDelSegment[0]][targetDelSegment[1]] = None
					del self.bodySegmentList[-1]
			
			if len(self.bodySegmentList) == 1 and eatCheck == False:
				MAP[self.bodySegmentList[0][0]][self.bodySegmentList[0][1]] = None
			
			if eatCheck == True:
				del FOOD_LIST[0]
				DataGame.loadFoodPiece(MAP, FOOD_LIST, self, "Random")
				self.score += 10
			
			# Move Head Segment #
			self.bodySegmentList[0] = targetMoveLoc
			MAP[targetMoveLoc[0]][targetMoveLoc[1]] = "Snake"