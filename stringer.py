import FreeCAD, FreeCADGui, Part, Draft
import os
import math
import framing

import stringer_sketch

__title__ = "FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"

def makeStringer(name):
	newstringer = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name)
	Stringer(newstringer)
	ViewProviderCollarBeam(newstringer.ViewObject)
#Two Story Placement	
#	newcollar.Placement = FreeCAD.Placement( FreeCAD.Vector (2e-14, 88.89999999999887, 5064.135),FreeCAD.Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )

#Single Story Placement
# Debugging JSON Serialize error
#	newstringer.Placement = FreeCAD.Placement( FreeCAD.Vector (2e-14, 88.89999999999887, 2430.465),FreeCAD.Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )
	FreeCAD.ActiveDocument.recompute()
	return newstringer


class Stringer_Command:

	"""
	The Stringer is a single pre-cut stair stringer.
	"""

	def GetResources(self):

#		image_path = "/" + framing.mod_name + '/icons/stringer.png'
		image_path = '/stickframe/icons/stringer.png'
		global_path = FreeCAD.getHomePath()+"Mod"
		user_path = FreeCAD.getUserAppDataDir()+"Mod"
		icon_path = ""

		if os.path.exists(user_path + image_path):
			icon_path = user_path + image_path
		elif os.path.exists(global_path + image_path):
			icon_path = global_path + image_path
		return {"MenuText": "Stringer",
				"ToolTip": "Add a Stringer to the Construction",
				'Pixmap': str(icon_path)}

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):

		newstringer = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "Stringer")

		ViewProviderStringer(newstringer.ViewObject)	
		Stringer(newstringer)

		newstringer.Visibility = True
		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.SendMsgToActiveView("ViewFit")	


class Stringer():

	def __init__(self, obj):
		obj.addProperty("App::PropertyLength", "Rise", "Dimension","Change the total Rise of the Stringer").Rise = 177.8
		obj.addProperty("App::PropertyLength", "Run", "Dimension","Change the total Rin of the Sringer").Run=279.4
		obj.addProperty("App::PropertyLength", "Landing", "Dimension","Pre-Set Landing ( NOT IMPLEMENTED )").Landing = "4 ft"
		obj.setEditorMode("Landing", 1)


		obj.addProperty("App::PropertyFloat", "Cost", "Member","Enter the cost of the construction member").Cost = 2.99
		obj.addProperty("App::PropertyEnumeration", "Function", "Member", "Where this member is being used").Function = ['1st Level Stairs','2nd Level Stairs','Attic Stairs','Basement Stairs']
		obj.addProperty("App::PropertyString", "MemberName", "Member","Where this member is being used").MemberName = "Stringer"
		obj.Proxy = self

#		obj.addExtension('Part::AttachExtensionPython', obj)

		#TODO:Use part to extrude the sketch	
		#		"PartDesign::Body','Body'
		#		"PartDesign::Pad","Pad"

		sketch = stringer_sketch.makeStringerSketch( "StringerSketch" )
		sketch.Visibility = False
#		sketch.ShowInTree = False

		newextrusion = FreeCAD.ActiveDocument.addObject('Part::Extrusion', 'StringerExtrusion')
#		extrusion = obj

		newextrusion.Base = FreeCAD.ActiveDocument.getObject(sketch.Name)
		newextrusion.Dir = ( 0,1,0 )
		newextrusion.LengthFwd = '1.5 in'
		newextrusion.Solid = True

		obj.addObject( sketch )
		obj.addObject( newextrusion )


	def onChanged(self, fp, prop):
		if prop == "Length" or prop == "Width" or prop == "Height":
			fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height)

		if prop == "Rise":
			fp.Group[0].setDatum(66, fp.Rise )
			FreeCAD.ActiveDocument.recompute()
		if prop == "Run":
			fp.Group[0].setDatum(67, fp.Run )
			FreeCAD.ActiveDocument.recompute()



	def execute(self, fp):
		

		fp.recompute()
#		print ("Stringer execute(d)")


class ViewProviderStringer:
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
			static char * stairstringer_xpm[] = {
			"128 128 15 1",
			" 	c None",
			".	c #000000",
			"+	c #FFAE4C",
			"@	c #FFC054",
			"#	c #FF9933",
			"$	c #FFCC66",
			"%	c #FFCC99",
			"&	c #FFCC33",
			"*	c #FFFF66",
			"=	c #FFFF99",
			"-	c #777777",
			";	c #663300",
			">	c #CC6633",
			",	c #FF6600",
			"'	c #FF9900",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"     .                  .                                                                                                       ",
			"    ......................                                                                                                      ",
			"    ......................                                                                                                      ",
			"    .. +@@#$$+$$%&$$$$+@..                                                                                                      ",
			"    .. +@@#$$+$$%&$$$$+@..                                                                                                      ",
			"    .. +@@#$$+$$%&$$$$+@..                                                                                                      ",
			"    .. +@@#$$+$$%&$$$$+@..                                                                                                      ",
			"    .. +@@#$$+$$%&$$$+@@..                                                                                                      ",
			"    .. +@@#$$+$$%&$$$+@@..                                                                                                      ",
			"    .. @@@#$$+$$%&$$$+@@..                                                                                                      ",
			"    .. @@@#$$+$$%&$$$+@@..                                                                                                      ",
			"    .. @@@#$$+$$%&$$$+@@..                                                                                                      ",
			"    .. @@@#$$+$$%&$$$+@@..                                                                                                      ",
			"    ...@@@#$$+$$%&$$$+@@......................                                                                                  ",
			"    .... @#$$+$$%&$$$+@@......................                                                                                  ",
			"      ....#$$+$$%&$$$+@@+ $$+$$$+$$@@$@@$$+ ..                                                                                  ",
			"       .... $+$$%&$$$+@@+$$$+$$$+$$@@@@@$$+ ..                                                                                  ",
			"         .... $$%&$$$+@@+$$$+$$$$+$$@@@@$$+ ..                                                                                  ",
			"           ... $%&$$$+@@+$$$+$$$$+$$@@$@$$+ ..                                                                                  ",
			"            .... &$$$+@@+$$$+$$$$+$$@@@@$$+ ..                                                                                  ",
			"              ....$$$+@@+$$$+$$$$+$$@@@$$$+ ..                                                                                  ",
			"               .... $+@@+$$$+$%$$+$$@@@$$$+ ..                                                                                  ",
			"                 ....+@@+$$$+$%$$+$$$@@$$$+ ..                                                                                  ",
			"                  .... @+$$$+$%$$+$$$@@$$$+ ..                                                                                  ",
			"                    .... $$$+$%$$+$$$@@$$$+ ..                                                                                  ",
			"                      ... $$+$%$$+$$$@@$$$+ ..                 ..                                                               ",
			"                       .... +$%$$+$$$@@$$$+ ......................                                                              ",
			"                         ....$%$$+$$$@@$$$+$.....................                                                               ",
			"                          .... $$+$$$@@$$$+$$&@@$$$+@@@+%$@$*=#..                                                               ",
			"                            ....$+$$$@@$$$+$$&@@$$$+@@@+%$@$*=#..                                                               ",
			"                             .... $$$@@$$$+$$&@@$$$+@@@+%$@$*=#..                                                               ",
			"                               .... $@@$$$+$$&@@$$$+@@@+%$@$*=#..                                                               ",
			"                                 ... @@$$$+$$&@@$$$+@@@+%$@$*=#..                                                               ",
			"                                  .... $$$+$$&@@$$$+@@@+%$@$*=#..                                                               ",
			"                                    ....$$+$$&@@$$$+@@@+%$@$*=#..                                                               ",
			"                                     .... +$$&@@$$$+@@@+%$@$*=#..                                                               ",
			"                                       ....$$&@@$$$+@@@+%$@$*=#..                                                               ",
			"                                        .... &@@%$$+@@@+%$@$*=#..                                                               ",
			"                                          .... @%$$+@@@+%$@$*=#......................                                           ",
			"                                            ... %$$+@@@+%$@$*=#......................                                           ",
			"                                             .... $+@@@+%$@$*=#-;>+$&$$+@@#$$+$$%&$..                                           ",
			"                                               ....+@@@+%$@$*=#-;>+$&$$+@@#$$+$$%&$..                                           ",
			"                                                .... @@+%$@$*=#-;>+$&$$+@@#$$+$$%&$..                                           ",
			"                                                  ....@+%$@$*=#-;>+$&$$+@@#$$+$$%&$..                                           ",
			"                                                   .... %$@$*=#-;>+$&$$+@@#$$+$$%&$..                                           ",
			"                                                     .... @$*=#-;>+$&$$+@@#$$+$$%&$..                                           ",
			"                                                       ... $*=#-;>+$&$$+@@#$$+$$%&$..                                           ",
			"                                                        .... =#-;>+$&$$+@@#$$+$$%&$..                                           ",
			"                                                          ....#-;>+$&$$+@@#$$+$$%&$..                                           ",
			"                                                           .... ;>+$&$$+@@#$$+$$%&$..                                           ",
			"                                                             ....>+$&$$+@@#$$+$$%&$..                  .                        ",
			"                                                              .... $&$$+@@#$$+$$%&$......................                       ",
			"                                                                .... $$+@@#$$+$$%&$......................                       ",
			"                                                                  ... $+@@#$$+$$%&$$$$+@+$$$+$+$#$##,# ..                       ",
			"                                                                   .... @@#$$+$$%&$$$$+@+$$$+$+$#$',## ..                       ",
			"                                                                     ....@#$$+$$%&$$$$+@+$$+$$+$#$#+#$ ..                       ",
			"                                                                      .... $$+$$%&$$$$+@+$$+$$+$#$#+#$ ..                       ",
			"                                                                        ....$+$$%&$$$$+@@+$+$$+$#$#+'$ ..                       ",
			"                                                                         .... $$%&$$$$+@@+$+$$+$#$#+#$ ..                       ",
			"                                                                           .... %&$$$$+@@+$+$$+$#$#+'$ ..                       ",
			"                                                                             ... &$$$$+@@+$+$$+$#$###$ ..                       ",
			"                                                                              .... $$$+@@+$+$$+$$#$#$$ ..                       ",
			"                                                                                ....$$+@@+$+$$+$$#$$$$ ..                       ",
			"                                                                                 .... @@@+$+$$+$$$#$$$......................    ",
			"                                                                                   ....@@+$+$$+$$$#$$$ .....................    ",
			"                                                                                    .... $$+$$+$$$$###$$@@$+$&@@%$$+@@@+%$..    ",
			"                                                                                      .... +$$+$$&$$$$$&@@$+$&@@%$$+@@@+%$..    ",
			"                                                                                        ... $$+$$&&$$$$&@@$+$&@@%$$+@@@+%$..    ",
			"                                                                                         .... +$$$&$$$$&@@$+$&@@%$$+@@@+%$..    ",
			"                                                                                           ....+$$$@$$&@@$$+$&@@$$$+@@@+%$..    ",
			"                                                                                            .... $$@&$&@@$+$$&@@$$$+@@@+%$..    ",
			"                                                                                              ....$@@$@@$$+$$&@@$$$+@@@+%$..    ",
			"                                                                                               .... @@@@$$+$$&@@$$$+@@@+%$..    ",
			"                                                                                                 .... @@$$+$$&@@$$$+@@@+%$..    ",
			"                                                                                                   ... @$$+$$&@@$$$+@@@+%$..    ",
			"                                                                                                    ........................    ",
			"                                                                                                      ......................    ",
			"                                                                                                       ..                 ..    ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                ",
			"                                                                                                                                "};
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


FreeCADGui.addCommand('Stringer', Stringer_Command())
