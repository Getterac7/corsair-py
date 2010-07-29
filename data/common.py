class SubclassShouldImplement(Exception):
	def __init__(self, msg="A method was called which should have been overridden"):
		Exception.__init__(self,msg)
		
def inspect( item ):
	"""Print useful information about item."""
	if hasattr( item, '__name__' ):
		print "NAME:	", item.__name__
	if hasattr( item, '__class__' ):
		print "CLASS:	", item.__class__.__name__
	print "ID:	", id( item )
	print "TYPE:	", type( item )
	print "VALUE:	", repr( item )
	print "CALLABLE:",
	if callable( item ):
		print "Yes"
	else:
		print "No"
	doc = None
	if hasattr( item, '__doc__' ) and item.__doc__:
		doc = getattr( item, '__doc__' )
		doc = doc.strip()	#Remove leading/trailing whitespace.
	print "DOC:	", doc
	
	