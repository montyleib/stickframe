import FreeCAD,FreeCADGui,Part, Draft
import os
import math
import framing

__title__="FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"

__command_name__ = "FloorJoist"
__command_group__ = "Members"


def makeFloorJoist( name ):
	newjoist = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name )
	FloorJoist(newjoist)
	ViewProviderFloorJoist(newjoist.ViewObject)	
	newjoist.Placement = FreeCAD.Placement( FreeCAD.Vector (2e-12, 88.9, -206.37),FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5 ) )
	FreeCAD.ActiveDocument.recompute()
	return newjoist
	

class FloorJoist_Command:
	"""
	The floor joist is a pre-determined size lmber that has a relationship to the flooring of the construction. It
    is pre-positioned to be placed below a stud plate.
	"""
	def GetResources(self):

#		image_path = "/" + framing.mod_name + '/icons/floorjoist.png'
		image_path = '/stickframe/icons/floorjoist.png'
		global_path = FreeCAD.getHomePath()+"Mod"
		user_path = FreeCAD.getUserAppDataDir()+"Mod"
		icon_path = ""
		 
		if os.path.exists(user_path + image_path):
			icon_path = user_path + image_path
		elif os.path.exists(global_path + image_path):
			icon_path = global_path + image_path
		return {"MenuText": "Joist",
			"ToolTip": "Add a Floor Joist to the Construction",
			'Pixmap' : str(icon_path) } 

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):



		#newjoist = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "FloorJoist")
		newjoist = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "FloorJoist")

		ViewProviderFloorJoist(newjoist.ViewObject)
		FloorJoist(newjoist)
		newjoist.Placement = FreeCAD.Placement( FreeCAD.Vector (2e-12,88.9, -206.37),FreeCAD.Rotation (0.5, -0.5, 0.5, 0.5) )

		
		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.SendMsgToActiveView("ViewFit")

class FloorJoist():
	"""
	The FloorJoist Class defines the graphical representation of the framing member and its underlying shape.
	"""

	#Placement = FreeCAD.Placement()

	def __init__(self, obj):

#		self.Placement = obj.Placement

		obj.addProperty("App::PropertyLength","Length","Lumber Dimension","Change the length of the Joist").Length = "96 in"
		obj.addProperty("App::PropertyLength","Width","Lumber Dimension","Lumber Edge Dimension").Width="1.5 in"
		obj.addProperty("App::PropertyLength","Height","Lumber Dimension", "Lumber Face Dimension").Height="7.5 in"
		obj.addProperty("App::PropertyLength","Centers","Construction Dimensison", "Construction Dimension").Centers="16 in"
		obj.setEditorMode("Centers", 1)

		obj.addProperty("App::PropertyFloat","Cost","Member","Enter the cost of the construction member").Cost = 2.99
		obj.addProperty("App::PropertyEnumeration","Function","Member","Where this member is being used").Function = ['Floor Joist', 'Rim Joist']
		obj.addProperty("App::PropertyString","MemberName","Member","Where this member is being used").MemberName = "Joist"
		obj.Proxy = self

#		obj.addExtension('Part::AttachExtensionPython', obj)
		
	def onChanged(self, fp, prop):
		if prop == "Length" or prop == "Width" or prop == "Height":
			#self.Placement = self.Placement.multiply ( fp.Placement )			
			#fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height)
			FreeCAD.ActiveDocument.recompute()			
			pass

	def execute(self,fp):
		fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height, FreeCAD.Vector(0,0,38.10),FreeCAD.Vector(1,0,0 ) )
		fp.recompute()


class ViewProviderFloorJoist:
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
			static char * floorjoist_xpm[] = {
			"64 64 3 1",
			" 	c None",
			".	c #010100",
			"+	c #E1B313",
			"                           .                   .+++.            ",
			"                          .                   .+++.             ",
			"                         .                   .+++.              ",
			"                        .                   .+++.               ",
			"                       .                   .+++.                ",
			"                      .                   .+++.                 ",
			"                     .                   .+++.                  ",
			"                    .                   .+++.                   ",
			"                   .                   .+++.                    ",
			"                  .                   .+++.                     ",
			"                 .                   .+++.                      ",
			"                .                   .+++.                       ",
			"               .                   .+++.                        ",
			"              .                   .+++.                         ",
			"             .                   .+++.                          ",
			"            .                   .+++.                           ",
			"           .                   .+++.                           .",
			"          .                   .+++.                           . ",
			"         .                   .+++.                           .  ",
			"        .                   .+++.                           .   ",
			"       .                   .+++.                           .    ",
			"      .                   .+++.                           .    .",
			"     .                   .+++.                           .    . ",
			"    .                   .+++.                           .    .  ",
			"   .                   .+++.                           .    .   ",
			"  .....................................................    .    ",
			"  .                  .+++.                            .  ..     ",
			"  .                 .+++.                             . .       ",
			"  ......................................................        ",
			"                  .+++.+++++++++.   .                 .         ",
			"  .....          .....+++++++++.....             .....          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .             .   .          ",
			"  .   .          .+++.+++++++++.   .            ..   .          ",
			"  .   .          .+++.+++++++++.   .           . .   .          ",
			"  .   .          .+++.+++++++++.   .          .  .   .          ",
			"  .   .          .+++.+++++++++.   .         .   .   .         .",
			"  .   .          .+++.++++++++..   .        .    .   .        . ",
			"  .   .          .+++.+++++++. .   .       .     .   .       .  ",
			"  .   .          .+++.++++++.  .   .      .      .   .      .   ",
			"  .   .          .+++.+++++.   .   .     .       .   .     .    ",
			"  .   .          .+++.++++.    .   .    .        .   .    .     ",
			"  .   .          .+++.+++.     .   .   .         .   .   .      ",
			"  .   .          .+++.++.      .   .  .          .   .  .       ",
			"  .   .          .+++.+.       .   . .           .   . .        ",
			"  .   .          .+++..        .   ..            .   ..         ",
			"  .....          .....         .....             .....          ",
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

FreeCADGui.addCommand('Floor Joist', FloorJoist_Command())

