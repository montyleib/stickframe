import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "MonoB" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class MonoB_Command:
	def GetResources(slf):
		#print 'Run getResources() for MonoB_Command' 
		image_path = '/sketchershapes/icons/monob.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'MonoB', 
			'ToolTip': 'Tooltip for MonoB command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'MonoB command is NOT active' 
			return False 
		else: 
			#print 'MonoB command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'MonoBCommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','MonoB') 
		newsampleobject = MonoB(b) 
		b.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute()  
class MonoB: 
 
 
	def __init__(self, obj):
 
		#print 'The MonoB class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-470.466644, -6.162975822039155e-31, 0.0), App.Vector (-5.684341886080802e-14, 340.36441, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-5.684341886080802e-14, 340.36441, 0.0), App.Vector (-5.684341886080802e-14, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-5.684341886080802e-14, -6.162975822039155e-31, 0.0), App.Vector (-470.466644, -6.162975822039155e-31, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-313.6444293333333, 113.45480333333333, 0.0), App.Vector (-235.233322, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-235.233322, 0.0, 0.0), App.Vector (-156.82221466666667, 226.90960666666666, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-156.82221466666667, 226.90960666666666, 0.0), App.Vector (-8.526512829121202e-14, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-470.466644, -6.162975822039155e-31, 0.0), App.Vector (-313.6444293333333, 113.45480333333334, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-313.6444293333333, 113.45480333333333, 0.0), App.Vector (-156.82221466666667, 226.90960666666666, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-156.82221466666667, 226.90960666666666, 0.0), App.Vector (-5.684341886080802e-14, 340.36441, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',0,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,-1,1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,2,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',0,1,2,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,1,0 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,4,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,2,0 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,2,5,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,2,1,2 ) )
		constraintList.append( Sketcher.Constraint('Symmetric',0,1,1,2,3))
		constraintList.append( Sketcher.Constraint('Coincident',6,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,2,3,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,2,4,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,1,6,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,1,7,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,2,0,2 ) )
		constraintList.append( Sketcher.Constraint('Equal',8,7))
		constraintList.append( Sketcher.Constraint('Equal',7,6))


		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print (' MonoB Class executed() ') 
FreeCADGui.addCommand('MonoB',MonoB_Command() ) 
