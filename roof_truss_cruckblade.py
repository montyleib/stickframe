import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "CruckBlade" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class CruckBlade_Command:
	def GetResources(slf):
		#print 'Run getResources() for CruckBlade_Command' 
		image_path = '/sketchershapes/icons/cruckblade.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'CruckBlade', 
			'ToolTip': 'Tooltip for CruckBlade command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'CruckBlade command is NOT active' 
			return False 
		else: 
			#print 'CruckBlade command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'CruckBladeCommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','CruckBlade') 
		newsampleobject = CruckBlade(b) 
		b.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute()  
class CruckBlade: 
 
 
	def __init__(self, obj):
 
		#print 'The CruckBlade class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-57.21529, 37.476, 0.0), App.Vector (-57.21529, 15.8113, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-57.21529, 15.8113, 0.0), App.Vector (-48.6204, 15.8113, 0.0)))
		geometryList.append( Part.Circle ( App.Vector (-57.21529, 37.476, 0.0), App.Vector (0.0, 0.0, 1.0), 1.0))
		geometryList.append( Part.Circle ( App.Vector (-57.21529, 49.53004266666667, 0.0), App.Vector (0.0, 0.0, 1.0), 1.0))
		geometryList.append( Part.Circle ( App.Vector (-57.21529, 58.246052, 0.0), App.Vector (0.0, 0.0, 1.0), 1.0))
		geometryList.append( Part.Circle ( App.Vector (0.0, 143.523315, 0.0), App.Vector (0.0, 0.0, 1.0), 1.0))
		geometryList.append( Part.Circle ( App.Vector (-48.6204, 15.8113, 0.0), App.Vector (0.0, 0.0, 1.0), 1.0))
		geometryList.append( Part.Circle ( App.Vector (-48.6204, 29.8, 0.0), App.Vector (0.0, 0.0, 1.0), 1.0))
		geometryList.append( Part.Circle ( App.Vector (-48.6204, 43.2929, 0.0), App.Vector (0.0, 0.0, 1.0), 1.0))
		geometryList.append( Part.Circle ( App.Vector (0.0, 131.383423, 0.0), App.Vector (0.0, 0.0, 1.0), 1.0))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 131.383423, 0.0), App.Vector (0.0, 143.523315, 0.0)))


		constraintList.append( Sketcher.Constraint('Vertical',0 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,1,0,2 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Equal',2,3))
		constraintList.append( Sketcher.Constraint('Equal',2,4))
		constraintList.append( Sketcher.Constraint('PointOnObject',5,2,-2 ) )
		constraintList.append( Sketcher.Constraint('Equal',8,2))
		constraintList.append( Sketcher.Constraint('Vertical',3,3,4,3 ) )
		constraintList.append( Sketcher.Constraint('Vertical',4,3,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',13,1,1,2 ) )
		constraintList.append( Sketcher.Constraint('Equal',9,10))
		constraintList.append( Sketcher.Constraint('Equal',9,11))
		constraintList.append( Sketcher.Constraint('Equal',9,12))
		constraintList.append( Sketcher.Constraint('Vertical',11,3,10,3 ) )
		constraintList.append( Sketcher.Constraint('Vertical',10,3,1,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',16,1,13,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',16,2,5,2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',16 ) )


		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print (' CruckBlade Class executed() ') 
FreeCADGui.addCommand('CruckBlade',CruckBlade_Command() ) 
