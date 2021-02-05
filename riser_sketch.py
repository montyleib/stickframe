import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "Riser_Sketch" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class Riser_Sketch_Command:
	def GetResources(self):
		#print 'Run getResources() for Riser_Sketch_Command' 
		image_path = '/sketchershapes/icons/riser_sketch.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'Riser_Sketch', 
			'ToolTip': 'Tooltip for Riser_Sketch command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'Riser_Sketch command is NOT active' 
			return False 
		else: 
			#print 'Riser_Sketch command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'Riser_SketchCommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','Riser_Sketch') 
		newsampleobject = Riser_Sketch(b) 
		b.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute()  
class Riser_Sketch: 
 

	def __init__(self, obj): 
 
		#print 'The Riser_Sketch class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-279.4, 355.6, 0.0), App.Vector (-260.34999999999997, 355.6, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-260.34999999999997, 355.6, 0.0), App.Vector (-260.34999999999997, 203.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-260.34999999999997, 203.2, 0.0), App.Vector (-279.4, 203.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-279.4, 203.2, 0.0), App.Vector (-279.4, 355.6, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',0,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,2,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,3,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,0,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',0 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',3 ) )
		constraintList.append( Sketcher.Constraint('DistanceY',-1,1,2,2,203.2))
		constraintList.append( Sketcher.Constraint('DistanceY',3,1,3,2,152.4))
		constraintList.append( Sketcher.Constraint('DistanceX',0,1,0,2,19.05))
		constraintList.append( Sketcher.Constraint('DistanceX',2,2,-1,1,279.4))


		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print ' Riser_Sketch Class executed()'
FreeCADGui.addCommand('Riser_Sketch',Riser_Sketch_Command() ) 
