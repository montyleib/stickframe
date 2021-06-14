import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "Storage" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class Storage_Command:
	def GetResources(slf):
		#print 'Run getResources() for Storage_Command' 
		image_path = '/sketchershapes/icons/storage.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'Storage', 
			'ToolTip': 'Tooltip for Storage command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'Storage command is NOT active' 
			return False 
		else: 
			#print 'Storage command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'StorageCommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','Storage') 
		newsampleobject = Storage(b) 
		b.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute()  
class Storage: 
 
 
	def __init__(self, obj):
 
		#print 'The Storage class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-405.530396, -1.1737312160261198e-31, 0.0), App.Vector (0.0, 390.17266173470676, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1.2127674758214812e-29, 390.17266173470676, 0.0), App.Vector (405.5303959999999, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (405.5303959999999, -1.1737312160261198e-31, 0.0), App.Vector (-405.530396, -1.1737312160261198e-31, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-198.78692216059636, -1.1737312160261198e-31, 0.0), App.Vector (-198.78692216059636, 198.91394647566653, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-198.78692216059636, 198.91394647566653, 0.0), App.Vector (198.78692216059636, 198.91394647566653, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (198.78692216059636, 198.91394647566653, 0.0), App.Vector (198.78692216059636, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1.2127674758214812e-29, 198.91394647566653, 0.0), App.Vector (-1.2127674758214812e-29, 390.17266173470676, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-198.78692216059636, -1.1737312160261198e-31, 0.0), App.Vector (-298.1698231166517, 103.29474905071974, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (198.78692216059636, -1.1737312159974212e-31, 0.0), App.Vector (298.1698231166517, 103.29474905071969, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',0,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,-1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,2,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,0,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',0,2,-2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,1,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,2,0 ) )
		constraintList.append( Sketcher.Constraint('Vertical',3 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,1,3,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,2,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',4 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,1,4,2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',5 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,2,0,2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',6 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,1,3,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',7,2,0 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,1,5,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',8,2,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',5,2,2 ) )
		constraintList.append( Sketcher.Constraint('Perpendicular',1,0,8 ) )
		constraintList.append( Sketcher.Constraint('Perpendicular',0,0,7 ) )
		constraintList.append( Sketcher.Constraint('Symmetric',3,2,4,2,6))


		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print (' Storage Class executed() ') 
FreeCADGui.addCommand('Storage',Storage_Command() ) 
