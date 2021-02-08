import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"

__command_name__ = "RafterCalculator" #Name of the command to appear in Toolbar
__command_group__ = "Constructions" #Name of Toolbar to assign the command

class RafterCalculator_Command:
	def GetResources(slf):
		#print 'Run getResources() for RafterCalculator_Command' 
		image_path = '/stickframe/icons/raftercalculator.png' 
		global_path = FreeCAD.getHomePath()+'Mod' 
		user_path = FreeCAD.getUserAppDataDir()+'Mod' 
		icon_path = '' 

		if os.path.exists(user_path + image_path): 
			icon_path = user_path + image_path 
		elif os.path.exists(global_path + image_path): 
			icon_path = global_path + image_path 
		return {'MenuText': 'RafterCalculator', 
			'ToolTip': 'Tooltip for RafterCalculator command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'RafterCalculator command is NOT active' 
			return False 
		else: 
			#print 'RafterCalculator command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'RafterCalculatorCommand activated' 
 
		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','RafterCalculator') 
		newsampleobject = RafterCalculator(b) 
		b.ViewObject.Proxy=0 
		FreeCAD.ActiveDocument.recompute()  

class RafterCalculator: 
 
 
	def __init__(self, obj): 
 
		#print 'The RafterCalculator class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 

		geometryList.append( Part.LineSegment( App.Vector (-1346.2, 131.7625, 0.0), App.Vector (0.0, 1258.8136627906977, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1346.2, 0.0, 0.0), App.Vector (-1206.8247342132063, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 1258.8136627906977, 0.0), App.Vector (0.0, 1010.364893759911, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1092.2, 95.96489375989356, 0.0), App.Vector (-1092.2, 186.34163794595736, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1092.2, 186.34163794595736, 0.0), App.Vector (-984.25, 186.34163794595736, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-984.25, 186.34163794595736, 0.0), App.Vector (-1.1368683772161603e-13, 1010.3648937599108, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1092.2, 95.96489375989356, 0.0), App.Vector (-1206.8247342132063, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1346.2, 0.0, 0.0), App.Vector (-1346.2, 131.7625, 0.0)))

		constructionList.append( Part.LineSegment( App.Vector (0.0, 1010.364893759911, 0.0), App.Vector (-122.28893305553511, 1156.4322304651334, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1206.8247342132063, 0.0, 0.0), App.Vector (-1329.1136672687499, 146.0673367052327, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1092.2, 186.34163794595736, 0.0), App.Vector (0.0, 1100.7416379459576, 0.0)))



		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )
#		for constraint in constraintList:
#			print constraint
#			obj.addConstraint( constraint )

		#View properties
#TODO: Initiate Per Sketch

#		obj.ViewObject.LineWidth = 2.00
#		obj.ViewObject.LineColor = (0.33,0.67,1.00)
#		obj.ViewObject.DrawStyle = u"Dashed" 

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print ' RafterCalculator Class executed()'
FreeCADGui.addCommand('RafterCalculator',RafterCalculator_Command() ) 
