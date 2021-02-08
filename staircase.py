import FreeCAD,FreeCADGui,Part, Draft, Sketcher
import os, math
import framing

__title__="FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"
__command_name__ = "FloorPanel"
__command_group__ = "Constructions"

floor_levels = ['None','Basement','1st Floor','Second Floor', 'Third Floor', 'Attic' ]

class StairCase_Command:

	def GetResources(self):

#		image_path = "/" + framing.mod_name + '/icons/staircase.png'
		image_path = '/stickframe/icons/staircase.png'
		global_path = FreeCAD.getHomePath()+"Mod"
		user_path = FreeCAD.getUserAppDataDir()+"Mod"
		icon_path = ""

		if os.path.exists(user_path + image_path):
			icon_path = user_path + image_path
		elif os.path.exists(global_path + image_path):
			icon_path = global_path + image_path
		return {"MenuText": "StairCase",
                    "ToolTip": "Add a Stair Case to the Construction",
                    'Pixmap': str(icon_path)}

	def IsActive(self):
		if FreeCAD.ActiveDocument is None:
			return False
		else:
			return True

	def Activated(self):

		grpobj = FreeCAD.activeDocument().addObject('App::DocumentObjectGroupPython', 'Staircase')

		#create each componant of the staircase

		#TODO: Determine number of steps and loop through adding a full compliment of these.
		mystringer=FreeCAD.ActiveDocument.addObject("Sketcher::SketchObjectPython","Stringer_Sketch")
		mytread=FreeCAD.ActiveDocument.addObject("Sketcher::SketchObjectPython","Tread_Sketch")
		myriser=FreeCAD.ActiveDocument.addObject("Sketcher::SketchObjectPython","Riser_Sketch")
		mybottomriser=FreeCAD.ActiveDocument.addObject("Sketcher::SketchObjectPython","BottomRiser_Sketch")

		#add each to group
		grpobj.addObject ( mystringer )
		grpobj.addObject ( mytread )
		grpobj.addObject ( myriser )
		grpobj.addObject ( mybottomriser )

		mystringer.ViewObject.Proxy=0
		mytread.ViewObject.Proxy=0
		myriser.ViewObject.Proxy=0
		mybottomriser.ViewObject.Proxy=0

		newstringer = Stringer(mystringer)		
		newtread = Tread(mytread)		
		newriser = Riser(myriser)		
		newbottomriser = BottomRiser(mybottomriser)
		
		extruded_stringer = FreeCAD.ActiveDocument.getObject( "Stringer" )
		grpobj.addObject (extruded_stringer )

		FreeCAD.ActiveDocument.recompute() 

		#cloned_stringer = Draft.clone( extruded_stringer )
		#grpobj.addObject (cloned_stringer )

		extruded_tread = FreeCAD.ActiveDocument.getObject( "Tread" )
		grpobj.addObject (extruded_tread )

		extruded_riser = FreeCAD.ActiveDocument.getObject( "Riser" )
		grpobj.addObject (extruded_riser )

		extruded_bottomriser = FreeCAD.ActiveDocument.getObject( "BottomRiser" )
		grpobj.addObject (extruded_bottomriser )

		StairCase(grpobj)
		ViewProviderStairCase(grpobj.ViewObject)

		FreeCAD.ActiveDocument.recompute() 
		FreeCADGui.SendMsgToActiveView("ViewFit")	

class StairCase:

	def __init__(self, obj):

		obj.addProperty("App::PropertyEnumeration","Level","Level","The Length dimension").Level = floor_levels
		obj.addProperty("App::PropertyFloat","Rise","Level","The overall Rise of the Staircase").Rise = 1000
		obj.addProperty("App::PropertyFloat","Run","Level","The overall Run of the Staircase").Run = 1000
		obj.Proxy = self

#		print ("StairCase init")

	def onChanged(self, fp, prop):
		''' Do something here '''

	def execute(self,fp):

		fp.recompute()
#		print ("Staircase executed()")

class Stringer:

	def __init__(self, obj):

		sketch = obj
		sketch.Visibility = False
		
		App = FreeCAD
		geometryList = []
		constructionList = []
		constraintList = []

		geometryList.append(Part.LineSegment(App.Vector(-3861.083025058167, 1801.8531072129163,0.0), App.Vector(-3378.447646925896, 1801.8531072129163, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-3378.447646925896, 1801.8531072129163, 0.0), App.Vector(-3378.447646925896, 1576.6214688113018, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-3861.083025058167, 1801.8531072129163, 0.0), App.Vector(-3861.083025058167, 1576.6214688113018, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-482.6353781322709, 1.2245759961615477e-13,0.0), App.Vector(-1.7053025658242404e-13, 1.2245759961615477e-13, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-1.425526363618701e-13, 1.2245759961615477e-13,0.0), App.Vector(-1.425526363618701e-13, 225.23163840161453, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-1.425526363618701e-13, 225.23163840161453, 0.0), App.Vector(-482.6353781322709, 225.23163840161453, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-3861.083025058167, 1576.6214688113018,0.0), App.Vector(-482.635378132271, 2.2082335959794364e-13, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-3378.447646925896, 1576.6214688113018,0.0), App.Vector(-2895.812268793625, 1576.6214688113018, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-2895.812268793625, 1576.6214688113018, 0.0), App.Vector(-2895.812268793625, 1351.3898304096872, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-2895.812268793625, 1351.3898304096872,0.0), App.Vector(-2413.1768906613543, 1351.3898304096872, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-2413.1768906613543, 1351.3898304096872,0.0), App.Vector(-2413.1768906613543, 1126.1581920080728, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-2413.1768906613543, 1126.1581920080728,0.0), App.Vector(-1930.5415125290835, 1126.1581920080728, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-1930.5415125290835, 1126.1581920080728,0.0), App.Vector(-1930.5415125290835, 900.9265536064581, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-1930.5415125290835, 900.9265536064581,0.0), App.Vector(-1447.9061343968126, 900.9265536064581, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-1447.9061343968126, 900.9265536064581,0.0), App.Vector(-1447.9061343968126, 675.6949152048436, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-1447.9061343968126, 675.6949152048436,0.0), App.Vector(-965.2707562645418, 675.6949152048436, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-965.2707562645418, 675.6949152048436,0.0), App.Vector(-965.2707562645418, 450.46327680322906, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-965.2707562645418, 450.46327680322906,0.0), App.Vector(-482.6353781322709, 450.46327680322906, 0.0)))
		geometryList.append(Part.LineSegment(App.Vector(-482.6353781322709, 450.46327680322906,0.0), App.Vector(-482.6353781322709, 225.23163840161453, 0.0)))
		constructionList.append(Part.LineSegment(App.Vector(-3833.790527, 2014.348145, 0.0), App.Vector(99.58325783493278, 178.75908098916287, 0.0)))
		constructionList.append(Part.LineSegment(App.Vector(-3861.083025058167, 1801.8531072129163,0.0), App.Vector(-1.425526363618701e-13, 1.2245759961615477e-13, 0.0)))
		constructionList.append(Part.LineSegment(App.Vector(-4188.939453, 2125.139648, 0.0), App.Vector(-4643.51709, 1587.911621, 0.0)))
		constructionList.append(Part.LineSegment(App.Vector(340.306061, 149.793411, 0.0), App.Vector(-155.59672500000002, -337.84439100000003, 0.0)))

		constraintList.append(Sketcher.Constraint('Vertical',2 ) )
		constraintList.append(Sketcher.Constraint('Vertical',1 ) )
		constraintList.append(Sketcher.Constraint('Vertical',8 ) )
		constraintList.append(Sketcher.Constraint('Vertical',10 ) )
		constraintList.append(Sketcher.Constraint('Vertical',12 ) )
		constraintList.append(Sketcher.Constraint('Vertical',14 ) )
		constraintList.append(Sketcher.Constraint('Vertical',16 ) )
		constraintList.append(Sketcher.Constraint('Vertical',18 ) )
		constraintList.append(Sketcher.Constraint('Vertical',4 ) )

		constraintList.append( Sketcher.Constraint('Horizontal',0 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',7 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',9 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',11 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',13 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',15 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',17 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',5 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',3 ) )

		constraintList.append( Sketcher.Constraint('Equal',2,1))
		constraintList.append( Sketcher.Constraint('Equal',1,8))
		constraintList.append( Sketcher.Constraint('Equal',8,10))
		constraintList.append( Sketcher.Constraint('Equal',10,12))
		constraintList.append( Sketcher.Constraint('Equal',12,14))
		constraintList.append( Sketcher.Constraint('Equal',14,16))
		constraintList.append( Sketcher.Constraint('Equal',16,18))
		constraintList.append( Sketcher.Constraint('Equal',18,4))
		constraintList.append( Sketcher.Constraint('Equal',0,7))
		constraintList.append( Sketcher.Constraint('Equal',7,9))
		constraintList.append( Sketcher.Constraint('Equal',9,11))
		constraintList.append( Sketcher.Constraint('Equal',11,13))
		constraintList.append( Sketcher.Constraint('Equal',13,15))
		constraintList.append( Sketcher.Constraint('Equal',15,17))
		constraintList.append( Sketcher.Constraint('Equal',17,5))
		constraintList.append( Sketcher.Constraint('Equal',5,3))

		constraintList.append( Sketcher.Constraint('Coincident',0,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,2,8,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,1,1,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',9,1,8,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',10,1,9,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',11,1,10,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',12,1,11,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',13,1,12,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',13,2,14,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',15,1,14,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',16,1,15,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',16,2,17,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',18,1,17,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,2,18,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,2,5,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,4,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,1,6,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,1,2,2 ) )

		#Lock to origin
		constraintList.append( Sketcher.Constraint('Coincident',3,2,-1,1 ) )

		#lock to construction lines
		constraintList.append( Sketcher.Constraint('PointOnObject',0,2,19 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,2,19 ) )
		constraintList.append( Sketcher.Constraint('Coincident',20,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',20,2,3,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',21,1,19,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',22,1,19,2 ) )

		constraintList.append( Sketcher.Constraint('Perpendicular',20,0,21 ) )
		constraintList.append( Sketcher.Constraint('Perpendicular',22,0,20 ) )

		constraintList.append( Sketcher.Constraint('PointOnObject',3,2,22 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',0,1,21 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',21,2,6 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',22,2,6 ) )

		#set tread Rise and run
		constraintList.append( Sketcher.Constraint('DistanceY',1,2,1,1,177.8))
		constraintList.append( Sketcher.Constraint('DistanceX',0,1,0,2,279.4))

		objects = sketch.addGeometry( geometryList, False)
		constructions = sketch.addGeometry( constructionList, True)
		constraints = sketch.addConstraint( constraintList )

		sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))

		f = FreeCAD.ActiveDocument.addObject('Part::Extrusion', 'Stringer')
		f.Base = App.ActiveDocument.getObject('Stringer_Sketch')
		f.Dir = (0,1,0)
		f.LengthFwd = '1.5 in'
		f.Solid = True



class Tread:
	def __init__(self, obj):
		sketch = obj
		sketch.Visibility = False		

		App = FreeCAD
		geometryList = []
		constructionList = []
		constraintList = []

		geometryList.append( Part.LineSegment( App.Vector (12.69999999999982, 177.8, 0.0), App.Vector (279.4, 177.8, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (279.4, 177.8, 0.0), App.Vector (279.4, 203.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (279.4, 203.2, 0.0), App.Vector (12.69999999999989, 203.2, 0.0)))
		tmpCircle = Part.Circle ( App.Vector (12.699999999999982, 190.5, 0.0), App.Vector (0.0, 0.0, 1.0), 12.7)
		geometryList.append( Part.ArcOfCircle (  tmpCircle, 1.57079632679, 4.71238898038))
		constructionList.append( Part.LineSegment( App.Vector (0.0, 203.20000000000002, 0.0), App.Vector (0.0, 177.8, 0.0)))

		constraintList.append( Sketcher.Constraint('Horizontal',0 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )

		constraintList.append( Sketcher.Constraint('Vertical',1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',4 ) )
		constraintList.append( Sketcher.Constraint('Vertical',0,1,3,3 ) )
		constraintList.append( Sketcher.Constraint('Vertical',2,2,3,3 ) )

		constraintList.append( Sketcher.Constraint('Coincident',2,1,1,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',0,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,1,2,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,0,1 ) )

		constraintList.append( Sketcher.Constraint('Tangent',3,0,4,0 ) )

		constraintList.append( Sketcher.Constraint('DistanceY',-1,1,1,1,177.8))
		constraintList.append( Sketcher.Constraint('DistanceX',-1,1,1,2,279.4))
		constraintList.append( Sketcher.Constraint('DistanceY',1,1,1,2,25.4))

		constraintList.append( Sketcher.Constraint('Equal',4,1))
		#constraintList.append( Sketcher.Constraint('PointOnObject',4,2,-2 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',4,1,2,2 ) )

		constraintList.append( Sketcher.Constraint('DistanceX',-2,1,4,1,-38.1))

		objects = sketch.addGeometry( geometryList, False)
		constructions = sketch.addGeometry( constructionList, True)
		constraints = sketch.addConstraint( constraintList )

		#App.ActiveDocument.Sketch.renameConstraint(11, u'Rise')
		#App.ActiveDocument.Sketch.renameConstraint(12, u'Run')
		#App.ActiveDocument.Sketch.renameConstraint(13, u'TreadThickness')
		#App.ActiveDocument.Sketch.renameConstraint(16, u'TreadTongue')

		f = FreeCAD.ActiveDocument.addObject('Part::Extrusion', 'Tread')
		f.Base = App.ActiveDocument.getObject('Tread_Sketch')
		f.LengthFwd = '36 in'
		f.Solid = True

class Riser:
	def __init__(self, obj):
		sketch = obj
		sketch.Visibility = False
		
		App = FreeCAD
		geometryList = []
		constructionList = []
		constraintList = []

		geometryList.append( Part.LineSegment( App.Vector (260.35, 355.6, 0.0), App.Vector (279.4, 355.6, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (279.4, 355.6, 0.0), App.Vector (279.4, 203.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (279.4, 203.2, 0.0), App.Vector (260.35, 203.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (260.35, 203.2, 0.0), App.Vector (260.35, 355.6, 0.0)))

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
		constraintList.append( Sketcher.Constraint('DistanceX',-1,1,1,2,279.4))

		objects = sketch.addGeometry( geometryList, False)
		constructions = sketch.addGeometry( constructionList, True)
		constraints = sketch.addConstraint( constraintList )

		f = FreeCAD.ActiveDocument.addObject('Part::Extrusion', 'Riser')
		f.Base = App.ActiveDocument.getObject('Riser_Sketch')
		f.LengthFwd = '36 in'
		f.Solid = True
		    
class BottomRiser:
	def __init__(self, obj):
		sketch = obj
		sketch.Visibility = False		

		App = FreeCAD
		geometryList = []
		constructionList = []
		constraintList = []

		geometryList.append( Part.LineSegment( App.Vector (260.35, 355.6, 0.0), App.Vector (279.4, 355.6, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (279.4, 355.6, 0.0), App.Vector (279.4, 203.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (279.4, 203.2, 0.0), App.Vector (260.35, 203.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (260.35, 203.2, 0.0), App.Vector (260.35, 355.6, 0.0)))

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
		constraintList.append( Sketcher.Constraint('DistanceX',-1,1,1,2,279.4))

		objects = sketch.addGeometry( geometryList, False)
		constructions = sketch.addGeometry( constructionList, True)
		constraints = sketch.addConstraint( constraintList )

		f = FreeCAD.ActiveDocument.addObject('Part::Extrusion', 'BottomRiser')
		f.Base = App.ActiveDocument.getObject('BottomRiser_Sketch')
		f.LengthFwd = '36 in'
		f.Solid = True


    
class ViewProviderStairCase:
	def __init__(self, obj):
		''' Set this object to the proxy object of the actual view provider '''
		obj.Proxy = self

	def attach(self, obj):
		''' Setup the scene sub-graph of the view provider, this method is mandatory '''
		return

	def updateData(self, fp, prop):
		''' If a property of the handled feature has changed we have the chance to handle this here '''
		return

	def getDisplayModes(self,obj):
		''' Return a list of display modes. '''
		modes=[]
		return modes

	def getDefaultDisplayMode(self):
		''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
		return "Lines"

	def setDisplayMode(self,mode):
		''' Map the display mode defined in attach with those defined in getDisplayModes.
		Since they have the same names nothing needs to be done. This method is optional.
		'''
		return mode

	def onChanged(self, vp, prop):
		''' Print the name of the property that has changed '''
#		FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

	def getIcon(self):
		''' Return the icon in XMP format which will appear in the tree view. This method is optional
		and if not defined a default icon is shown.
		'''
		
		return """
			/* XPM */
			static char * staircase_xpm[] = {
			"64 64 4 1",
			" 	c None",
			".	c #000000",
			"+	c #E1B313",
			"@	c #090000",
			"                       ..+++++++@+++++++.+++++++++++++++++++++++",
			"                       ..++++++++@+++++++.++++++++++++++++++++++",
			"                       .+.+++++++@++++++++..++++++++++++++++++++",
			"                       .+.++++++++@+++++++++.+++++++++++++++++++",
			"                       .++.++++++++@+++++++++.++++++++++++++++++",
			"                       .++.+++++++++@++++++++...................",
			"                       .+++.++++++++@++++++++.+++++++++++++++++.",
			"                       .+++.+++++++++@+++++++.+++++++++++++++++.",
			"                       .++++.+++++++++@++++++.+++++++++++++++++.",
			"                       .++++.+++++++++@++++++.+++++++++++++++++.",
			"                       .+++++.+++++++++@+++++.+++++++++++++++++.",
			"            ...........@+++++.++++++++++@++++.+++++++++++++++++.",
			"            .++++++++++@++++++.+++++++++@++++.+++++++++++++++++.",
			"            ..++++++++++@+++++.++++++++++@+++.++++++++++++++++. ",
			"            ..++++++++++@++++++.++++++++++@++.+++++++++++++++.  ",
			"            ..+++++++++++@+++++.+++++++++++@+.++++++++++++++.   ",
			"            .+.++++++++++@++++++.++++++++++@+.+++++++++++++.    ",
			"            .+.+++++++++++@+++++............@.+++++++++++++.    ",
			"            .+.+++++++++++@+++++.+++++++++++++++++++++++++.     ",
			"            .++.+++++++++++@++++.++++++++++++++++++++++++.      ",
			"            .++.+++++++++++@++++.+++++++++++++++++++++++.       ",
			"            .++.++++++++++++@+++.++++++++++++++++++++++.        ",
			"............@++.++++++++++++@+++.+++++++++++++++++++++.         ",
			"++++++++++++@+++.++++++++++++@++.++++++++++++++++++++.          ",
			"+++++++++++++@++.++++++++++++@++.+++++++++++++++++++.           ",
			"+++++++++++++@++.+++++++++++++@+.+++++++++++++++++++.           ",
			"+++++++++++++@+++.++++++++++++@+.++++++++++++++++++.            ",
			"+++++++++++++@+++.+++++++++++++@.+++++++++++++++++.             ",
			"++++++++++++++@++.+++++++++++++@.++++++++++++++++.              ",
			"++++++++++++++@+++.+++++++++++++@+++++++++++++++.               ",
			"++++++++++++++@+++..............@++++++++++++++.                ",
			"++++++++++++++@+++.+++++++++++++++++++++++++++.                 ",
			"+++++++++++++++@++.++++++++++++++++++++++++++.                  ",
			"+++++++++++++++@++.+++++++++++++++++++++++++.                   ",
			"+++++++++++++++@++.+++++++++++++++++++++++++.                   ",
			"+++++++++++++++@++.++++++++++++++++++++++++.                    ",
			"++++++++++++++++@+.+++++++++++++++++++++++.                     ",
			"++++++++++++++++@+.++++++++++++++++++++++.                      ",
			"++++++++++++++++@+.+++++++++++++++++++++.                       ",
			"++++++++++++++++@+.++++++++++++++++++++.                        ",
			"+++++++++++++++++@.+++++++++++++++++++.                         ",
			"+++++++++++++++++@.++++++++++++++++++.                          ",
			"+++++++++++++++++@.++++++++++++++++++.                          ",
			"+++++++++++++++++@.+++++++++++++++++.                           ",
			"++++++++++++++++++@++++++++++++++++.                            ",
			"..................@+++++++++++++++.                             ",
			".++++++++++++++++++++++++++++++++.                              ",
			".+++++++++++++++++++++++++++++++.                               ",
			".++++++++++++++++++++++++++++++.                                ",
			".+++++++++++++++++++++++++++++.                                 ",
			".++++++++++++++++++++++++++++.                                  ",
			".++++++++++++++++++++++++++++.                                  ",
			".+++++++++++++++++++++++++++.                                   ",
			".++++++++++++++++++++++++++.                                    ",
			".+++++++++++++++++++++++++.                                     ",
			".++++++++++++++++++++++++.                                      ",
			".+++++++++++++++++++++++.                                       ",
			".++++++++++++++++++++++.                                        ",
			".+++++++++++++++++++++.                                         ",
			".+++++++++++++++++++++.                                         ",
			".++++++++++++++++++++.                                          ",
			".+++++++++++++++++++.                                           ",
			"..+++++++++++++++++.                                            ",
			"...................                                             "};
			"""

	def __getstate__(self):
		''' When saving the document this object gets stored using Python's cPickle module.
		Since we have some un-pickable here -- the Coin stuff -- we must define this method
		to return a tuple of all pickable objects or None.
		'''
		return None

	def __setstate__(self,state):
		''' When restoring the pickled object from document we have the chance to set some
		internals here. Since no data were pickled nothing needs to be done here.
		'''
		return None
        
FreeCADGui.addCommand('StairCase', StairCase_Command())

