import FreeCAD, FreeCADGui, Part, Draft
import os, math
import floorjoist, floorpanel, panel, framing

__title__="FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"

__command_name__ = "Floor"
__command_group__ = "Constructions"

floor_levels = ['None','Basement','1st Floor','Second Floor', 'Third Floor', 'Attic' ]

def makeFloor():
	pass


class Floor_Command:
	""" The Floor object creates a container for all the items that make up
	a framed floor.
	"""

	def GetResources(self):

		image_path = '/framing/icons/floor.png'
		global_path = FreeCAD.getHomePath()+"Mod"
		user_path = FreeCAD.getUserAppDataDir()+"Mod"
		icon_path = ""

		if os.path.exists(user_path + image_path):
			icon_path = user_path + image_path
		elif os.path.exists(global_path + image_path):
			icon_path = global_path + image_path
		return {"MenuText": "Floor",
			"ToolTip": "Add a Floor Group to the Construction",
			'Pixmap' : str(icon_path) }

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		#TODO: Move this to a makeFloor() command

		partobj = FreeCAD.ActiveDocument.addObject('App::Part','Floor')

		partobj.addProperty("App::PropertyLength", "Length", "Assembly Dimension","Change the overall length of the Floor").Length = "8 ft"
		partobj.addProperty("App::PropertyLength", "Width", "Assembly Dimension","Change the overall width of the Floor").Width = "8 ft"
#		partobj.addExtension('Part::AttachExtensionPython', partobj)

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
		length = partobj.Length.getValueAs( 'mm' ) - 38.1
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

#		print ( "Length: \t", length )
#		print ( "Centers: \t", board_centers )
#		print ( "Board Width: \t", board_width )
#		print ( "" )
#		print ( "Gaps Lenght: \t", gaps_length )
#		print ( "Total Boards: \t", ttl_boards )
#		print ( "Center Spans: \t", span_gaps )

#		print ( "Span Gap: \t", span_gap )
#		print ( "Start Gap: \t", start_gap )
#		print ( "End Gap: \t", end_gap)
#		print ( "" )
#		print ( "Length Check: \t", (span_gap * span_gaps ) + start_gap + end_gap + (ttl_boards * board_width ) )

		#TODO: Load from XML or similar

		#Longer Rim Joists
		names.append ( floorjoist.makeFloorJoist( "RimJoist" ).Name )
		names.append ( floorjoist.makeFloorJoist( "RimJoist" ).Name )
#		lengths.append ( '2438.4 mm' )
#		lengths.append ( '2438.4 mm' )
		lengths.append ( partobj.Length )
		lengths.append ( partobj.Length )
		placements.append( FreeCAD.Vector (-38.1, 50.80 , -251.3250)  )
		placements.append( FreeCAD.Vector (-38.1, - partobj.Width.getValueAs('mm') +88.9 , -251.3250)  )
		rotations.append ( FreeCAD.Rotation (0.7071067811865475, 4.329780281177466e-17, 0.7071067811865476, 4.329780281177467e-17) )
		rotations.append ( FreeCAD.Rotation (0.7071067811865475, 4.329780281177466e-17, 0.7071067811865476, 4.329780281177467e-17) )

		#Span joists ( all the same length and orientantion, offset only by centers )
		

		#the only thing changin is the X of the placement
		for i in range(0, ttl_boards):
			if i == 0 :
				#first_joist, no span added
				names.append ( floorjoist.makeFloorJoist( "RimJoist" ).Name )
				lengths.append ( partobj.Width - board_width * 2)
				placements.append( FreeCAD.Vector ( 0, 88.90, -251.3250)  )	
				rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )
			if i == 1:
				#second, add first span.
				names.append ( floorjoist.makeFloorJoist( "FloorJoist" ).Name )
				lengths.append ( partobj.Width - board_width *2 )
				placements.append( FreeCAD.Vector ( start_gap, 88.90, -251.325)  )
				rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )

			if ( i > 1 and i < ttl_boards -1):
				#middle_bays
				names.append ( floorjoist.makeFloorJoist( "FloorJoist" ).Name )
				lengths.append ( partobj.Width - board_width *2 )
				placements.append( FreeCAD.Vector ( (board_centers * (i - 1) + start_gap + board_width ) , 88.90, -251.325)  )
				rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )

			if i == ttl_boards -1:
				#last_joist
				names.append ( floorjoist.makeFloorJoist( "RimJoist" ).Name )
				lengths.append ( partobj.Width - board_width *2 )	
#				print( "Length in mm: ", length )
				placements.append( FreeCAD.Vector ( length,  88.90, -251.3250)  )
				rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )


#		names.append ( floorjoist.makeFloorJoist( "RimJoist" ).Name )
#		names.append ( floorjoist.makeFloorJoist( "RimJoist" ).Name )

#		names.append ( floorjoist.makeFloorJoist( "FloorJoist" ).Name )
#		names.append ( floorjoist.makeFloorJoist( "FloorJoist" ).Name )
#		names.append ( floorjoist.makeFloorJoist( "FloorJoist" ).Name )
#		names.append ( floorjoist.makeFloorJoist( "FloorJoist" ).Name )
#		names.append ( floorjoist.makeFloorJoist( "FloorJoist" ).Name )

#		lengths.append ( '2362.2 mm' )
#		lengths.append ( '2362.2 mm' )	

#		lengths.append ( '2362.2 mm' )
#		lengths.append ( '2362.2 mm' )
#		lengths.append ( '2362.2 mm' )
#		lengths.append ( '2362.2 mm' )
#		lengths.append ( '2362.2 mm' )

#		placements.append( FreeCAD.Vector (-38.0999, 50.8, -251.3250)  )
#		placements.append( FreeCAD.Vector (-38.0999, -2349.4999, -251.3250)  )
#
#		placements.append( FreeCAD.Vector (406.4, 88.90, -251.325)  )
#		placements.append( FreeCAD.Vector (812.8, 88.90, -251.325)  )
#		placements.append( FreeCAD.Vector (1219.2, 88.90, -251.325)  )
#		placements.append( FreeCAD.Vector (1625.6, 88.90, -251.325)  )
#		placements.append( FreeCAD.Vector (2032.0, 88.90, -251.325) )

#		rotations.append ( FreeCAD.Rotation (0.7071067811865475, 4.329780281177466e-17, 0.7071067811865476, 4.329780281177467e-17) )
#		rotations.append ( FreeCAD.Rotation (0.7071067811865475, 4.329780281177466e-17, 0.7071067811865476, 4.329780281177467e-17) )

#		rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )
#		rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )
#		rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )
#		rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )
#		rotations.append ( FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )

		

		#Panels
#		names.append ( floorpanel.makePanel( "FloorPanel" ).Name )
#		names.append ( floorpanel.makePanel( "FloorPanel" ).Name )
#		names.append ( floorpanel.makePanel( "FloorPanel" ).Name )

#		lengths.append ( '2438.4 mm' )
#		lengths.append ( '1219.2 mm' )
#		lengths.append ( '1219.2 mm' )

#		placements.append( FreeCAD.Vector (2.27, 88.90, -60.825)  )
#		placements.append( FreeCAD.Vector (1219.20, 88.90, -60.825)  )
#		placements.append( FreeCAD.Vector (1219.20, -2349.49, -60.825)  )
 
#		rotations.append (FreeCAD. Rotation (0.0, 0.0, 0.7071067811865476, -0.7071067811865475) )
#		rotations.append (FreeCAD. Rotation (0.0, 0.0, -0.7071067811865477, 0.7071067811865474) )
#		rotations.append (FreeCAD. Rotation (0.0, 0.0, 2.220446049250313e-16, -1.0) )

#		dim1 = Draft.makeDimension(FreeCAD.ActiveDocument.RimJoist001,4,0,FreeCAD.Vector(400.0,-2500.0,-88.90))
#		dim2 = Draft.makeDimension(FreeCAD.ActiveDocument.RimJoist002,4,0,FreeCAD.Vector(-200.0,-2700.0,-88.90))

#		dim1.ViewObject.FontSize = '76.2 mm'
#		dim1.ViewObject.FlipText = True

#		dim2.ViewObject.FontSize = '76.2 mm'
#		dim2.ViewObject.FlipText = True


#TODO: this codes is used for all 'containers' it can be moved to framing class

		for name, placement in zip ( names, placements ):
			FreeCAD.ActiveDocument.getObject( name ).Placement.Base = placement

		for name, rotation in zip ( names, rotations ):
			FreeCAD.ActiveDocument.getObject( name ).Placement.Rotation = rotation

		for name, length in zip ( names, lengths ):
			partobj.addObject ( FreeCAD.ActiveDocument.getObject( name ) )
			FreeCAD.ActiveDocument.getObject( name ).Length = length

		for name, expressions in zip ( names, expressionslist):
#			print ( name )
			for label, expression in expressions:
#				print ("\t{}".format(expression) )

				obj = FreeCAD.ActiveDocument.getObject( name )
				obj.setExpression ( label, expression  )

		#Placement [Pos=(-2.72848e-12,-1.40687e-12,44.95), Yaw-Pitch-Roll=(0,0,0)]
		partobj.Placement = FreeCAD.Placement ( FreeCAD.Vector ( -2.72848e-12,-1.40687e-12,44.95 ), FreeCAD.Rotation (0,0,0 ) )

		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.SendMsgToActiveView("ViewFit")	

class Floor:


	def __init__(self, obj):
		#self.Placement = FreeCAD.Placement()

		#TODO : App.DocumentObjectGroup does not seem to have a Proxy so how
		#do I add a ViewProvider SOLUTION use App.DocumentObjectGroupPython

		obj.addProperty("App::PropertyEnumeration","FloorLevel","Framing","The level of this flooring group").FloorLevel = floor_levels
		obj.addProperty("App::PropertyLength","Width","Assembly Dimension","Change the width of the entire floor.").Length = "8 ft"
		obj.addProperty("App::PropertyLength","Length","Assembly Dimension","Change the length of the entire floor.").Length = "8 ft"

		obj.Proxy = self


	def setProperties(self, obj):
		# move property setup here 
		pass

	def onChanged(self, fp, prop):
		''' Do something here '''
		#if prop == "Length" or prop == "Width" or prop == "Height":
		#	fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height)
		pass

	def execute(self,fp):
		fp.recompute()
#		print ("Framing.Floor executed()")

class ViewProviderFloor:
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
			static char * floor_xpm[] = {
			"64 64 4 1",
			" 	c None",
			".	c #010100",
			"+	c #F2F466",
			"@	c #E1B313",
			"                           .++++++++++++++++++++++++++++++++++++",
			"                          .+++++++++++++++++++++++++++++++++++++",
			"                         .++++++++++++++++++++++++++++++++++++++",
			"                        .+++++++++++++++++++++++++++++++++++++++",
			"                       .++++++++++++++++++++++++++++++++++++++++",
			"                      .+++++++++++++++++++++++++++++++++++++++++",
			"                     .++++++++++++++++++++++++++++++++++++++++++",
			"                    .+++++++++++++++++++++++++++++++++++++++++++",
			"                   .++++++++++++++++++++++++++++++++++++++++++++",
			"                  .+++++++++++++++++++++++++++++++++++++++++++++",
			"                 .++++++++++++++++++++++++++++++++++++++++++++++",
			"                .+++++++++++++++++++++++++++++++++++++++++++++++",
			"               .++++++++++++++++++++++++++++++++++++++++++++++++",
			"              .+++++++++++++++++++++++++++++++++++++++++++++++++",
			"             .++++++++++++++++++++++++++++++++++++++++++++++++++",
			"            .+++++++++++++++++++++++++++++++++++++++++++++++++++",
			"           .+++++++++++++++++++++++++++++++++++++++++++++++++++.",
			"          .+++++++++++++++++++++++++++++++++++++++++++++++++++.+",
			"         .+++++++++++++++++++++++++++++++++++++++++++++++++++.++",
			"        .+++++++++++++++++++++++++++++++++++++++++++++++++++.++.",
			"       .+++++++++++++++++++++++++++++++++++++++++++++++++++.++.@",
			"      .+++++++++++++++++++++++++++++++++++++++++++++++++++.++.@@",
			"     .+++++++++++++++++++++++++++++++++++++++++++++++++++.++.@@@",
			"    .+++++++++++++++++++++++++++++++++++++++++++++++++++.++.@@@@",
			"   .+++++++++++++++++++++++++++++++++++++++++++++++++++.++.@@@@@",
			"  .....................................................++.@@@@@@",
			"  .+++++++++++++++++++++++++++++++++++++++++++++++++++.+.@@@@@@@",
			"  .+++++++++++++++++++++++++++++++++++++++++++++++++++..@@@@@@@@",
			"  .....................................................@@@@@@@@@",
			"       .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@",
			"  .....          .....@@@@@@@@@.....@@@@@@@@@@@@@.....@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@@.@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@@..@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@@. .@@@.@@@@@@@@@@",
			"  .   .          .@@@.@@@@@@@@@.@@@.@@@@@@@@@@.  .@@@.@@@@@@@@@@",
			"  .   .         ..@@@.@@@@@@@@@.@@@.@@@@@@@@@.   .@@@.@@@@@@@@@.",
			"  .   .        . .@@@.@@@@@@@@..@@@.@@@@@@@@.    .@@@.@@@@@@@@. ",
			"  .   .       .  .@@@.@@@@@@@. .@@@.@@@@@@@.     .@@@.@@@@@@@.  ",
			"  .   .      .   .@@@.@@@@@@.  .@@@.@@@@@@.      .@@@.@@@@@@.   ",
			"  .   .     .    .@@@.@@@@@.   .@@@.@@@@@.       .@@@.@@@@@.    ",
			"  .   .    .     .@@@.@@@@.    .@@@.@@@@.        .@@@.@@@@.     ",
			"  .   .   .      .@@@.@@@.     .@@@.@@@.         .@@@.@@@.      ",
			"  .   .  .       .@@@.@@.      .@@@.@@.          .@@@.@@.       ",
			"  .   . .        .@@@.@.       .@@@.@.           .@@@.@.        ",
			"  .   ..         .@@@..        .@@@..            .@@@..         ",
			"  .....          .....         .....             .....          ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                "};
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

FreeCADGui.addCommand('Floor', Floor_Command())

