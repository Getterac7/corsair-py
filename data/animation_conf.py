
from GameState import GS
import Ring
import Vector


''' ANIMATION SYSTEM v4 '''
masterAnimationDict = {}




''' Player '''
dict = masterAnimationDict['Player'] = {}
dict['fileName'] = 'Corsair.png'				#File name of the image to load for these sprites.
dict['tileSize'] = Vector.Twin(35, 33)		#Size in pixels of each tile in the image.
actions = dict['actions'] = {}				#Jump into the actions dictionary.

#off
act = actions['off'] = {}					#Dictionary name for the action.
act['spriteRow'] = 0						#Zero indexed row number to find the images.  The first image will be on the left edge.
act['frameCount'] = 1						#Number of frames in the animation.
act['offset'] = Vector.Twin(0, 0)			#Offset of a child's center point from the parent's center point.  Only child objects will use this field.
act['collision'] = 16.5						#The bounding collision circle for this animation relative to the object.  Value is the radius of the circle.  Circle will be positioned in the center of the image.
act['delay'] = 0							#The delay in milliseconds between each animation frame.  Set to zero to disable animation.
#act['images'] = Ring()						#This gets generated later automatically.

#on
act = actions['on'] = {}
act['spriteRow'] = 1
act['frameCount'] = 1
act['offset'] = Vector.Twin(0, 0)
act['collision'] = 16.5
act['delay'] = 0

#hit
act = actions['hit'] = {}
act['spriteRow'] = 2
act['frameCount'] = 1
act['offset'] = Vector.Twin(0, 0)
act['collision'] = 16.5
act['delay'] = 0







''' PlayerLaser '''
dict = masterAnimationDict['PlayerLaser'] = {}
dict['fileName'] = 'Lasers.png'
dict['tileSize'] = Vector.Twin(14, 14)
actions = dict['actions'] = {}

#moving
act = actions['moving'] = {}
act['spriteRow'] = 1
act['frameCount'] = 1
act['offset'] = Vector.Twin(0, 0)
act['collision'] = 7
act['delay'] = 0

#death
act = actions['death'] = {}
act['spriteRow'] = 1
act['frameCount'] = 10
act['offset'] = Vector.Twin(0, 0)
act['collision'] = 7
act['delay'] = 20





''' Explosion '''
dict = masterAnimationDict['Explosion'] = {}
dict['fileName'] = 'Explosion.png'
dict['tileSize'] = Vector.Twin(39, 35)
actions = dict['actions'] = {}

#death
act = actions['death'] = {}
act['spriteRow'] = 0
act['frameCount'] = 11
act['offset'] = Vector.Twin(0, 0)
act['collision'] = 0
act['delay'] = 20





''' Enemy '''
dict = masterAnimationDict['Enemy'] = {}
dict['fileName'] = 'Enemies.png'
dict['tileSize'] = Vector.Twin(31, 33)
actions = dict['actions'] = {}

#off
act = actions['off'] = {}
act['spriteRow'] = 0
act['frameCount'] = 10
act['offset'] = Vector.Twin(0, 0)
act['collision'] = 16.5
act['delay'] = 0

#on
act = actions['on'] = {}
act['spriteRow'] = 1
act['frameCount'] = 10
act['offset'] = Vector.Twin(0, 0)
act['collision'] = 16.5
act['delay'] = 0






''' EnemyLaser '''
dict = masterAnimationDict['EnemyLaser'] = {}
dict['fileName'] = 'Lasers.png'
dict['tileSize'] = Vector.Twin(14, 14)
actions = dict['actions'] = {}

#moving
act = actions['moving'] = {}
act['spriteRow'] = 0
act['frameCount'] = 1
act['offset'] = Vector.Twin(0, 0)
act['collision'] = 7
act['delay'] = 0

#death
act = actions['death'] = {}
act['spriteRow'] = 0
act['frameCount'] = 10
act['offset'] = Vector.Twin(0, 0)
act['collision'] = 7
act['delay'] = 20






''' Enemy Death Sequence '''
dict = masterAnimationDict['EnemyDeath'] = {}
dict['fileName'] = 'EnemyDeath.png'
dict['tileSize'] = Vector.Twin(74, 74)
actions = dict['actions'] = {}

#death
act = actions['death'] = {}
act['spriteRow'] = 0
act['frameCount'] = 17
act['offset'] = Vector.Twin(0, 0)
act['collision'] = 0
act['delay'] = 50





''' HUD '''
dict = masterAnimationDict['HUD'] = {}
dict['fileName'] = 'HUD.png'
dict['tileSize'] = Vector.Twin( 210, 146 )
actions = dict['actions'] = {}

#on
act = actions['on'] = {}
act['spriteRow'] = 0
act['frameCount'] = 1
act['offset'] = Vector.Twin(0, 0)
act['collision'] = 0
act['delay'] = 0





''' Shield '''
dict = masterAnimationDict['Shield'] = {}
dict['fileName'] = 'Shield.png'
dict['tileSize'] = Vector.Twin( 107, 107 )
actions = dict['actions'] = {}

#on
act = actions['on'] = {}
act['spriteRow'] = 0
act['frameCount'] = 6
act['offset'] = Vector.Twin(0, 0)
act['collision'] = 0
act['delay'] = 0
















def init():
	#Generate image Rings, Rects, and tuples for all directions.
	for actorName,actorDict in masterAnimationDict.iteritems():	#For each Actor definition
		fileName = actorDict[ 'fileName' ]	#Easier referencing.
		tileW,tileH = actorDict[ 'tileSize' ]
		halfTileW = int( tileW / 2 )
		halfTileH = int( tileH / 2 )
		imageDict = GS.IM.loadSprites( fileName, ( tileW, tileH ) )	#Get the split image surfaces.
		baseD = actorDict[ 'actions' ]	#Get the default data here.
		
		for actionName,actionDict in baseD.iteritems():	#Loop through each action in the base dictionary.
			try:
				imglist = imageDict[ actionDict[ 'spriteRow' ] ][ 0:actionDict[ 'frameCount' ] ]	#Get the images for the current action in a list.
			except:
				print "Error occurred initializing animations!"
				print "actorName=%s; actionName=%s" % (actorName, actionName)
				raise SystemExit, -1
			actionDict[ 'images' ] = Ring.Ring( imglist )	#Populate image ring.
			
