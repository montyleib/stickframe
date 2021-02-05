import FreeCAD,FreeCADGui,Part, Draft
import os, math
import ceilingjoist
import framing

__title__="FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"

__command_name__ = "Ceiling"
__command_group__ = "Constructions"

ceiling_levels = ['None','Basement','1st Floor','Second Floor', 'Third Floor', 'Attic' ]

def makeCeiling():
	pass

class Ceiling_Command:
	""" The Ceiling object creates a container for all the items that make up
	a framed ceiling.
	"""

	def GetResources(self):

		image_path = '/framing/icons/ceiling.png'
		global_path = FreeCAD.getHomePath()+"Mod"
		user_path = FreeCAD.getUserAppDataDir()+"Mod"
		icon_path = ""

		if os.path.exists(user_path + image_path):
			icon_path = user_path + image_path
		elif os.path.exists(global_path + image_path):
			icon_path = global_path + image_path
		return {"MenuText": "Ceiling",
			"ToolTip": "Add a Ceiling Group to the Construction",
			'Pixmap' : str(icon_path) }

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):

		partobj = FreeCAD.ActiveDocument.addObject('App::Part','ceiling')

		partobj.addProperty("App::PropertyLength", "Length", "Assembly Dimension","Change the overall length of the Floor").Length = "3352.800"
		partobj.addProperty("App::PropertyLength", "Width", "Assembly Dimension","Change the overall width of the Floor").Width = "2743.2"
#		partobj.addExtension('Part::AttachExtensionPython', partobj)

		FreeCAD.ActiveDocument.recompute()

		names = []
		lengths = []
		placements = []
		rotations = []
		expressionslist = []
		expressions = []

		if framing.isItemSelected():
			selection = FreeCADGui.Selection.getSelection()

			#One Edge
			edge = FreeCADGui.Selection.getSelection()[0].Shape
			if 	isinstance( edge, Part.Wire ):	
				partobj.Length = edge.Length



		#calculate # of boards and positions
		length = partobj.Length.getValueAs( 'mm' )
		board_centers = FreeCAD.Units.parseQuantity('406.4 mm')
		board_width = FreeCAD.Units.parseQuantity('38.1 mm')

		gaps = math.ceil ( length.Value / board_centers )
		ttl_boards = gaps + 1
		span_gaps = gaps - 2

		gaps_length = length.Value/board_centers
		
		span_gap = board_centers - board_width
		start_gap = board_centers - board_width - ( board_width/2 )

		end_gap = length - ( span_gap.getValueAs( 'mm' ) * span_gaps ) - start_gap.getValueAs( 'mm' ) - ( board_width.getValueAs( 'mm') * ttl_boards)


		#the only thing changin is the X of the placement
		for i in range(0, ttl_boards):
			if i == 0 :
				#first_joist, no span added
				names.append ( ceilingjoist.makeJoist( "CeilingJoist" ).Name )
				lengths.append ( partobj.Width - board_width * 2)
				#lengths.append ( '2438.4 mm' )
				#placements.append( FreeCAD.Vector (38.1,   88.9, 2468.57)  )

			if i == 1:
				#second, add first span.
				names.append ( ceilingjoist.makeJoist('CeilingJoist').Name )
				lengths.append ( partobj.Width - board_width *2 )
				#lengths.append ( '2438.4 mm' )
				placements.append( FreeCAD.Vector ( start_gap, 88.90, 2468.57)  )
				#placements.append( FreeCAD.Vector (38.1,   88.9, 2468.57)  )
				#rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )


			if ( i > 1 and i < ttl_boards -1):
				#middle_bays
				names.append ( ceilingjoist.makeJoist('CeilingJoist').Name )
				lengths.append ( partobj.Width - board_width *2 )
				placements.append( FreeCAD.Vector ( (board_centers * (i - 1) + start_gap + board_width ) , 88.90, 2468.57)  )
				#rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )


			if i == ttl_boards -1:
				#last_joist
				names.append ( ceilingjoist.makeJoist('CeilingJoist').Name )
				lengths.append ( partobj.Width - board_width *2 )	
				placements.append( FreeCAD.Vector ( (board_centers.getValueAs('mm') * (i -1) + end_gap + board_width.getValueAs('mm')/2),  88.90, 2468.57)  )
				#placements.append( FreeCAD.Vector (38.1,   88.9, 2468.57)  )	
				#rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )






#		names.append ( ceilingjoist.makeJoist('CeilingJoist').Name )
#		names.append ( ceilingjoist.makeJoist('CeilingJoist').Name )
#		names.append ( ceilingjoist.makeJoist('CeilingJoist').Name )
#		names.append ( ceilingjoist.makeJoist('CeilingJoist').Name )
#		names.append ( ceilingjoist.makeJoist('CeilingJoist').Name )
#		names.append ( ceilingjoist.makeJoist('CeilingJoist').Name )
#		names.append ( ceilingjoist.makeJoist('CeilingJoist').Name )

#		lengths.append ( '2438.4 mm' )
#		lengths.append ( '2438.4 mm' )
#		lengths.append ( '2438.4 mm' )
#		lengths.append ( '2438.4 mm' )
#		lengths.append ( '2438.4 mm' )
#		lengths.append ( '2438.4 mm' )
#		lengths.append ( '2438.4 mm' )

#		placements.append( FreeCAD.Vector (38.1,   88.9, 2468.57)  )
#		placements.append( FreeCAD.Vector (406.4,  88.9, 2468.57)  )
#		placements.append( FreeCAD.Vector (812.8,  88.9, 2468.57)  )
#		placements.append( FreeCAD.Vector (1219.2, 88.9, 2468.57)  )
#		placements.append( FreeCAD.Vector (1625.6, 88.9,2468.57)  )
#		placements.append( FreeCAD.Vector (2032,   88.9, 2468.57)  )
#		placements.append( FreeCAD.Vector (2271.51,88.9,2468.57)  )


		for name, placement in zip ( names, placements ):
#			FreeCAD.ActiveDocument.getObject( name ).Placement.Base = placement
			FreeCAD.ActiveDocument.getObject( name ).Group[0].Placement.Base = placement

		for name, rotation in zip ( names, rotations ):
			FreeCAD.ActiveDocument.getObject( name ).Placement.Rotation = rotation

		for name, length in zip ( names, lengths ):
			partobj.addObject ( FreeCAD.ActiveDocument.getObject( name ) )
			FreeCAD.ActiveDocument.getObject( name ).Length = length

		for name, expressions in zip ( names, expressionslist):
			for label, expression in expressions:

				obj = FreeCAD.ActiveDocument.getObject( name )
				obj.setExpression ( label, expression  )

		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.SendMsgToActiveView("ViewFit")	

class Ceiling:

	def __init__(self, obj):

		obj.addProperty("App::PropertyEnumeration","Level","Level","The level of this ceiling group").CeilingLevel = ceiling_levels

		obj.addProperty("App::PropertyLength","Width","Assembly Dimension","Change the width of the entire ceiling.").Width = "8 ft"
		obj.addProperty("App::PropertyLength","Length","Assembly Dimension","Change the length of the entire ceiling.").Length = "8 ft"

		obj.Proxy = self

	def onChanged(self, fp, prop):
		''' Do something here '''

	def execute(self,fp):
		fp.recompute()

class ViewProviderCeiling:
	def __init__(self, obj):
		''' Set this object to the proxy object of the actual view provider '''
		obj.Proxy = self

	def attach(self, obj):
		''' Setup the scene sub-graph of the view provider, this method is mandatory '''
		return

	def updateData(self, fp, prop):
		''' If a property of the handled feature has changed we have the chance to handle this here '''
		return

	def getDisplayModes(self,obj):
		''' Return a list of display modes. '''
		modes=[]
		return modes

	def getDefaultDisplayMode(self):
		''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
		return "Lines"

	def setDisplayMode(self,mode):
		''' Map the display mode defined in attach with those defined in getDisplayModes.
		Since they have the same names nothing needs to be done. This method is optional.
		'''
		return mode

	def onChanged(self, vp, prop):
		''' Print the name of the property that has changed '''
		FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

	def getIcon(self):
		''' Return the icon in XMP format which will appear in the tree view. This method is optional
		and if not defined a default icon is shown.
		'''
		return """
			/* XPM */
			static char * ceiling_icon_xpm[] = {
			"16 16 4 1",
			" 	c None",
			".	c #000000",
			"+	c #141010",
			"@	c #C39D55",
			"        ...++...",
			"       ..@@@@...",
			"      ..@@@@.@@+",
			"    ..@@@@..@@@+",
			"   ..@@@...@@@@.",
			"  ..@@@..@@@@@..",
			"..@@@...@@@@@.  ",
			".......@@@@@..  ",
			".@@@.@@@@@@..   ",
			".@@@.@@@@@..    ",
			".@@@.@@@@..     ",
			".@@@.@@@..      ",
			".@@@.@@..       ",
			".@@@.@..        ",
			".@@@...         ",
			"......          "};
			"""

	def __getstate__(self):
		''' When saving the document this object gets stored using Python's cPickle module.
		Since we have some un-pickable here -- the Coin stuff -- we must define this method
		to return a tuple of all pickable objects or None.
		'''
		return None

	def __setstate__(self,state):
		''' When restoring the pickled object from document we have the chance to set some
		internals here. Since no data were pickled nothing needs to be done here.
		'''
		return None

FreeCADGui.addCommand('Ceiling', Ceiling_Command())
