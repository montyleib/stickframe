import FreeCAD,FreeCADGui,Part, Draft
import os, math
import framing

__title__="FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"

__command_name__ = "Plate"
__command_group__ = "Members"

def makePlate(name):
	newplate = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name )
	Plate(newplate)
	ViewProviderPlate(newplate.ViewObject)	

	FreeCAD.ActiveDocument.recompute()
	return newplate

class Plate_Command:
	"""
	The Plate_Command class integrates the plate object into the FreeCAD Workbench, StickFrame
	"""
	def GetResources(self):
		#icon_path = framing.getIconImage( "stud" ) 	

		#image_path = "/" + framing.mod_name + '/icons/plate.png'
		image_path = '/stickframe/icons/plate.png'
		global_path = FreeCAD.getHomePath()+"Mod"
		user_path = FreeCAD.getUserAppDataDir()+"Mod"
		icon_path = ""

		if os.path.exists(user_path + image_path):
			icon_path = user_path + image_path
		elif os.path.exists(global_path + image_path):
			icon_path = global_path + image_path
		return {"MenuText": "Plate",
			"ToolTip": "Add a Stud wall Plate to the Construction",
			'Pixmap': str(icon_path)}

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		newplate=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Plate")
		plateshape = Plate(newplate)
		ViewProviderPlate(newplate.ViewObject)

		if framing.isItemSelected():
			selection = FreeCADGui.Selection.getSelectionEx()
			obj = selection[0].SubElementNames
			edge_name = obj[0]

			#One Edge
			edge_obj = FreeCADGui.Selection.getSelection()[0]
			edge_shp = FreeCADGui.Selection.getSelection()[0].Shape
			

			edge_elt = FreeCADGui.Selection.getSelection ()[0].Shape.Edge1

			if 	isinstance( edge_shp, Part.Wire ):	
					FreeCAD.ActiveDocument.getObject(newplate.Name).Length = edge_elt.Length
					FreeCAD.ActiveDocument.getObject(newplate.Name).Support = [(edge_obj,'Vertex1'),(edge_obj,edge_name)]
					FreeCAD.ActiveDocument.getObject(newplate.Name).MapMode = 'OXY'

			if 	isinstance( edge_shp, Part.Compound ):
					FreeCAD.ActiveDocument.getObject(newplate.Name).Length = edge_elt.Length	
					
					vertex = ""
					edge = ""
			
					FreeCAD.ActiveDocument.getObject(newplate.Name).Support = [(edge_obj,'Vertex1'),(edge_obj,edge_name)]
					FreeCAD.ActiveDocument.getObject(newplate.Name).MapMode = 'OXY'
					


#		newplate.Placement = FreeCAD.Placement( FreeCAD.Vector (0.0, 88.9, 0.0),FreeCAD.Rotation (0.7071067811865475, 0.0, 0.0, 0.7071067811865476) )
		newplate.Placement = FreeCAD.Placement( FreeCAD.Vector (0.0, 0, 0.0),FreeCAD.Rotation (0.0, 0.0, 0.0, 0.0) )
		
		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.SendMsgToActiveView("ViewFit")	
		FreeCADGui.activeDocument().activeView().viewIsometric()	
		return newplate

class Plate:
	"""
	The Plate Class defines the graphical representation of a Wall Plate using the Shape class. It
	provides helper properties to aide in construction and generating a Cut Plan and Bill of Materials.
	"""

	def __init__(self, obj):


		#platelengths = ['8 ft','10 ft']
		#platelocations = ['Bottom','Top']

		obj.addProperty("App::PropertyLength","Length","Lumber Dimension","The board foot length ( cut length ) dimension").Length = "96 in"
		obj.addProperty("App::PropertyLength","Width","Lumber Dimension","Lumber Edge Dimension").Width="1.5 in"
		obj.setEditorMode("Width", 1)
		obj.addProperty("App::PropertyLength","Height","Lumber Dimension", "Lumber Face Dimension").Height="3.5 in"
		obj.setEditorMode("Height", 1)
		obj.addProperty("App::PropertyLength","Centers","Construction Dimensison", "Construction Dimension").Centers="16 in"
		obj.setEditorMode("Centers", 1)
		obj.addProperty("App::PropertyFloat","Cost","Member","Cost of the construction member").Cost = 2.99
		obj.addProperty("App::PropertyEnumeration","Function","Member","Where this member is being used").Function = ['Sill', 'Top', 'Top2']
		obj.addProperty("App::PropertyString","MemberName","Member","What is this piece generally called").MemberName = "Plate"
		obj.Proxy = self

		obj.addExtension('Part::AttachExtensionPython')

	def onChanged(self, fp, prop):
		if prop == "Length" or prop == "Width" or prop == "Height":
#			self.Placement.Base = self.Placement.Base.mulitply ( fp.Placement.Base )
#			fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height)	
			FreeCAD.ActiveDocument.recompute()
		if prop == "Function":
			if fp.Function == "Sill":
				#fp.Placement = FreeCAD.Placement( FreeCAD.Vector (0.0, 88.9, 0.0),FreeCAD.Rotation (0.7071067811865475, 0.0, 0.0, 0.7071067811865476) )
				fp.Placement = FreeCAD.Placement( FreeCAD.Vector (0.0, 88.9, 0.0),FreeCAD.Rotation (0.0, 0.0, 0.0, 0.0) )
			if fp.Function == "Top":
				fp.Placement = FreeCAD.Placement( FreeCAD.Vector (0.0, 5.33e-13, 2390.78 + 38.1),FreeCAD.Rotation (-0.7071067811865475, 0.0, 0.0, 0.7071067811865476) )
			if fp.Function == "Top2":
				fp.Placement = FreeCAD.Placement( FreeCAD.Vector (88.89, 1.6919798894838616e-14, 2428.88 + 38.1),FreeCAD.Rotation (0.7071067811865476, 0.0, 0.0, -0.7071067811865475) )
				fp.Length = 2258.81


	def execute(self,fp):
		fp.Shape = Part.makeBox(fp.Length,fp.Height,fp.Width, FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1) )
		fp.positionBySupport()
		fp.recompute()

class ViewProviderPlate:
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
			static char * plate_xpm[] = {
			"64 64 3 1",
			" 	c None",
			".	c #010100",
			"+	c #E1B313",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"        ......................................................  ",
			"       .++++++++++++++++++++++++++++++++++++++++++++++++++++..  ",
			"      .++++++++++++++++++++++++++++++++++++++++++++++++++++.+.  ",
			"     .++++++++++++++++++++++++++++++++++++++++++++++++++++.++.  ",
			"    .+++++++++++++++++++++++++++++++++++++++++++++++++++++.++.  ",
			"   .+++++++++++++++++++++++++++++++++++++++++++++++++++++.+++.  ",
			"  .+++++++++++++++++++++++++++++++++++++++++++++++++++++.++++.  ",
			" .......................................................+++++.  ",
			" .+++++++++++++++++++++++++++++++++++++++++++++++++++++.++++.   ",
			" .+++++++++++++++++++++++++++++++++++++++++++++++++++++.+++.    ",
			" .+++++++++++++++++++++++++++++++++++++++++++++++++++++.++.     ",
			" .+++++++++++++++++++++++++++++++++++++++++++++++++++++.++.     ",
			" .+++++++++++++++++++++++++++++++++++++++++++++++++++++.+.      ",
			" .+++++++++++++++++++++++++++++++++++++++++++++++++++++..       ",
			" .......................................................        ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                "};
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

FreeCADGui.addCommand('Plate', Plate_Command())
