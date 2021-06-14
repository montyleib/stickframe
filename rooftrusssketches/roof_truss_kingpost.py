import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "KingPost" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class KingPost_Command:
	def GetResources(slf):
		#print 'Run getResources() for KingPost_Command' 
		image_path = '/sketchershapes/icons/kingpost.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'KingPost', 
			'ToolTip': 'Tooltip for KingPost command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'KingPost command is NOT active' 
			return False 
		else: 
			#print 'KingPost command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'KingPostCommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','KingPost') 
		newsampleobject = KingPost(b) 
		b.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute()  
class KingPost: 
 
 
	def __init__(self, obj):
 
		#print 'The KingPost class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-394.45751999999993, 0.0, 0.0), App.Vector (0.0, 354.675873, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 354.675873, 0.0), App.Vector (360.374542, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (360.374542, 0.0, 0.0), App.Vector (-394.45751999999993, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 0.0, 0.0), App.Vector (0.0, 354.675873, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',0,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,-1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,2,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,0,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',-1,1,3,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,0,2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',3 ) )


		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print (' KingPost Class executed() ') 
FreeCADGui.addCommand('KingPost',KingPost_Command() ) 
