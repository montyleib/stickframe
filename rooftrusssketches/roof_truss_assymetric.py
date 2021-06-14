import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "Assymetric" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class Assymetric_Command:
	def GetResources(slf):
		#print 'Run getResources() for Assymetric_Command' 
		image_path = '/sketchershapes/icons/assymetric.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'Assymetric', 
			'ToolTip': 'Tooltip for Assymetric command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'Assymetric command is NOT active' 
			return False 
		else: 
			#print 'Assymetric command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'AssymetricCommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','Assymetric') 
		newsampleobject = Assymetric(b) 
		b.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute()  
class Assymetric: 
 
 
	def __init__(self, obj):
 
		#print 'The Assymetric class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-363.695251, -5.560352306440874e-41, 0.0), App.Vector (0.0, 252.19868838339903, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-272.77143825, 63.04967209584976, 0.0), App.Vector (-272.77143825, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-272.77143825, 0.0, 0.0), App.Vector (-181.8476255, 126.09934419169953, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-181.8476255, 126.09934419169953, 0.0), App.Vector (-181.8476255, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-181.8476255, 0.0, 0.0), App.Vector (-90.92381275, 189.1490162875493, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-90.92381275, 189.1490162875493, 0.0), App.Vector (-90.92381275, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 252.19868838339903, 0.0), App.Vector (0.0, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 252.19868838339903, 0.0), App.Vector (155.985458, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-363.695251, -5.560352306440874e-41, 0.0), App.Vector (-272.77143825, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-272.77143825, 0.0, 0.0), App.Vector (-181.8476255, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-181.8476255, 0.0, 0.0), App.Vector (-90.92381275, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-90.92381275, 0.0, 0.0), App.Vector (0.0, 2.475253607383357e-41, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-369.567352, 0.0, 0.0), App.Vector (155.985458, 0.0, 0.0)))


		constraintList.append( Sketcher.Constraint('PointOnObject',0,2,-2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,1,0 ) )
		constraintList.append( Sketcher.Constraint('Vertical',1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,2,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',2,2,0 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,3,1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',3 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,4,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,2,0 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,2,5,1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',5 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,1,0,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,2,-1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,1,0,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',7,2,-1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',0,1,-1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,-1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,2,-1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',5,2,-1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,2,1,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',9,2,3,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',10,1,9,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',10,2,5,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',11,1,10,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',11,2,-1,1 ) )
		constraintList.append( Sketcher.Constraint('Equal',8,9))
		constraintList.append( Sketcher.Constraint('Equal',9,10))
		constraintList.append( Sketcher.Constraint('Equal',10,11))
		constraintList.append( Sketcher.Constraint('Coincident',9,1,8,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',12,1,-1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',12,2,7,2 ) )


		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print (' Assymetric Class executed() ') 
FreeCADGui.addCommand('Assymetric',Assymetric_Command() ) 
