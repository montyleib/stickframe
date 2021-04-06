import FreeCAD,FreeCADGui,Part, Draft, Sketcher
import os
import framing, stud, floorjoist, floorpanel, panel, header
import itertools

__title__="FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"

__command_name__ = "Door"
__command_group__ = "Constructions"

class Door_Command:
	def GetResources(slf):
		icon_path = framing.getIconImage( "door" ) 	

#		image_path = "/" + framing.mod_name + '/icons/door.png'
		# image_path = '/stickframe/icons/door.png' 
		# global_path = FreeCAD.getHomePath()+'Mod' 
		# user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		# icon_path = '' 

		# if os.path.exists(user_path + image_path): 
		# 	icon_path = user_path + image_path 
		# elif os.path.exists(global_path + image_path): 
		# 	icon_path = global_path + image_path 
		return {'MenuText': 'Door', 
			'ToolTip': 'Add a door rough out to the construction.', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'Door command is NOT active' 
			return False 
		else: 
			#print 'Door command IS active' 
			return True 
 
	def Activated(self): 
		#print 'DoorCommand activated' 

#		grpobj = FreeCAD.activeDocument().addObject('App::DocumentObjectGroupPython','DoorGrp')
#		Door(grpobj)
#		ViewProviderDoor(grpobj.ViewObject)	
		FreeCAD.ActiveDocument.recompute()
 
		partobj = FreeCAD.ActiveDocument.addObject('App::Part','Door')
		partobj.addProperty("App::PropertyLength", "Length", "Assembly Dimension","Change the overall length of the Door").Length = "3352.800"
		partobj.addProperty("App::PropertyLength", "Width", "Assembly Dimension","Change the overall width of the Door").Width = "2743.2"

		partobj.addExtension('Part::AttachExtensionPython')

		b =FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','DoorSketch') 

		b.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000,0.000000,0.000000),FreeCAD.Rotation(-0.707107,0.000000,0.000000,-0.707107))
		newsketch = DoorSketch(b) 

		b.ViewObject.Proxy=0
		FreeCAD.ActiveDocument.recompute()
		partobj.addObject ( FreeCAD.ActiveDocument.getObject( b.Name ) )



		names = []

		names.append ( stud.makeStud('KingStud').Name )
		names.append ( stud.makeStud('JackStud').Name )
		names.append ( stud.makeStud('JackStud').Name )
		names.append ( stud.makeStud('KingStud').Name )
#		names.append ( stud.makeStud('Cripple').Name )
		names.append ( header.makeHeader('DoorHeader').Name )
		names.append ( header.makeHeader('DoorHeader').Name )
#		names.append ( panel.makePanel('HeaderShim').Name )

		lengths = []

		lengths.append ( '2352.67 mm' )
		lengths.append ( '2095.5 mm' )
		lengths.append ( '2095.5 mm' )
		lengths.append ( '2352.68 mm' )
#		lengths.append ( '50.8 mm' )
		lengths.append ( '1308.1 mm' )
		lengths.append ( '1308.1 mm' )
#		lengths.append ( '1231.9 mm' )

		placements = []

		placements.append ( FreeCAD.Vector (38.1, 38.1, 0.0) )
		placements.append ( FreeCAD.Vector (89.3759784728, -592.129214178, -8e-15) )
		placements.append ( FreeCAD.Vector (89.37597847279994, -1709.729214178, 0.0) )
		placements.append ( FreeCAD.Vector (89.37597847279994, -1747.829214178, 0.0) )

		placements.append ( FreeCAD.Vector (0.475978472800008, -554.0292141780001, 2098.67) )
		placements.append ( FreeCAD.Vector (54.45097847279999, -554.0292141780001, 2098.67) )
#		placements.append ( FreeCAD.Vector (54.4509784728025, -554.0292141780001, 2098.67) )


		rotations = []

		rotations.append ( FreeCAD.Rotation (0.0, 0.0, -0.7071067811865477, 0.7071067811865474) )
		rotations.append ( FreeCAD.Rotation (0.0, 0.0, -0.7071067811865477, 0.7071067811865474) )
		rotations.append ( FreeCAD.Rotation (0.0, 0.0, -0.7071067811865477, 0.7071067811865474) )
		rotations.append ( FreeCAD.Rotation (0.0, 0.0, -0.7071067811865477, 0.7071067811865474) )
		rotations.append ( FreeCAD.Rotation (0.0, 0.0, 0.7071067811865476, -0.7071067811865475) )
		rotations.append ( FreeCAD.Rotation (0.0, 0.0, 0.7071067811865476, -0.7071067811865475) )


		for name, placement in zip ( names, placements ):
			FreeCAD.ActiveDocument.getObject( name ).Placement.Base = placement

		for name, rotation in zip ( names, rotations ):
			FreeCAD.ActiveDocument.getObject( name ).Placement.Rotation = rotation

		for name, length in zip ( names, lengths ):
#			grpobj.addObject ( FreeCAD.ActiveDocument.getObject( name ) )
#			FreeCAD.ActiveDocument.getObject( name ).Length = length

			partobj.addObject ( FreeCAD.ActiveDocument.getObject( name ) )
			FreeCAD.ActiveDocument.getObject( name ).Length = length

		expressionslist = []
		expressions = []

		expressions.append( ['Placement.Base.x','DoorSketch.Shape.Edge4.Vertex1.X'] )
		expressions.append( ['Placement.Base.y','DoorSketch.Shape.Edge4.Vertex1.Y + 38.09'] )
		expressions.append( ['Placement.Base.z','DoorSketch.Shape.Edge4.Vertex1.Z'] )
		expressionslist.append( expressions )
		expressions = []
		expressions.append( ['Length','DoorSketch.Constraints.RoughOpeningHeight'] )
		expressions.append( ['Placement.Base.x','DoorSketch.Shape.Edge4.Vertex1.X'] )
		expressions.append( ['Placement.Base.y','DoorSketch.Shape.Edge4.Vertex1.Y'] )
		expressions.append( ['Placement.Base.z','DoorSketch.Shape.Edge4.Vertex1.Z'] )
		expressionslist.append( expressions )
		expressions = []
		expressions.append( ['Length','DoorSketch.Constraints.RoughOpeningHeight'] )
		expressions.append( ['Placement.Base.x','DoorSketch.Shape.Edge2.Vertex2.X'] )
		expressions.append( ['Placement.Base.y','DoorSketch.Shape.Edge2.Vertex2.Y - 38.09'] )
		expressions.append( ['Placement.Base.z','DoorSketch.Shape.Edge2.Vertex2.Z'] )
		expressionslist.append( expressions )
		expressions = []
		expressions.append( ['Placement.Base.x','DoorSketch.Shape.Edge2.Vertex2.X'] )
		expressions.append( ['Placement.Base.y','DoorSketch.Shape.Edge2.Vertex2.Y - 38.09 - 38.09'] )
		expressions.append( ['Placement.Base.z','DoorSketch.Shape.Edge2.Vertex2.Z'] )
		expressionslist.append( expressions )
		expressions = []
		expressions.append( ['Length','DoorSketch.Constraints.RoughOpeningWidth + 3"'] )
		expressions.append( ['Placement.Base.x','DoorSketch.Shape.Edge1.Vertex1.X - 38.09'] )
		expressions.append( ['Placement.Base.y','DoorSketch.Shape.Edge1.Vertex1.Y + 38.09'] )
		expressions.append( ['Placement.Base.z','DoorSketch.Shape.Edge1.Vertex1.Z + 38.09'] )
		expressionslist.append( expressions )
		expressions = []
		expressions.append( ['Length','DoorSketch.Constraints.RoughOpeningWidth + 3"'] )
		expressions.append( ['Placement.Base.x','DoorSketch.Shape.Edge1.Vertex1.X - 38.09 - 38.09 - 12.7'] )
		expressions.append( ['Placement.Base.y','DoorSketch.Shape.Edge1.Vertex1.Y + 38.09'] )
		expressions.append( ['Placement.Base.z','DoorSketch.Shape.Edge1.Vertex1.Z + 38.09'] )
		expressionslist.append( expressions )
		expressions = []
			
		for name, expressions in zip( names, expressionslist):
		#	print ( name )
			for label, expression in expressions:
		#		print ("\t{}".format(expression) )

				obj = FreeCAD.ActiveDocument.getObject( name )
				obj.setExpression ( label, expression  )

		#Placement [Pos=(35.1117,-555.822,1.12508), Yaw-Pitch-Roll=(0,0,0)]

		partobj.Placement = FreeCAD.Placement ( FreeCAD.Vector ( 35.1117,-555.822,1.12508 ), FreeCAD.Rotation (0,0,0 ) )

		FreeCADGui.SendMsgToActiveView("ViewFit")	
		FreeCAD.ActiveDocument.recompute()

class DoorSketch: 
	def __init__(self, obj): 
 
		#print 'The Door class has been instantiated init' 
		obj.Proxy = self 
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (38.09999999999991, 2095.5, 0.0), App.Vector (1117.6, 2095.5, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (1117.6, 2095.5, 0.0), App.Vector (1117.6, 812.8, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (1117.6, 812.8, 0.0), App.Vector (38.09999999999991, 812.8, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (38.09999999999991, 812.8, 0.0), App.Vector (38.09999999999991, 2095.5, 0.0)))

		constraintList.append( Sketcher.Constraint('Coincident',0,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,2,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,3,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,0,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',0 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',3 ) )
		constraintList.append( Sketcher.Constraint('DistanceX',2,2,-2000,0,38.1))
		named_constraint = Sketcher.Constraint('DistanceX',0,1,0,2,1231.9)
		named_constraint.Name = "RoughOpeningWidth"
		constraintList.append( named_constraint )
		named_constraint = Sketcher.Constraint('DistanceY',-1,1,0,1,2032.0)
		named_constraint.Name = "RoughOpeningHeight"
		constraintList.append( named_constraint )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,-1 ) )

		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

		obj.Placement = FreeCAD.Placement( FreeCAD.Vector (38.10000000000001, 38.1, 0.0),FreeCAD.Rotation (-0.49999999999999983, 0.4999999999999999, 0.5000000000000001, -0.4999999999999999) )

		obj.Visibility = False

		#FreeCAD.ActiveDocument.recompute()

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 


	def execute(self,fp):	
		#fp.Placement.multiply( FreeCAD.Placement( FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,90) )  )
		fp.recompute()
		#print ( 'Door Class executed()' )		


FreeCADGui.addCommand('Door',Door_Command() ) 
