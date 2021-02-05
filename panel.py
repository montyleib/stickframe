import FreeCAD, FreeCADGui
import Part, Draft
import os, math


__title__="FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"

__command_name__ = "Panel"
__command_group__ = "Members"

def makePanel( name ):
	newpanel = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name )
	Panel(newpanel)
	ViewProviderPanel(newpanel.ViewObject)	
	FreeCAD.ActiveDocument.recompute()
	

class Panel_Command:
	"""
	The Panel_Command class integrates the panel object into the FreeCAD Workbench, StickFrame
	"""
	def GetResources(self):

		image_path = '/framing/icons/panel.png'
		global_path = FreeCAD.getHomePath()+"Mod"
		user_path = FreeCAD.getUserAppDataDir()+"Mod"
		icon_path = ""

		if os.path.exists(user_path + image_path):
			icon_path = user_path + image_path
		elif os.path.exists(global_path + image_path):
			icon_path = global_path + image_path
		return {"MenuText": "Panel",
			"ToolTip": "Add a  Panel to the Construction",
			'Pixmap': str(icon_path)}

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		newobj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Panel")
		Panel(newobj)
		ViewProviderPanel(newobj.ViewObject)	

		newobj.Placement = FreeCAD.Placement( FreeCAD.Vector (2e-12, 88.9, -53.975),FreeCAD.Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )

		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.SendMsgToActiveView("ViewFit")
		FreeCADGui.activeDocument().activeView().viewIsometric()	
		return newobj

class Panel():
	"""
	The Panel Class defines the graphical representation of the object and its underlying shape.
	"""

	def __init__(self, obj):

		precuts = ['8 ft', '4 ft', '2 ft']

		obj.addProperty("App::PropertyLength", "Length", "Lumber Dimension","Change the length of the Panel").Length = "8ft"
		obj.addProperty("App::PropertyLength","Width","Lumber Dimension","Lumber Edge Dimension").Width="4ft"
#		obj.setEditorMode("Width", 1)
		obj.addProperty("App::PropertyLength","Height","Lumber Dimension", "Lumber Face Dimension").Height=".75 in"
#		obj.setEditorMode("Height", 1)
		obj.addProperty("App::PropertyFloat", "Cost", "Member","Enter the cost of the construction member").Cost = 19.99
		obj.addProperty("App::PropertyEnumeration", "Function", "Member", "Where this member is being used").Function = ['1st Level ', '2nd Level', '3rd Level','4th Level']
		obj.addProperty("App::PropertyString", "MemberName", "Member","Where this member is being used").MemberName = "Panel"
		obj.Proxy = self

#		obj.addExtension('Part::AttachExtensionPython', obj)

	def onChanged(self, fp, prop):
		if prop == "Length" or prop == "Width" or prop == "Height":
#			self.Placement.Base = self.Placement.Base.mulitply ( fp.Placement )			
#			fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height)
			FreeCAD.ActiveDocument.recompute()

	def execute(self, fp):
		fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height )
		fp.recompute()

class ViewProviderPanel:
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
#		image_path = '/framing/icons/panel_.png'
#		icon_string = open( user_path + image_path )
#		print ( icon_string )



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


FreeCADGui.addCommand('Panel', Panel_Command())
