from os.path import join
import sys

import pygame

import Camera
import EventQueue
import HashMap
import ImageManager
import Vector

class GameState:
	def __init__(self):
		pygame.init()
		pygame.font.init()
		
		self.SCREEN_SIZE = Vector.Twin( 700, 430 )	#Display size
		
		self.HALF_SCREEN_SIZE = self.SCREEN_SIZE / 2	#Half display size
		
		#Some directory locations
		self.DATA_PATH = sys.path[0]
		self.IMAGE_PATH = join(self.DATA_PATH, 'images')
		#self.SOUND_PATH = join(self.DATA_PATH, 'sounds')
		
		#Setup ImageManager
		self.IM = ImageManager.ImageManager(self.IMAGE_PATH)
		
		#Init Event scheduler
		self.EQ = EventQueue.EventQueue( 0 )	#It won't matter what time we set for the first passthrough.
		
		#self.HASH_GRID_SIZE = 256	#HashMap grid size
		#self.HM = HashMap.HashMap2D( self.HASH_GRID_SIZE )	#HashMap for Entities.
		
		self.camera = None	#Camera
		
		self.player = None	#Reference to player1
		self.enemies = []	#Reference to all enemies
		
		self.driver = None	#StateDriver to be populated later.
		
		#Fonts
		self.font_text20 = pygame.font.Font( None, 20 )
		self.font_digital = pygame.font.Font( join(self.DATA_PATH, 'DS-Digital.ttf'), 20 )
		self.font_digital_large = pygame.font.Font( join(self.DATA_PATH, 'DS-Digital.ttf'), 36 )
		
GS = GameState()
