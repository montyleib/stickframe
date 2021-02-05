import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "Stringer_Sketch" #Name of the command to appear in Toolbar
__command_group__ = "Constructions" #Name of Toolbar to assign the command


def makeStringerSketch( name ):
		newsketch=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython',name) 
		Stringer_Sketch(newsketch) 
		newsketch.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute() 
		newsketch.Placement = FreeCAD.Placement( FreeCAD.Vector (1219.2,-38.1,0),FreeCAD.Rotation (0.7071067811865476, 0.0, 0.0, 0.7071067811865475) )

		newsketch.Placement.Rotation = FreeCAD.Rotation (4.329780281177467e-17, 0.7071067811865476, 0.7071067811865475, 4.329780281177466e-17)

		return newsketch


class Stringer_Sketch_Command:
	def GetResources(self):
		#print 'Run getResources() for Stringer_Sketch_Command' 
		image_path = '/framing/icons/stringer_sketch.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'Stringer_Sketch', 
			'ToolTip': 'Tooltip for Stringer_Sketch command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'Stringer_Sketch command is NOT active' 
			return False 
		else: 
			#print 'Stringer_Sketch command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'Stringer_SketchCommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','Stringer_Sketch') 
		newsketch = Stringer_Sketch(b) 
		b.ViewObject.Proxy=0 
		newsketch.Placement = FreeCAD.Placement( FreeCAD.Vector (1219.2,-38.1,0),FreeCAD.Rotation (0.7071067811865476, 0.0, 0.0, 0.7071067811865475) )

		newsketch.Placement.Rotation = FreeCAD.Rotation (4.329780281177467e-17, 0.7071067811865476, 0.7071067811865475, 4.329780281177466e-17)

		FreeCAD.ActiveDocument.recompute()  

class Stringer_Sketch: 
 
 
	def __init__(self, obj): 
 
		#print 'The Stringer_Sketch class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-2235.2, 1422.4, 0.0), App.Vector (-1955.8, 1422.4, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1955.8, 1422.4, 0.0), App.Vector (-1955.8, 1244.6000000000001, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-2235.2, 1422.4, 0.0), App.Vector (-2235.2, 1244.6000000000001, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-279.4, 0.0, 0.0), App.Vector (0.0, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 0.0, 0.0), App.Vector (0.0, 177.8, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 177.8, 0.0), App.Vector (-279.4, 177.8, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-2235.2, 1244.6000000000001, 0.0), App.Vector (-279.4000000000001, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1955.8, 1244.6000000000001, 0.0), App.Vector (-1676.3999999999999, 1244.6000000000001, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1676.3999999999999, 1244.6000000000001, 0.0), App.Vector (-1676.3999999999999, 1066.8, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1676.3999999999999, 1066.8, 0.0), App.Vector (-1397.0, 1066.8, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1397.0, 1066.8, 0.0), App.Vector (-1397.0, 889.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1397.0, 889.0, 0.0), App.Vector (-1117.6, 889.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1117.6, 889.0, 0.0), App.Vector (-1117.6, 711.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1117.6, 711.2, 0.0), App.Vector (-838.1999999999999, 711.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-838.1999999999999, 711.2, 0.0), App.Vector (-838.1999999999999, 533.4, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-838.1999999999999, 533.4, 0.0), App.Vector (-558.8, 533.4, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-558.8, 533.4, 0.0), App.Vector (-558.8, 355.6, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-558.8, 355.6, 0.0), App.Vector (-279.4, 355.6, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-279.4, 355.6, 0.0), App.Vector (-279.4, 177.8, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-2154.6670588235297, 1548.9517647058829, 0.0), App.Vector (80.53294117647056, 126.5517647058823, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-2235.2, 1422.4, 0.0), App.Vector (0.0, 0.0, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-2154.6670588235297, 1548.9517647058829, 0.0), App.Vector (-2315.732941176471, 1295.8482352941182, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (80.53294117647059, 126.55176470588236, 0.0), App.Vector (-80.53294117647062, -126.55176470588233, 0.0)))


		constraintList.append( Sketcher.Constraint('Vertical',2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',8 ) )
		constraintList.append( Sketcher.Constraint('Vertical',10 ) )
		constraintList.append( Sketcher.Constraint('Vertical',12 ) )
		constraintList.append( Sketcher.Constraint('Vertical',14 ) )
		constraintList.append( Sketcher.Constraint('Vertical',16 ) )
		constraintList.append( Sketcher.Constraint('Vertical',18 ) )
		constraintList.append( Sketcher.Constraint('Vertical',4 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',0 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',7 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',9 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',11 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',13 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',15 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',17 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',5 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',3 ) )
		constraintList.append( Sketcher.Constraint('Equal',2,1))
		constraintList.append( Sketcher.Constraint('Equal',1,8))
		constraintList.append( Sketcher.Constraint('Equal',8,10))
		constraintList.append( Sketcher.Constraint('Equal',10,12))
		constraintList.append( Sketcher.Constraint('Equal',12,14))
		constraintList.append( Sketcher.Constraint('Equal',14,16))
		constraintList.append( Sketcher.Constraint('Equal',16,18))
		constraintList.append( Sketcher.Constraint('Equal',18,4))
		constraintList.append( Sketcher.Constraint('Equal',0,7))
		constraintList.append( Sketcher.Constraint('Equal',7,9))
		constraintList.append( Sketcher.Constraint('Equal',9,11))
		constraintList.append( Sketcher.Constraint('Equal',11,13))
		constraintList.append( Sketcher.Constraint('Equal',13,15))
		constraintList.append( Sketcher.Constraint('Equal',15,17))
		constraintList.append( Sketcher.Constraint('Equal',17,5))
		constraintList.append( Sketcher.Constraint('Equal',5,3))
		constraintList.append( Sketcher.Constraint('Coincident',0,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,2,8,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,1,1,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',9,1,8,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',10,1,9,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',11,1,10,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',12,1,11,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',13,1,12,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',13,2,14,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',15,1,14,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',16,1,15,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',16,2,17,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',18,1,17,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,2,18,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,2,5,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,4,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,1,6,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,1,2,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,-1,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',0,2,19 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,2,19 ) )
		constraintList.append( Sketcher.Constraint('Coincident',20,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',20,2,3,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',21,1,19,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',22,1,19,2 ) )
		constraintList.append( Sketcher.Constraint('Perpendicular',20,0,21 ) )
		constraintList.append( Sketcher.Constraint('Perpendicular',22,0,20 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,2,22 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',0,1,21 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',21,2,6 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',22,2,6 ) )
		constraintList.append( Sketcher.Constraint('DistanceY',1,2,1,1,177.8))
		constraintList.append( Sketcher.Constraint('DistanceX',0,1,0,2,279.4))

		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
#		print (' Stringer_Sketch Class executed()')
FreeCADGui.addCommand('Stringer_Sketch',Stringer_Sketch_Command() ) 
