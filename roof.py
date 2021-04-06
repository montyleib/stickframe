import FreeCAD,FreeCADGui,Part, Draft
import os, math
import rafter, ridgebeam, roofpanel, framing

__title__="FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"

__command_name__ = "Roof"
__command_group__ = "Constructions"

#ceiling_levels = ['None','Basement','1st Floor','Second Floor', 'Third Floor', 'Attic' ]

class Roof_Command:
	""" The Roof object creates a container for all the items that make up
	a framed roof.
	"""

	def GetResources(self):
		icon_path = framing.getIconImage( "roof" ) 	

#		image_path = "/" + framing.mod_name + '/icons/roof.png'
		# image_path = '/stickframe/icons/roof.png'
		# global_path = FreeCAD.getHomePath()+"Mod"
		# user_path = FreeCAD.getUserAppDataDir()+"Mod"
		# icon_path = ""

		# if os.path.exists(user_path + image_path):
		# 	icon_path = user_path + image_path
		# elif os.path.exists(global_path + image_path):
		# 	icon_path = global_path + image_path
		return {"MenuText": "Roof",
			"ToolTip": "Add a Roof Group to the Construction",
			'Pixmap' : str(icon_path) }

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):

		partobj = FreeCAD.ActiveDocument.addObject('App::Part','Roof')

		partobj.addProperty("App::PropertyLength", "Length", "Assembly Dimension","Change the overall length of the Roof").Length = "3352.800"
		partobj.addProperty("App::PropertyLength", "Width", "Assembly Dimension","Change the overall width of the Roof").Width = "2743.2"
		partobj.addExtension('Part::AttachExtensionPython' )

		partobj.Placement = FreeCAD.Placement( FreeCAD.Vector ( 0 ,0, 2006)  ,FreeCAD.Rotation ( 0, 0, 0, 0) )


		FreeCAD.ActiveDocument.recompute()

		names = []
		lengths = []
		placements = []
		rotations = []
		expressionslist = []
		expressions = []

		if framing.isItemSelected():
			selection = FreeCADGui.Selection.getSelectionEx()
			obj = selection[0].SubElementNames
			edge_name = obj[0]

			#One Edge
			edge_obj = FreeCADGui.Selection.getSelection()[0]
			edge_shp = FreeCADGui.Selection.getSelection()[0].Shape
			

			edge_elt = FreeCADGui.Selection.getSelection ()[0].Shape.Edge1

			if 	isinstance( edge_shp, Part.Wire ):	
				partobj.Length = edge_elt.Length
				FreeCAD.ActiveDocument.getObject(partobj.Name).Support = [(edge_obj,'Vertex1'),(edge_obj,edge_name)]
				FreeCAD.ActiveDocument.getObject(partobj.Name).MapMode = 'OXY'


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

#		end_gap = length -  ( span_gaps * span_gap ) - start_gap - ( ttl_boards * board_width )
		end_gap = length - ( span_gap.getValueAs( 'mm' ) * span_gaps ) - start_gap.getValueAs( 'mm' ) - ( board_width.getValueAs( 'mm') * ttl_boards)


		for i in range(0, ttl_boards):
			if i == 0 :
				#first_joist, no span added
				names.append ( rafter.makeRafter('RoofRafter').Name )
				lengths.append ( partobj.Width - board_width * 2)
				placements.append( FreeCAD.Vector ( 0,-( 1218.2 - 88.90), 0)  )	
#				rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )
			if i == 1:
				#second, add first span.
				names.append ( rafter.makeRafter('RoofRafter').Name )
				lengths.append ( partobj.Width - board_width *2 )
				placements.append( FreeCAD.Vector ( start_gap,-1129.3, 0)  )
#				rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )

			if ( i > 1 and i < ttl_boards -1):
				#middle_bays
				names.append ( rafter.makeRafter('RoofRafter').Name )
				lengths.append ( partobj.Width - board_width *2 )
				placements.append( FreeCAD.Vector ( (board_centers * (i - 1) + start_gap + board_width ) , -1129.3, 0)  )
#				rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )

			if i == ttl_boards -1:
				#last_joist
				names.append ( rafter.makeRafter('RoofRafter').Name )
				lengths.append ( partobj.Width - board_width *2 )	
				placements.append( FreeCAD.Vector ( (board_centers.getValueAs('mm') * (i -1) + end_gap + board_width.getValueAs('mm')/2),  -1129.3,0 ) )
#				rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )


#		names.append ( rafter.makeRafter('RoofRafter').Name )
#		names.append ( rafter.makeRafter('RoofRafter').Name )
#		names.append ( rafter.makeRafter('RoofRafter').Name )
#		names.append ( rafter.makeRafter('RoofRafter').Name )
#		names.append ( rafter.makeRafter('RoofRafter').Name )
#		names.append ( rafter.makeRafter('RoofRafter').Name )
#		names.append ( rafter.makeRafter('RoofRafter').Name )

#		placements.append( FreeCAD.Vector (0,0,0)  )
#		placements.append( FreeCAD.Vector (406.4,0,0)  )
#		placements.append( FreeCAD.Vector (812.8,0,0)  )
#		placements.append( FreeCAD.Vector (1219.2,0,0)  )
#		placements.append( FreeCAD.Vector (1625.6,0,0)  )
#		placements.append( FreeCAD.Vector (2032.0,0,0)  )
#		placements.append( FreeCAD.Vector (2400.3,0,0)  )


# Rotation (0.5015264712616718, -0.4992350141084935, -0.4992350141084935, 0.5000000000000001)

#		rotations.append ( FreeCAD.Rotation (0.5, -0.5, -0.5, 0.5) )
#		rotations.append ( FreeCAD.Rotation (0.5, -0.5, -0.5, 0.5) )
#		rotations.append ( FreeCAD.Rotation (0.5, -0.5, -0.5, 0.5) )
#		rotations.append ( FreeCAD.Rotation (0.5, -0.5, -0.5, 0.5) )
#		rotations.append ( FreeCAD.Rotation (0.5, -0.5, -0.5, 0.5) )
#		rotations.append ( FreeCAD.Rotation (0.5, -0.5, -0.5, 0.5) )
#		rotations.append ( FreeCAD.Rotation (0.5, -0.5, -0.5, 0.5) )

		for name, placement in zip ( names, placements ):
			FreeCAD.ActiveDocument.getObject( name ).Group[0].Placement.Base = placement
			

		for name, rotation in zip ( names, rotations ):
			FreeCAD.ActiveDocument.getObject( name ).Group[0].Placement.Rotation = rotation

		for name, length in zip ( names, lengths ):
			partobj.addObject ( FreeCAD.ActiveDocument.getObject( name ) )
		#	FreeCAD.ActiveDocument.getObject( name ).Group[0].Length = length

		for name, expressions in zip ( names, expressionslist):
#			print ( name )
			for label, expression in expressions:
#				print ("\t{}".format(expression) )

				obj = FreeCAD.ActiveDocument.getObject( name ).Group[0]
				obj.setExpression ( label, expression  )

		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.SendMsgToActiveView("ViewFit")	

class Roof:

	def __init__(self, obj):

#		obj.addProperty("App::PropertyEnumeration","Level","RoofLevel","The level of this flooring group").RoofLevel = roof_levels

		obj.Proxy = self

		#obj.Shape = plate

	def onChanged(self, fp, prop):
		''' Do something here '''

	def execute(self,fp):
		fp.positionBySupport()
		fp.recompute()


class ViewProviderRoof:
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
#		FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

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

FreeCADGui.addCommand('Roof', Roof_Command())
