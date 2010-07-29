from os.path import join

from pygame import image, error

class ImageManager:
	def __init__( self, image_path ):
		self.IMAGE_PATH = image_path
		self.image_dic = {}
	
	def getFrame( self, filename, x, y ):
		return self.image_dic[filename][y][x]
		
	def getRow( self, filename, y ):
		return self.image_dic[filename][y]
	
	def loadSprites( self, filename, tileSize ):
		'''Takes an image and splits it into subsurfaces, caches the results.
		Returns a 2d list (y,x) of tiles indexed by their relative positions in the image.
		'''
		#Check if we have already loaded this image before
		if not filename in self.image_dic:
			images = []
			fullname = join( self.IMAGE_PATH, filename )
			
			try:
				master_image = image.load( fullname ).convert_alpha()
				
			except error, message:
				print 'Cannot load image:', fullname
				raise SystemExit, message
			
			master_width, master_height = master_image.get_size()
			tileWidth,tileHeight = tileSize
			tileCountWidth = int( master_width/tileWidth )
			tileCountHeight = int( master_height/tileHeight )
			
			for j in xrange( tileCountHeight ):
				row = []
				for i in xrange( tileCountWidth ):
					row.append( master_image.subsurface( ( i*tileWidth, j*tileHeight, tileWidth, tileHeight ) ) )
				images.append( row )
			
			#Store images in dictionary
			self.image_dic[filename] = images
		
		return self.image_dic[filename]

