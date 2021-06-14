import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "MonoA" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class MonoA_Command:
	def GetResources(slf):
		#print 'Run getResources() for MonoA_Command' 
		image_path = '/sketchershapes/icons/monoa.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'MonoA', 
			'ToolTip': 'Tooltip for MonoA command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'MonoA command is NOT active' 
			return False 
		else: 
			#print 'MonoA command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'MonoACommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','MonoA') 
		newsampleobject = MonoA(b) 
		b.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute()  
class MonoA: 
 
 
	def __init__(self, obj):
 
		#print 'The MonoA class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-402.0118811282057, 0.0, 0.0), App.Vector (5.684341886080802e-14, 397.534418, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (5.684341886080802e-14, 397.53441799999996, 0.0), App.Vector (5.684341886080802e-14, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (5.684341886080802e-14, 0.0, 0.0), App.Vector (-402.0118811282057, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-201.00594056410284, 0.0, 0.0), App.Vector (-201.00594056410284, 198.76720899999998, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-201.00594056410284, 198.76720899999998, 0.0), App.Vector (5.684341886080802e-14, -2.842170943040401e-14, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',1,1,0,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,-1,1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,1,1,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,0,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,2,0 ) )
		constraintList.append( Sketcher.Constraint('Vertical',3 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,1,3,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,2,1,2 ) )
		constraintList.append( Sketcher.Constraint('Symmetric',0,1,1,2,3))


		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print (' MonoA Class executed() ') 
FreeCADGui.addCommand('MonoA',MonoA_Command() ) 
