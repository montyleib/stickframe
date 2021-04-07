import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "Rafter" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

def makeRafterSketch( name ):
		newsketch=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython',name) 
		Rafter_Sketch(newsketch) 
		newsketch.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute() 
		newsketch.Placement = FreeCAD.Placement( FreeCAD.Vector (0,-1114.03,2031.3),FreeCAD.Rotation (0.49999999999999994, -0.49999999999999994, -0.49999999999999994, 0.5000000000000001) )

		return newsketch


class Rafter_Sketch_Command:
	def GetResources(slf):
		#print 'Run getResources() for Rafter_Command' 
		image_path = '/stickframe/icons/raftersketch.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'Rafter', 
			'ToolTip': 'Tooltip for Rafter command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'Rafter command is NOT active' 
			return False 
		else: 
			#print 'Rafter command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'RafterCommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','Rafter') 
		newsampleobject = Rafter_Sketch(b) 
		b.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute()  

class Rafter_Sketch: 
 
 
	def __init__(self, obj): 
 
		#print 'The Rafter class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (0.0, 1816.2841752452775, 0.0), App.Vector (-1632.1341752452774, 184.1500000000001, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1632.1341752452774, 184.1500000000001, 0.0), App.Vector (-1632.1341752452774, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1632.1341752452774, 0.0, 0.0), App.Vector (-1546.8764916132027, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1546.8764916132027, 0.0, 0.0), App.Vector (-1219.2, 327.6764916132027, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1219.2, 327.6764916132027, 0.0), App.Vector (-1219.2, 435.626491613203, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1200.15, 435.626491613203, 0.0), App.Vector (-1111.25, 435.626491613203, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1111.25, 435.626491613203, 0.0), App.Vector (0.0, 1546.876491613203, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 1546.876491613203, 0.0), App.Vector (0.0, 1816.2841752452775, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1219.2, 435.626491613203, 0.0), App.Vector (-1200.15, 435.626491613203, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (134.7038418160373, 1681.5803334292402, 0.0), App.Vector (0.0, 1816.2841752452775, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1589.5053334292402, -42.628841816037415, 0.0), App.Vector (-1724.2091752452777, 92.07500000000002, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1219.2, 435.626491613203, 0.0), App.Vector (0.0, 1654.8264916132032, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',1,1,0,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',0,1,7,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,1,6,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,1,5,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,1,3,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,1,2,2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',7 ) )
		constraintList.append( Sketcher.Constraint('Vertical',4 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',5 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,2,5,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,1,4,2 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',8 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,-1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',6,2,-2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',9,1,6 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',10,1,3 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',10,2,0 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',11,2,7 ) )
		constraintList.append( Sketcher.Constraint('Parallel',6,0))
		constraintList.append( Sketcher.Constraint('Parallel',11,0))
		constraintList.append( Sketcher.Constraint('Parallel',3,0))
		constraintList.append( Sketcher.Constraint('Parallel',9,10))
		constraintList.append( Sketcher.Constraint('Perpendicular',6,0,9 ) )
		named_constraint = Sketcher.Constraint('DistanceX',4,2,-1,1,1219.2)
		named_constraint.Name = "Run"
		constraintList.append( named_constraint )
		constraintList.append( Sketcher.Constraint('DistanceX',8,1,8,2,19.05))
		constraintList.append( Sketcher.Constraint('DistanceX',5,1,5,2,88.9))
		constraintList.append( Sketcher.Constraint('Distance',9,0,-2000,0,190.5))
		constraintList.append( Sketcher.Constraint('Equal',10,9))
		constraintList.append( Sketcher.Constraint('Coincident',11,1,4,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,2,1 ) )
		named_constraint = Sketcher.Constraint('DistanceY',4,2,11,2,1219.2)
		named_constraint.Name = "Rise"
		constraintList.append( named_constraint )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,10 ) )
		named_constraint = Sketcher.Constraint('Distance',0,1,10,2,2438.4)
		named_constraint.Name = "BoardLength"
		constraintList.append( named_constraint )
		constraintList.append( Sketcher.Constraint('DistanceY',1,2,1,1,184.15))
		constraintList.append( Sketcher.Constraint('Coincident',9,2,0,1 ) )


		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
#		print (' Rafter_Sketch Class executed()')
FreeCADGui.addCommand('Rafter_Sketch',Rafter_Sketch_Command() ) 
