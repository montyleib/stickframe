import FreeCAD,FreeCADGui,Part, Draft
import os, math
from pivy import coin
import stud, plate, studspacer, framing

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url__ = "http://www.mathcodeprint.com"

__command_name__ = "Wall"
__command_group__ = "Constructions"


wall_type = ['Interior','Exterior','Load Bearing','Non-Load Bearing','Demising']
#Not sure if room name makes any sense as most walls will be part of two rooms.
wall_room = ['Living','Dining','Bedroom','Garage','Bathroom','Kitchen']
wall_direction = ['North','South','East','West']

def makeWall():
	pass

class Wall_Command:
	""" The Wall object creates a container for all the items that make up
	a stud wall.
	"""

	def GetResources(self):

		image_path = '/framing/icons/wall.png'
		global_path = FreeCAD.getHomePath()+"Mod"
		user_path = FreeCAD.getUserAppDataDir()+"Mod"
		icon_path = ""

		if os.path.exists(user_path + image_path):
			icon_path = user_path + image_path
		elif os.path.exists(global_path + image_path):
			icon_path = global_path + image_path
		return {"MenuText": "Wall",
			"ToolTip": "Add a Wall Group to the Construction",
			'Pixmap' : str(icon_path) }

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		#TODO: Move this to a makeWall() command, and it should probs go in 
		# 	  the wall class not the toolbar command class, Wall_Command

		partobj = FreeCAD.ActiveDocument.addObject('App::Part','Wall')
		partobj.addProperty("App::PropertyLength", "Length", "Assembly Dimension","Change the overall Length of the Wall").Length = "8 ft"
		partobj.addProperty("App::PropertyLength", "Height", "Assembly Dimension","Change the overall Height of the Wall").Height = "8 ft"
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

		#retrieve lumber dimensions
		#TODO: Actually get the values from a settings location
		stud_centers = FreeCAD.Units.parseQuantity('406.4 mm')
		stud_width = FreeCAD.Units.parseQuantity('3.5 in')
		stud_thickness = FreeCAD.Units.parseQuantity('1.5 in')
		adj_length = partobj.Length.getValueAs( 'mm' ) - (stud_thickness.getValueAs( 'mm') * 3 )
		length = partobj.Length.getValueAs( 'mm' ) 

		#Calculate spacing
		gaps = math.ceil ( adj_length.Value / stud_centers )
		ttl_studs = gaps
		span_gaps = gaps - 2

		gaps_length = length.Value/stud_centers

		span_gap = stud_centers - stud_thickness
		start_gap = stud_centers - stud_thickness - ( stud_thickness/2 )

		end_gap = length - ( span_gap.getValueAs( 'mm' ) * span_gaps ) - start_gap.getValueAs( 'mm' ) - ( stud_width.getValueAs( 'mm') * ttl_studs)
			
		#the only thing changin is the X of the placement
		for i in range(0, ttl_studs):
			if i == 0 :
				#first_joist, no span added
				names.append ( stud.makeStud( "Starter" ).Name )
				lengths.append ( partobj.Height - stud_thickness * 3)
				placements.append( FreeCAD.Vector ( 38.09, 88.90, -38.09)  )	
				rotations.append ( FreeCAD.Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )
			if i == 1:
				#second, add first span.
				names.append ( stud.makeStud( "Stud" ).Name )
				lengths.append ( partobj.Height - stud_thickness * 3 )
				placements.append( FreeCAD.Vector ( start_gap, 88.90, -38.09)  )
				rotations.append (FreeCAD. Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )

			if ( i > 1 and i < ttl_studs ):
				#middle_bays
				names.append ( stud.makeStud( "Stud" ).Name )
#				lengths.append ( partobj.Height - stud_thickness * 3 )
				lengths.append ( 2324.10 )
				placements.append( FreeCAD.Vector ( (stud_centers * (i - 1) + start_gap + stud_thickness ) , 88.90, -38.09)  )
				rotations.append (FreeCAD. Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )

			if i == ttl_studs -1:
				#last_joist
				names.append ( stud.makeStud( "End" ).Name )
				lengths.append ( partobj.Height - stud_thickness * 3 )	
#				placements.append( FreeCAD.Vector ( length - ( stud_width.getValueAs( 'mm') * 2 ),  88.90, -38.09)  )  
				placements.append( FreeCAD.Vector ( length ,  88.90, -38.09)  )
				rotations.append ( FreeCAD.Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )


		#Add Nailers
				names.append ( stud.makeStud( "Start_Nailer" ).Name )
				names.append ( stud.makeStud( "End_Nailer" ).Name )

				lengths.append ( partobj.Height - stud_thickness * 3 )	
				lengths.append ( partobj.Height - stud_thickness * 3 )	

				placements.append( FreeCAD.Vector ( 38.1 + 38.1 ,  0, -38.09)  )
				placements.append( FreeCAD.Vector ( length - 38.1 -38.1 ,  88.90, -38.09)  )

				rotations.append ( FreeCAD.Rotation (0.0, 0.0, 0.7071067811865475, 0.7071067811865476) )
				rotations.append ( FreeCAD.Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )	

		#Plates
		names.append( plate.makePlate ( 'Bottom' ).Name)
		names.append( plate.makePlate ( 'Top' ).Name)
		names.append( plate.makePlate ( 'Top2' ).Name)

#		lengths.append ( '2438.4 mm' )
#		lengths.append ( '2438.4 mm' )
#		lengths.append ( '2258.81 mm' )

		lengths.append ( length )
		lengths.append ( length )
		lengths.append ( length - ( stud_width.getValueAs( 'mm') * 2 ))

		placements.append( FreeCAD.Vector (0.0, 0.0, 0.0)  )
		placements.append( FreeCAD.Vector (0.0, 5.33e-13, 2324.1 + 38.1)  ) #TODO: Paramaterize
		placements.append( FreeCAD.Vector (88.10, 1.7e-14, 2324.1 + 38.1 + 38.1)  ) #TODO: Paramaterize

		rotations.append ( FreeCAD.Rotation (-0.7071067811865475, 0.0, 0.0, 0.7071067811865476) )
		rotations.append ( FreeCAD.Rotation (-0.7071067811865475, 0.0, 0.0, 0.7071067811865476) )
		rotations.append ( FreeCAD.Rotation (-0.7071067811865475, 0.0, 0.0, 0.7071067811865476) )

		#Spacers
		names.append( studspacer.makeStudspacer ( 'Studspacer' ).Name)
		names.append( studspacer.makeStudspacer ( 'Studspacer' ).Name)
		names.append( studspacer.makeStudspacer ( 'Studspacer' ).Name)
		names.append( studspacer.makeStudspacer ( 'Studspacer' ).Name)
		names.append( studspacer.makeStudspacer ( 'Studspacer' ).Name)
		names.append( studspacer.makeStudspacer ( 'Studspacer' ).Name)
		lengths.append ( '300.0 mm' )
		lengths.append ( '300.0 mm' )
		lengths.append ( '300.0 mm' )
		lengths.append ( '300.0 mm' )
		lengths.append ( '300.0 mm' )
		lengths.append ( '300.0 mm' )
		placements.append( FreeCAD.Vector (38.10, 0.0, 419.0999999999999)  )
		placements.append( FreeCAD.Vector (38.10, 0.0, 1028.6999999999998)  )
		placements.append( FreeCAD.Vector (38.10, 0.0, 1638.2999999999997)  )
		placements.append( FreeCAD.Vector (length - 76.2 , 0.0, 1638.2999999999997)  ) # TODO: Use BoardWidth * 2
		placements.append( FreeCAD.Vector (length - 76.2, 0.0, 1028.6999999999998)  )# TODO: Use BoardWidth * 2
		placements.append( FreeCAD.Vector (length - 76.2, 0.0, 419.0999999999999)  )# TODO: Use BoardWidth * 2
		rotations.append ( FreeCAD.Rotation (0.0, 0.0, 0.0, 1.0) )
		rotations.append ( FreeCAD.Rotation (0.0, 0.0, 0.0, 1.0) )
		rotations.append ( FreeCAD.Rotation (0.0, 0.0, 0.0, 1.0) )
		rotations.append ( FreeCAD.Rotation (0.0, 0.0, 0.0, 1.0) )
		rotations.append ( FreeCAD.Rotation (0.0, 0.0, 0.0, 1.0) )
		rotations.append ( FreeCAD.Rotation (0.0, 0.0, 0.0, 1.0) )

		#Studs
#		names.append( stud.makeStud ( 'Starter' ).Name)
#		names.append( stud.makeStud ( 'StarterCorner' ).Name)
#		names.append( stud.makeStud ( 'EndCorner' ).Name)
#		names.append( stud.makeStud ( 'End' ).Name)
#		lengths.append ( '2352.675 mm' )
#		lengths.append ( '2352.675 mm' )
#		lengths.append ( '2352.675 mm' )
#		lengths.append ( '2352.675 mm' )
#		placements.append( FreeCAD.Vector (0.0, 0.0, -38.1)  )
#		placements.append( FreeCAD.Vector (76.19999999999999, 0.0, -38.1)  )
#		placements.append( FreeCAD.Vector (2324.1, 0.0, -38.1)  )
#		placements.append( FreeCAD.Vector (2400.2999999999997, 0.0, -38.1)  )
#		rotations.append ( FreeCAD.Rotation (-0.0, -0.0, 0.7071067811865475, 0.7071067811865476) )
#		rotations.append ( FreeCAD.Rotation (-0.0, -0.0, 0.7071067811865475, 0.7071067811865476) )
#		rotations.append ( FreeCAD.Rotation (-0.0, -0.0, 0.7071067811865475, 0.7071067811865476) )
#		rotations.append ( FreeCAD.Rotation (0.0, 0.0, 0.7071067811865475, 0.7071067811865476) )

#		names.append( stud.makeStud ( 'Stud' ).Name)
#		names.append( stud.makeStud ( 'Stud' ).Name)
#		names.append( stud.makeStud ( 'Stud' ).Name)
#		names.append( stud.makeStud ( 'Stud' ).Name)
#		names.append( stud.makeStud ( 'Stud' ).Name)
#		lengths.append ( '2352.675 mm' )
#		lengths.append ( '2352.675 mm' )
#		lengths.append ( '2352.675 mm' )
#		lengths.append ( '2352.675 mm' )
#		lengths.append ( '2352.675 mm' )
#		placements.append( FreeCAD.Vector (444.5000000000001, 88.88999999999992, -38.099999999999994)  )
#		placements.append( FreeCAD.Vector (850.9000000000001, 88.89, -38.099999999999994)  )
#		placements.append( FreeCAD.Vector (1257.3000000000002, 88.89000000000009, -38.099999999999994)  )
#		placements.append( FreeCAD.Vector (1663.7000000000003, 88.89000000000017, -38.099999999999994)  )
#		placements.append( FreeCAD.Vector (2070.1000000000004, 88.89000000000026, -38.099999999999994)  )
#		rotations.append ( FreeCAD.Rotation (0.0, 0.0, 0.7071067811865476, -0.7071067811865476) )
#		rotations.append ( FreeCAD.Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )
#		rotations.append ( FreeCAD.Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )
#		rotations.append ( FreeCAD.Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )
#		rotations.append ( FreeCAD.Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )	
	

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

		partobj.Placement = FreeCAD.Placement ( FreeCAD.Vector ( -1.97398e-14,-3.55271e-13,38.1 ), FreeCAD.Rotation (0,0,0 ) )


		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.SendMsgToActiveView("ViewFit")	

class Wall:
	def __init__(self, obj):

		obj.addProperty("App::PropertyEnumeration","RoomName","Room","Room this wall is part of").RoomName = wall_room
		obj.addProperty("App::PropertyEnumeration","Direction","Room","Define which wall by cardinal").Direction = wall_direction 
#		obj.addExtension('Part::AttachExtensionPython', obj)
		obj.Proxy = self


	def onChanged(self, fp, prop):
		''' Do something here '''
#		if prop == "Length" or prop == "Width" or prop == "Height":
			#fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height)

	def setProperties(self, obj):
		# move property setup here 
		pass


	def execute(self,fp):
		
		#fp.ViewObject.Proxy=0
		fp.recompute()


class ViewProviderWall:
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
			static char * wall_xpm[] = {
			"102 113 46 1",
			" 	c None",
			".	c #000000",
			"+	c #E1B313",
			"@	c #101010",
			"#	c #070707",
			"$	c #040404",
			"%	c #060606",
			"&	c #D9AE18",
			"*	c #050505",
			"=	c #090909",
			"-	c #DDB21A",
			";	c #C09913",
			">	c #DFB213",
			",	c #020202",
			"'	c #DFB215",
			")	c #0C0C0C",
			"!	c #080808",
			"~	c #E0B214",
			"{	c #DDB013",
			"]	c #111111",
			"^	c #010101",
			"/	c #0D0D0D",
			"(	c #E0B315",
			"_	c #E0B216",
			":	c #0B0B0B",
			"<	c #DDB015",
			"[	c #030303",
			"}	c #0E0E0E",
			"|	c #0F0F0F",
			"1	c #DFB114",
			"2	c #DEB218",
			"3	c #D2A713",
			"4	c #DFB31B",
			"5	c #DBB11C",
			"6	c #D8AD1B",
			"7	c #E0B316",
			"8	c #E0B215",
			"9	c #E1B314",
			"0	c #DAAF19",
			"a	c #DDB116",
			"b	c #D4AB1B",
			"c	c #0A0A0A",
			"d	c #E0B213",
			"e	c #D5AC1B",
			"f	c #D8AE1A",
			"g	c #DEB115",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..     ....@+++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..    ...#$..++++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..  ...%&+++...++++..+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++......++++++++..*++..++=..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++....++++++++++-;..+..;....",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..++++++++++++++>$.....,..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..+++++++++++++++')...++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..+++++++++++++++...#+++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..+++++++++++++!..++++++..",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..++++++++++~{..]++++++...",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..++++++++++..,++++++.... ",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..++++++++^..++++++^...   ",
			"             ..++++++++..+++..       ..++++++++..+++..       ..++++++++..+++..++++++/..++++++)...     ",
			"             ..++++++++..+++..       ..++++++++..+++..      ...(+++++++..+++..+++_+..:++++++....      ",
			"             ..++++++++..+++..       ..++++++++..+++..     ....^+++++++..+++..+++..^++++++....        ",
			"             ..++++++++..+++..       ..++++++++..+++..   ....++..:+++++..+++..<[..++++++[...          ",
			"             ..++++++++..+++..       ..++++++++..+++..  ...+++++}..++++..+++....++++++|...            ",
			"             ..++++++++..+++..       ..++++++++..+++.....*+++++++1,..++..++*..%++++++....             ",
			"             ..++++++++..+++..       ..++++++++..+++....++++++++++++..,..:...)+++++....               ",
			"             ..++++++++..+++..       ..++++++++..++2..++++++++++++++~+.....#+++++%...                 ",
			"             ..++++++++..+++..       ..++++++++..+++..++++++++++++++++:...++++~;...                   ",
			"             ..++++++++..+++..       ..++++++++..+++..+++++++++++++++..[3+++++....                    ",
			"             ..++++++++..+++..       ..++++++++..+++..+++++++++++++^..++++++....                      ",
			"             ..++++++++..+++..       ..++++++++..+++..+++++++++++)..++++++!...                        ",
			"             ..++++++++..+++..       ..++++++++..+++..++++++++++..:++++++...                          ",
			"             ..++++++++..+++..       ..++++++++..+++..++++++++..^++++++....                           ",
			"             ..++++++++..+++..       ..++++++++..+++..++++++[..+4++++,...                             ",
			"             ..++++++++..+++..      ...++++++++..+++..++++|..+5++++}...                               ",
			"             ..++++++++..+++..     .....+++++++..+++..+++..=6+++++....                                ",
			"             ..++++++++..+++..   ....++...+++++..+++..+...++++++....                                  ",
			"             ..++++++++..+++.. ....+7++++..%+++..++8....+++++>$...                                    ",
			"             ..++++++++..+++.....]+++++++++..++..++^..@++++++...                                      ",
			"             ..++++++++..+++...$++++++++++9+[....[...++++++....                                       ",
			"             ..++++++++..+++..++++++++++++++++.....++++++....                                         ",
			"             ..++++++++..+++..+++++++++++++++0*..^a++++!...                                           ",
			"             ..++++++++..+++..+++++++++++++++..|+9++++...                                             ",
			"             ..++++++++..+++..+++++++++++++..,++++++....                                              ",
			"             ..++++++++..+++..+++++++++++,..+++++b,...                                                ",
			"             ..++++++++..+++..+++++++++}..+~++++/...                                                  ",
			"             ..++++++++..+++..++++++++..c++++++....                                                   ",
			"             ..++++++++..+++..++++++...++++++....                                                     ",
			"            ...++++++++..+++..++++$..++++9d[...                                                       ",
			"           .....}++++++..+++..+++..+++++++...                                                         ",
			"         ...$++)..+2+++..+++..+..*e+++++....                                                          ",
			"       ....++++++^..+++..+++....++++++....                                                            ",
			"      ...++++++++++..$+..++...++++++#...                                                              ",
			"    ...:+++++++++++';....^..^+++++3...                                                                ",
			"  ...^++++++++++++++++$....++++++....                                                                 ",
			"....++++++++++++++++++,..*+++++^...                                                                   ",
			"..+~++++++++++++++++/..++++++)...                                                                     ",
			"%++++++++++++++++++..cd+++++....                                                                      ",
			"+++++++++++++++++..^++++++....                                                                        ",
			"+++++++++++++++[..++++++[...                                                                          ",
			"++++++++++++++..++++++|...                                                                            ",
			"++++++++++++..*>+++++....                                                                             ",
			"++++++++++...++++++....                                                                               ",
			"++++++++#..+++++f#...                                                                                 ",
			"++++++{..]++++~;...                                                                                   ",
			"+++++..$++++(+....                                                                                    ",
			"+++^..++++++^...                                                                                      ",
			"+c..+++++d=...                                                                                        ",
			"..:g+++++....                                                                                         ",
			"^++++++....                                                                                           ",
			"+++++[...                                                                                             ",
			"+++}...                                                                                               ",
			"++....                                                                                                "};
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


FreeCADGui.addCommand('Wall', Wall_Command())
