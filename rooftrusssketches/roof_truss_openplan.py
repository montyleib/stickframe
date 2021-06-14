import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "OpenPlan" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class OpenPlan_Command:
	def GetResources(slf):
		#print 'Run getResources() for OpenPlan_Command' 
		image_path = '/sketchershapes/icons/openplan.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'OpenPlan', 
			'ToolTip': 'Tooltip for OpenPlan command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'OpenPlan command is NOT active' 
			return False 
		else: 
			#print 'OpenPlan command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'OpenPlanCommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','OpenPlan') 
		newsampleobject = OpenPlan(b) 
		b.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute()  
class OpenPlan: 
 
 
	def __init__(self, obj):
 
		#print 'The OpenPlan class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-373.54892489660926, 0.0, 0.0), App.Vector (0.0, 359.28739897807606, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 359.28739897807606, 0.0), App.Vector (373.5489248966092, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-373.54892489660926, 0.0, 0.0), App.Vector (373.54892489660926, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-247.04075159508955, 0.0, 0.0), App.Vector (-247.04075159508955, 121.6782849731159, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-134.31910986850124, 230.09638703483088, 0.0), App.Vector (134.31910986850124, 230.09638703483088, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (247.04075159508955, 121.6782849731159, 0.0), App.Vector (247.04075159508955, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-247.04075159508955, 0.0, 0.0), App.Vector (-307.83382955093396, 63.2061936381664, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (247.04075159508955, 0.0, 0.0), App.Vector (307.83382955093396, 63.2061936381664, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 230.0963870348309, 0.0), App.Vector (0.0, 359.28739897807606, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',1,1,0,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,-1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,1,2 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,1,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,2,0 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,1,0 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,2,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',4 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',5,1,1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',5 ) )
		constraintList.append( Sketcher.Constraint('Vertical',3 ) )
		constraintList.append( Sketcher.Constraint('Symmetric',3,2,5,1,-2))
		constraintList.append( Sketcher.Constraint('PointOnObject',0,2,-2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,1,3,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',6,2,0 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,1,5,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',7,2,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',8,1,4 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,2,0,2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',8 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',5,2,2 ) )
		constraintList.append( Sketcher.Constraint('Perpendicular',6,0,0 ) )
		constraintList.append( Sketcher.Constraint('Perpendicular',1,0,7 ) )


		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print (' OpenPlan Class executed() ') 
FreeCADGui.addCommand('OpenPlan',OpenPlan_Command() ) 
