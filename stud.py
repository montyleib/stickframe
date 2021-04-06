import FreeCAD,FreeCADGui,Part, Draft
import os, math
import framing

__title__="FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"

__command_name__ = "Stud"
__command_group__ = "Members"

def makeStud(name):
	newstud = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name )
	Stud(newstud)
	ViewProviderStud(newstud.ViewObject)
#	newstud.Placement = FreeCAD.Placement( FreeCAD.Vector (38.1, 88.89, 0.0),FreeCAD.Rotation (0.0, 0.0, 0, 0) )  
	FreeCAD.ActiveDocument.recompute()
	return newstud

class Stud_Command:
	"""
	The Stud_Command class integrates the stud object into the FreeCAD Workbench, StickFrame
	It is pre-positioned to sit at the end of a stud plate.
	"""
	def GetResources(self):

		icon_path = framing.getIconImage( "stud" ) 	
	
		return {"MenuText": "Stud",
			"ToolTip": "Add a Stud to the Construction",
			'Pixmap': str(icon_path)}

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		newstud = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Stud")
		Stud(newstud)

		framing.defaultAttachment( newstud )

		# if framing.isItemSelected():
		# 	selection = FreeCADGui.Selection.getSelectionEx()
		# 	obj = selection[0].SubElementNames
		# 	edge_name = obj[0]

		# 	#One Edge
		# 	edge_obj = FreeCADGui.Selection.getSelection()[0]
		# 	edge_shp = FreeCADGui.Selection.getSelection()[0].Shape
		# 	edge_elt = FreeCADGui.Selection.getSelection ()[0].Shape.Edge1

		# 	if isinstance( edge_shp, Part.Wire ):	
		# 		#FreeCAD.ActiveDocument.getObject(newstud.Name).Length = edge_elt.Length
		# 		FreeCAD.ActiveDocument.getObject(newstud.Name).Support = [(edge_obj,'Vertex1'),(edge_obj,edge_name)]
		# 		FreeCAD.ActiveDocument.getObject(newstud.Name).MapMode = 'OXY'

		# 	if 	isinstance( edge_shp, Part.Compound ):
		# 		#FreeCAD.ActiveDocument.getObject(newplate.Name).Length = edge_elt.Length	
		# 		FreeCAD.ActiveDocument.getObject(newstud.Name).Support = [(edge_obj,'Vertex1'),(edge_obj,edge_name)]
		# 		FreeCAD.ActiveDocument.getObject(newstud.Name).MapMode = 'OXY'

#		newstud.Placement = FreeCAD.Placement( FreeCAD.Vector (38.1, 88.89, 0.0),FreeCAD.Rotation (0.0, 0.0, 0, 1) )
		newstud.Placement = FreeCAD.Placement( FreeCAD.Vector (0,0,0),FreeCAD.Rotation (0.0,0.0, 1, 0) )  

		ViewProviderStud(newstud.ViewObject)
		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.SendMsgToActiveView("ViewFit")	
		FreeCADGui.activeDocument().activeView().viewIsometric()

class Stud():
	"""
	The Stud Class defines the graphical representation of the object and the underlying Shape.
	"""
	Placement = FreeCAD.Placement

	def __init__(self, obj):

		precuts = ['92.25 in', '92.625 in', '93 in','96 in', '104.625 in', '116.625 in']
		centers = ['15.25 in', '16 in', '18 in', '24 in']

		obj.addProperty("App::PropertyLength","Length","Lumber Dimension","The board foot length ( cut length ) dimension").Length = "92.625 in"
		obj.addProperty("App::PropertyLength","Width","Lumber Dimension","Lumber Edge Dimension").Width="1.5 in"		
		obj.addProperty("App::PropertyLength","Height","Lumber Dimension", "Lumber Face Dimension").Height="3.5 in"
		obj.addProperty("App::PropertyLength","Centers","Construction Dimensison", "Lumber Face Dimension").Centers="16 in"

		obj.addProperty("App::PropertyFloat", "Cost", "Member","Enter the cost of the construction member").Cost = 2.99
		obj.addProperty("App::PropertyEnumeration", "Function", "Member", "Where this member is being used").Function = ['Corner', 'Wall', 'Nailer', 'King Stud', 'Jack Stud', 'Cripple Stud']
		obj.addProperty("App::PropertyString", "MemberName", "Member","Where this member is being used").MemberName = "Stud"
		obj.Proxy = self

		obj.addExtension('Part::AttachExtensionPython' )

	def onChanged(self, fp, prop):
		if prop == "Length" or prop == "Width" or prop == "Height" and prop > 0:
			FreeCAD.ActiveDocument.recompute()
		if prop == "Function":
			if fp.Function == "Corner":
				pass
			if fp.Function == "Nailer":
				pass

	def execute(self,fp):
		fp.Shape = Part.makeBox(fp.Length,fp.Height,fp.Width, FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0 ) )
		fp.positionBySupport()


class ViewProviderStud:
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
		pass

	def getIcon(self):
		''' Return the icon in XMP format which will appear in the tree view. This method is optional
		and if not defined a default icon is shown.
		'''
		return """
			/* XPM */
			static char * stud_icon_xpm[] = {
			"64 64 4 1",
			" 	c #FFFFFF",
			".	c #000000",
			"+	c #E1B313",
			"@	c #363636",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                                                                ",
			"                               ........                         ",
			"                              .++++++..                         ",
			"                            ..++++++.+.                         ",
			"                           .+++++++.++.                         ",
			"                          .++++++..+++.                         ",
			"                        ..++++++.+++++.                         ",
			"                       .......@.++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.+++++++.                         ",
			"                       .++++++.++++++.                          ",
			"                       .++++++.+++++.                           ",
			"                       .++++++.++++.                            ",
			"                       .++++++.+++.                             ",
			"                       .++++++.++.                              ",
			"                       .++++++.+.                               ",
			"                       .++++++..                                ",
			"                       ........                                 ",
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

FreeCADGui.addCommand('Stud', Stud_Command())

