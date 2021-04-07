import FreeCAD, FreeCADGui, Part, Draft
import os, math
import framing

__title__="FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"

__command_name__ = "Ridgebeam"
__command_group__ = "Members"

def makeRidgebeam(name):
	newridgebeam = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name )
	Ridgebeam(newridgebeam)
	ViewProviderRidgebeam(newridgebeam.ViewObject)	
	#newridgebeam.Placement = FreeCAD.Placement( FreeCAD.Vector (-2.76826374121, -1152.1267377466597, 3504.7299430953),FreeCAD.Rotation (0.5, 0.5, 0.5, 0.5) )
	#newridgebeam.Placement = FreeCAD.Placement( FreeCAD.Vector (0.0, -1149.3500000001998, 3343.2799999963),FreeCAD.Rotation (0.5, 0.5, 0.5, 0.5) )	

	FreeCAD.ActiveDocument.recompute()
	FreeCADGui.SendMsgToActiveView("ViewFit")
	return newridgebeam

class Ridgebeam_Command:
	"""
	The Ridgebeam_Command class integrates the ridgebeam object inot the FreeCAD Workbench, StickFrame
	"""
	def GetResources(self):
		icon_path = framing.getIconImage( "ridgebeam" ) 	


		return {"MenuText": "Ridgebeam",
				"ToolTip": "Add a Ridgebeam to the Construction",
				'Pixmap': str(icon_path)}

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		newridgebeam = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Ridgebeam")
		Ridgebeam(newridgebeam)
		framing.defaultAttachment( newridgebeam )

		ViewProviderRidgebeam(newridgebeam.ViewObject)	
		#newridgebeam.Placement = FreeCAD.Placement( FreeCAD.Vector (-2.76826374121, -1152.1267377466597, 3504.7299430953 + 76.2),FreeCAD.Rotation (0.5, 0.5, 0.5, 0.5) )
		newridgebeam.Placement = FreeCAD.Placement( FreeCAD.Vector (-2.76826374121, -1152.1267377466597, 3504.7299430953 + 76.2),FreeCAD.Rotation (0.0, 0.0, 0.0, 0.0) )
				
		FreeCAD.ActiveDocument.recompute()


class Ridgebeam():
	"""
	The Ridgebeam Class defines the graphical representation of the object and its underlying shape.
	"""
	Placement = FreeCAD.Placement

	def __init__(self, obj):

#		self.ridgebeam_placement = FreeCAD.Placement()
		
#		print ("Class Variable :Initial placement: ", self.ridgebeam_placement )

		precuts = ['92.25 in', '92.625 in', '93 in','96 in', '104.625 in', '116.625 in']
		centers = ['15.25 in', '16 in', '18 in', '24 in']

		obj.addProperty("App::PropertyLength", "Length", "Lumber Dimension","Change the length of the Ridgebeam").Length = 2352.68
		obj.addProperty("App::PropertyLength","Width","Lumber Dimension","Lumber Edge Dimension").Width=38.10
#		obj.setEditorMode("Width", 1)
		obj.addProperty("App::PropertyLength","Height","Lumber Dimension", "Lumber Face Dimension").Height=266.7
#		obj.setEditorMode("Height", 1)
		obj.addProperty("App::PropertyFloat", "Cost", "Member","Enter the cost of the construction member").Cost = 2.99
		obj.addProperty("App::PropertyEnumeration", "Function", "Member", "Where this member is being used").Function = ['Corner', 'Wall', 'Nailer', 'King Ridgebeam', 'Jack Ridgebeam']
		obj.addProperty("App::PropertyString", "MemberName", "Member","Where this member is being used").MemberName = "Ridgebeam"
		obj.Proxy = self

		obj.addExtension('Part::AttachExtensionPython')

	def onChanged(self, fp, prop):
		if prop == "Length" or prop == "Width" or prop == "Height" and prop > 0:
			FreeCAD.ActiveDocument.recompute()


	def execute(self, fp):
		fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height ,FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1 ) )
		fp.positionBySupport()
		

class ViewProviderRidgebeam:
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

		user_path = FreeCAD.getUserAppDataDir()+"Mod"
		image_path = '/stickframe/icons/ridgebeam.png'
		icon_string = open( user_path + image_path )
		print ( icon_string )

		return """
			/* XPM */
			static char * ridgebeam_icon_xpm[] = {
			"16 16 4 1",
			" 	c None",
			".	c #000000",
			"+	c #141010",
			"@	c #C39D55",
			"        ...++...",
			"       ..@@@@...",
			"      ..@@@@.@@+",
			"    ..@@@@..@@@+",
			"   ..@@@...@@@@.",
			"  ..@@@..@@@@@..",
			"..@@@...@@@@@.  ",
			".......@@@@@..  ",
			".@@@.@@@@@@..   ",
			".@@@.@@@@@..    ",
			".@@@.@@@@..     ",
			".@@@.@@@..      ",
			".@@@.@@..       ",
			".@@@.@..        ",
			".@@@...         ",
			"......          "};
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


FreeCADGui.addCommand('Ridgebeam', Ridgebeam_Command())
