import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "Guides " #Name of the command to appear in Toolbar
__command_group__ = "Members" #Name of Toolbar to assign the command

class Guides_Command:
	def GetResources(self):
		print 'Run getResources() for Guides_Command' 
		image_path = '/sketchershapes/icons/Guides.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'Guides', 
			'ToolTip': 'Tooltip for Guides command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'Guides command is NOT active' 
			return False 
		else: 
			#print 'Guides command IS active' 
			return True 
 
	def Activated(self): 
		#print 'GuidesCommand activated' 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','Guides')
		newsampleobject = Guides(b)
		b.ViewObject.Proxy=0
		FreeCAD.ActiveDocument.recompute()

class Guides: 
	def __init__(self, obj): 
 
		#print 'The Guides class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		constructionList.append( Part.LineSegment( App.Vector (0.0, 1625.6000000000001, 0.0), App.Vector (-1473.1999999999998, 152.39999999999986, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1473.1999999999998, 152.39999999999998, 0.0), App.Vector (-1473.1999999999998, 0.0, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1473.1999999999998, 0.0, 0.0), App.Vector (-1356.1923163679253, 0.0, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1356.1923163679253, 0.0, 0.0), App.Vector (-1219.1999999999998, 136.9923163679254, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1219.1999999999998, 136.9923163679254, 0.0), App.Vector (-1219.1999999999998, 244.9423163679255, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1200.1499999999999, 244.9423163679255, 0.0), App.Vector (-1111.2499999999998, 244.9423163679255, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1111.2499999999998, 244.9423163679255, 0.0), App.Vector (0.0, 1356.1923163679255, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (0.0, 1356.1923163679255, 0.0), App.Vector (0.0, 1625.6000000000001, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (0.0, 1356.1923163679255, 0.0), App.Vector (-134.70384181603734, 1490.8961581839628, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1219.1999999999998, 136.9923163679254, 0.0), App.Vector (-1353.9038418160371, 271.6961581839627, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1219.1999999999998, 244.9423163679255, 0.0), App.Vector (0.0, 1464.1423163679256, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1219.1999999999998, 244.9423163679255, 0.0), App.Vector (-1200.1499999999999, 244.9423163679255, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1219.1999999999998, 244.9423163679255, 0.0), App.Vector (0.0, 244.9423163679255, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 1464.1423163679256, 0.0), App.Vector (0.0, 244.9423163679255, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-270.08232801349715, 1355.517671986503, 0.0), App.Vector (-574.8823280134972, 1355.517671986503, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-574.8823280134972, 1355.517671986503, 0.0), App.Vector (-574.8823280134972, 1050.717671986503, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-574.8823280134972, 1050.717671986503, 0.0), App.Vector (-270.08232801349715, 1355.517671986503, 0.0)))
		tmpCircle = Part.Circle ( App.Vector (-1219.1999999999998, 244.9423163679255, 0.0), App.Vector (0.0, 0.0, 1.0), 524.334872471)
		geometryList.append( Part.ArcOfCircle (  tmpCircle, 1e-16, 0.785398163397))


		constraintList.append( Sketcher.Constraint('Coincident',0,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,2,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,3,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,4,1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',4 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',5 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,2,6,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,2,7,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,2,0,1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',7 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',0,1,-2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,-1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,1,6,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',8,2,0 ) )
		constraintList.append( Sketcher.Constraint('Perpendicular',0,0,8 ) )
		constraintList.append( Sketcher.Constraint('Coincident',9,1,3,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',9,2,0 ) )
		constraintList.append( Sketcher.Constraint('Equal',9,8))
		constraintList.append( Sketcher.Constraint('Distance',8,0,-2000,0,190.5))
		constraintList.append( Sketcher.Constraint('Perpendicular',0,0,9 ) )
		named_constriant = Sketcher.Constraint('DistanceX',4,2,-1,1,1219.2)
		named_constriant.Name = "Run"
		constraintList.append( named_constriant )
		constraintList.append( Sketcher.Constraint('PointOnObject',10,2,7 ) )
		named_constriant = Sketcher.Constraint('DistanceY',5,2,10,2,1219.2)
		named_constriant.Name = "Rise"
		constraintList.append( named_constriant )
		constraintList.append( Sketcher.Constraint('Coincident',4,2,10,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',11,1,4,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',11,2,5,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',11 ) )
		named_constriant = Sketcher.Constraint('DistanceX',5,1,5,2,88.9)
		named_constriant.Name = "TopPlate"
		constraintList.append( named_constriant )
		named_constriant = Sketcher.Constraint('DistanceX',11,1,11,2,19.05)
		named_constriant.Name = "Sheathing"
		constraintList.append( named_constriant )
		named_constriant = Sketcher.Constraint('DistanceY',1,2,1,1,152.4)
		named_constriant.Name = "Fascia"
		constraintList.append( named_constriant )
		named_constriant = Sketcher.Constraint('DistanceX',1,2,3,2,254.0)
		named_constriant.Name = "Overhang"
		constraintList.append( named_constriant )
		constraintList.append( Sketcher.Constraint('PointOnObject',12,2,-2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',12,1,10,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',12 ) )
		constraintList.append( Sketcher.Constraint('Coincident',13,1,10,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',13,2,12,2 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',14 ) )
		constraintList.append( Sketcher.Constraint('Coincident',14,2,15,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',15,2,16,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',16,2,14,1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',15 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',14,1,0 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',15,2,0 ) )
		constraintList.append( Sketcher.Constraint('DistanceX',14,2,14,1,304.8))
		constraintList.append( Sketcher.Constraint('Coincident',17,3,10,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',17,2,10 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',17,1,12 ) )

		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

		#View properties

		obj.ViewObject.LineWidth = 2.00
		obj.ViewObject.LineColor = (0.33,0.67,1.00)
		obj.ViewObject.DrawStyle = u"Dashed" 

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print ' Guides Class executed()'
FreeCADGui.addCommand('Guides',Guides_Command() ) 
