import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "QueenPost" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class QueenPost_Command:
	def GetResources(slf):
		#print 'Run getResources() for QueenPost_Command' 
		image_path = '/sketchershapes/icons/queenpost.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'QueenPost', 
			'ToolTip': 'Tooltip for QueenPost command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'QueenPost command is NOT active' 
			return False 
		else: 
			#print 'QueenPost command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'QueenPostCommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','QueenPost') 
		newsampleobject = QueenPost(b) 
		b.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute()  
class QueenPost: 
 
 
	def __init__(self, obj):
 
		#print 'The QueenPost class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-383.81597040338363, 0.0, 0.0), App.Vector (0.0, 352.273682, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 352.273682, 0.0), App.Vector (383.8159704033835, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (383.8159704033835, 0.0, 0.0), App.Vector (-383.81597040338363, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 0.0, 0.0), App.Vector (0.0, 352.273682, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 0.0, 0.0), App.Vector (-184.84108627995724, 182.62297679279894, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 0.0, 0.0), App.Vector (184.84108627995724, 182.62297679279894, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',0,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,-1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,2,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,0,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,1,-1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,0,2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',3 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,1,3,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,2,0 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,1,3,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',5,2,1 ) )
		constraintList.append( Sketcher.Constraint('Symmetric',4,2,5,2,3))


		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print (' QueenPost Class executed() ') 
FreeCADGui.addCommand('QueenPost',QueenPost_Command() ) 
