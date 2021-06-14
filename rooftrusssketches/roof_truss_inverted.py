import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "Inverted" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class Inverted_Command:
	def GetResources(slf):
		#print 'Run getResources() for Inverted_Command' 
		image_path = '/sketchershapes/icons/inverted.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'Inverted', 
			'ToolTip': 'Tooltip for Inverted command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'Inverted command is NOT active' 
			return False 
		else: 
			#print 'Inverted command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'InvertedCommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','Inverted') 
		newsampleobject = Inverted(b) 
		b.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute()  
class Inverted: 
 
 
	def __init__(self, obj):
 
		#print 'The Inverted class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-306.036621, -2.767180847892295e-30, 0.0), App.Vector (306.036621, 298.23584, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (8.291862644992862e-31, 0.0, 0.0), App.Vector (8.291862644992862e-31, 149.11792, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (306.036621, 298.23584, 0.0), App.Vector (5.684341886080802e-14, 5.684341886080802e-14, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-306.036621, -2.767180847892295e-30, 0.0), App.Vector (0.0, 3.503246160812043e-46, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',1,1,-1,1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',0,1,-1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,1,0,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,-1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,-1,1 ) )
		constraintList.append( Sketcher.Constraint('Symmetric',0,1,0,2,1))


		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print (' Inverted Class executed() ') 
FreeCADGui.addCommand('Inverted',Inverted_Command() ) 
