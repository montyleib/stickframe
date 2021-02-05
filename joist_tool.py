import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part
import os
class JoistTool_Command:
	def GetResources(self):
#		print 'Run getResources() for JoistTool_Command' 
		image_path = '/sketchershapes/icons/JoistTool.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'JoistTool Menu', 
			'ToolTip': 'Tooltip for JoistTool command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
#			print 'JoistTool command is NOT active' 
			return False 
		else: 
#			print 'JoistTool command IS active' 
			return True 
 
	def Activated(self): 
 
#		print 'JoistToolCommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','JoistTool') 
		newsampleobject = JoistTool(b) 
		b.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute()  
class JoistTool: 
 
 
	def __init__(self, obj): 
 
#		print 'The JoistTool class has been instantiated init' 
		obj.Proxy = self

		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-1473.1999999999998, 123.15504587155961, 0.0), App.Vector (-1307.1904509283818, 266.7, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1307.1904509283818, 266.7, 0.0), App.Vector (1307.1904509283818, 266.7, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (1307.1904509283818, 266.7, 0.0), App.Vector (1473.1999999999998, 123.1550458715596, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1473.1999999999998, 123.15504587155961, 0.0), App.Vector (-1473.1999999999998, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1473.1999999999998, 0.0, 0.0), App.Vector (1473.1999999999998, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (1473.1999999999998, 0.0, 0.0), App.Vector (1473.1999999999998, 123.15504587155961, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1473.1999999999998, 123.15504587155961, 0.0), App.Vector (-2.2737367544323206e-13, 1397.0, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1473.1999999999998, 0.0, 0.0), App.Vector (-1384.2999999999997, 0.0, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1384.2999999999997, 0.0, 0.0), App.Vector (-1384.2999999999997, 200.02499999999998, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',1,1,0,2 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,1,1,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,1,3,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,1,4,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,2,2,2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',5 ) )
		constraintList.append( Sketcher.Constraint('Vertical',3 ) )
		constraintList.append( Sketcher.Constraint('Equal',3,5))
		constraintList.append( Sketcher.Constraint('Equal',0,2))
		constraintList.append( Sketcher.Constraint('Symmetric',3,2,4,2,-2))
		constraintList.append( Sketcher.Constraint('PointOnObject',3,2,-1 ) )
		constraintList.append( Sketcher.Constraint('DistanceY',4,2,1,2,266.7))
		constraintList.append( Sketcher.Constraint('DistanceX',3,2,-1,1,1473.2))
		constraintList.append( Sketcher.Constraint('Coincident',6,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',0,2,6 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',6,2,-2 ) )
		constraintList.append( Sketcher.Constraint('DistanceY',3,2,6,2,1397.0))
		constraintList.append( Sketcher.Constraint('Horizontal',7 ) )
		constraintList.append( Sketcher.Constraint('DistanceX',7,1,7,2,88.9))
		constraintList.append( Sketcher.Constraint('Coincident',7,1,3,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,1,7,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',8,2,0 ) )
		constraintList.append( Sketcher.Constraint('Vertical',8 ) )
		constraintList.append( Sketcher.Constraint('DistanceY',8,1,8,2,200.025))


		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
#		FreeCAD.Console.PrintMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
#		print ' JoistTool Class executed()'
FreeCADGui.addCommand('JoistTool',JoistTool_Command() ) 

