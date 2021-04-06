import FreeCAD
import FreeCADGui
import Part
import Draft
import os
import math
import framing


__title__="FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"

__command_name__ = "Studspacer"
__command_group__ = "Members"

def makeStudspacer(name):
	newstudspacer = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name )
	Studspacer(newstudspacer)
	ViewProviderStudspacer(newstudspacer.ViewObject)
	newstudspacer.Placement = FreeCAD.Placement( FreeCAD.Vector (38.099999999999994, 0.0, 457.19999999999993),FreeCAD.Rotation (0.0, 0.0, 0.0, 1.0) )	
	FreeCAD.ActiveDocument.recompute()
	return newstudspacer


class Studspacer_Command:
	"""
	The Studspacer_Command class integrates the studspacer object inot the FreeCAD Workbench, StickFrame
	"""
	def GetResources(self):
		icon_path = framing.getIconImage( "studspacer" ) 	


#		image_path = "/" + framing.mod_name + '/icons/studspacer.png'
		# image_path = '/stickframe/icons/studspacer.png'
		# global_path = FreeCAD.getHomePath()+"Mod"
		# user_path = FreeCAD.getUserAppDataDir()+"Mod"
		# icon_path = ""

		# if os.path.exists(user_path + image_path):
		# 	icon_path = user_path + image_path
		# elif os.path.exists(global_path + image_path):
		# 	icon_path = global_path + image_path
		return {"MenuText": "Studspacer",
				"ToolTip": "Add a Stud nailing spacer to the Construction",
				'Pixmap': str(icon_path)}

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		newstudspacer = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Studspacer")
		Studspacer(newstudspacer)
		ViewProviderStudspacer(newstudspacer.ViewObject)	
		newstudspacer.Placement = FreeCAD.Placement( FreeCAD.Vector (38.099999999999994, 0.0, 457.19999999999993),FreeCAD.Rotation (0.0, 0.0, 0.0, 1.0) )
		FreeCAD.ActiveDocument.recompute()


class Studspacer():
	"""
	The Studspacer Class defines the graphical representation of the object and its underlying shape.
	"""

	def __init__(self, obj):

#		self.Placement = FreeCAD.Placement()

#		print ("Class Variable :Initial placement: ", self.studspacer_placement )

		precuts = ['92.25 in', '92.625 in', '93 in','96 in', '104.625 in', '116 5/8 in']
		centers = ['15.25 in', '16 in', '18 in', '24 in']

		obj.addProperty("App::PropertyLength", "Length", "Lumber Dimension","The board foot length ( cut length ) dimension").Length = 300
		obj.addProperty("App::PropertyLength","Width","Lumber Dimension","Lumber Edge Dimension").Width=38.10
		obj.setEditorMode("Width", 1)
		obj.addProperty("App::PropertyLength","Height","Lumber Dimension", "Lumber Face Dimension").Height=88.90
		obj.setEditorMode("Height", 1)
		obj.addProperty("App::PropertyFloat", "Cost", "Member","Enter the cost of the construction member").Cost = 2.99
		obj.addProperty("App::PropertyEnumeration", "Function", "Member", "Where this member is being used").Function = ['Spacer']
		obj.addProperty("App::PropertyString", "MemberName", "Member","Where this member is being used").MemberName = "Studspacer"
		obj.Proxy = self

#		obj.addExtension('Part::AttachExtensionPython', obj)

	def onChanged(self, fp, prop):
		if prop == "Length" or prop == "Width" or prop == "Height":
#			self.Placement = self.Placement.multiply ( fp.Placement )			
#			fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height)
			FreeCAD.ActiveDocument.recompute()

#		print ("Class Variable :onChanged placement: ", self.studspacer_placement )
			pass

	def execute(self, fp):
		#Using the PNT arguement you can position the origin of the shape.
		#if the object has already been created, retrieve the current placement b4 re-creating
		#otherwise the fp ( featurepython ) object gets reset to 0,0,0 or whatever is in below commands

		fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height, FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,1,0 ) )

#		print ( "Object Placement:", fp.Placement )
#		fp.Placement = self.studspacer_placement
#		print ( "Object Placement:", fp.Placement )

		fp.recompute()
#		print ("Studspacer execute(d)")
		

class ViewProviderStudspacer:
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

#		user_path = FreeCAD.getUserAppDataDir()+"Mod"
#		image_path = '/stickframe/icons/studspacer.png'
#		icon_string = open( user_path + image_path )
#		print ( icon_string )

		return """
			/* XPM */
			static char * studspacer_xpm[] = {
			"35 147 17 1",
			" 	c None",
			".	c #000000",
			"+	c #575757",
			"@	c #F2F466",
			"#	c #CACACA",
			"$	c #C5C5C5",
			"%	c #8A8A8A",
			"&	c #9E9E9E",
			"*	c #101010",
			"=	c #333333",
			"-	c #A0A0A0",
			";	c #515151",
			">	c #E1B313",
			",	c #9D9D9D",
			"'	c #060606",
			")	c #111111",
			"!	c #8E8E8E",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@$.............$@@@@@@@+..",
			"..+@@@@@@@%.............%@@@@@@@+..",
			"..+@@@@@@@&..*=======*..&@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@-..;>>>>>>>;..-@@@@@@@+..",
			"..+@@@@@@@,..')))))))'..,@@@@@@@+..",
			"..+@@@@@@@!.............!@@@@@@@+..",
			"..+@@@@@@@#.............#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+..",
			"..+@@@@@@@#..         ..#@@@@@@@+.."};
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


FreeCADGui.addCommand('Studspacer', Studspacer_Command())

