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
	newstud.Placement = FreeCAD.Placement( FreeCAD.Vector (38.1, 88.89, 0.0),FreeCAD.Rotation (0.0, 0.0, 0.7071067811865476, -0.7071067811865476) )  
	FreeCAD.ActiveDocument.recompute()
	return newstud


class Stud_Command:
	"""
	The Stud_Command class integrates the stud object into the FreeCAD Workbench, StickFrame
	"""
	def GetResources(self):

#		image_path = "/" + framing.mod_name + '/icons/stud.png'
		image_path = '/stickframe/icons/stud.png'
		print( 'image path: ' + image_path )

		global_path = FreeCAD.getHomePath()+"Mod"
		user_path = FreeCAD.getUserAppDataDir()+"Mod"
		icon_path = ""

		if os.path.exists(user_path + image_path):
			icon_path = user_path + image_path
		elif os.path.exists(global_path + image_path):
			icon_path = global_path + image_path
		return {"MenuText": "Stud",
				"ToolTip": "Add a Stud to the Construction",
				'Pixmap': str(icon_path)}
#		print ("Stud GetResources")

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		newstud = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Stud")
		Stud(newstud)

		newstud.Placement = FreeCAD.Placement( FreeCAD.Vector (38.1, 88.89, 0.0),FreeCAD.Rotation (0.0, 0.0, 0.7071067811865476, -0.7071067811865476) ) 

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

		#This adds a placement to the Shape of the Object, however the Container ( Part::FeaturePython ) determines the positioning
		#self refers to this class and not the Feature Python class.

		#The __init__ is passed a FeaturePython object that has a placement.
#		self.Placement = obj.Placement

#		print ( "Placement from obj in Stud __init__: ", obj.Placement )
#		print ( "Placement from self in Stud __init__: ", self.Placement )

		precuts = ['92.25 in', '92.625 in', '93 in','96 in', '104.625 in', '116 5/8 in']
		centers = ['15.25 in', '16 in', '18 in', '24 in']

		obj.addProperty("App::PropertyLength","Length","Lumber Dimension","The board foot length ( cut length ) dimension").Length = "92.625 in"
		obj.addProperty("App::PropertyLength","Width","Lumber Dimension","Lumber Edge Dimension").Width="1.5 in"		
		obj.addProperty("App::PropertyLength","Height","Lumber Dimension", "Lumber Face Dimension").Height="3.5 in"
		obj.addProperty("App::PropertyLength","Centers","Construction Dimensison", "Lumber Face Dimension").Centers="16 in"

		obj.addProperty("App::PropertyFloat", "Cost", "Member","Enter the cost of the construction member").Cost = 2.99
		obj.addProperty("App::PropertyEnumeration", "Function", "Member", "Where this member is being used").Function = ['Corner', 'Wall', 'Nailer', 'King Stud', 'Jack Stud', 'Cripple Stud']
		obj.addProperty("App::PropertyString", "MemberName", "Member","Where this member is being used").MemberName = "Stud"
		obj.Proxy = self

#		obj.addExtension('Part::AttachExtensionPython', obj)


	def onChanged(self, fp, prop):
		# fp is the FeaturePython Object, changes to placement effect where and how the object appears
		# When properties such as length, width and height are changes in the Properties/Combo tabs
		# the onchanged is called.
		# Those changes trigger one onChanged for each property
		
		# onChanged is called by FreeCAD, not the custom code

		#fp.Placement is all Zero' in this call ... 
		#NOPE, fp.Placement gets ZERO'd BY this call ( it is actually getting zerod by execute() )

		# on changed need to use fp.Shape = Part.makeBox as Shape is immutable 
		# so BOTH onChanged and execute must maintain state		
		
		# Q.) If execute is being called anyway why do I need a makeBox here? 
		# A.) Execute does not get called until the item is "re-calculated", leaving the object visibly unchanged
		# 		Other factors are involved in this ..., it seems not completely true.


		if prop == "Length" or prop == "Width" or prop == "Height" and prop > 0:
#			fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height) # <-- This ZEROS fp.Placement
#			self.Placement.Base = self.Placement.Base + fp.Placement.Base # <-- Then THIS tries to apply it, so no effect.
#			oesn't seem like i need to do anything here ...
			
			#need to make sure the property is greater than zero
			
			FreeCAD.ActiveDocument.recompute()
			pass
		if prop == "Function":
			#print ( "Function Changed", prop )
			if fp.Function == "Corner":
				pass
			if fp.Function == "Nailer":
				pass


	def execute(self, fp):
		# Execute gets called EVERY time the propety changes , may not need the makeBox Call in onChanged
		# but it needs to maintain the state of the Placement, otherwise it is just zeroing everything
		
		# Makebox takes a direction vector not a rotation, The direction vector is assumed to be the direction of this
		# objects origin. So hopefully this never changes. NOPE, or yep  ... grrrr so confusing.

#		fp.positionBySupport()
		fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height, FreeCAD.Vector(0,0,38.10),FreeCAD.Vector(1,0,0 ) )


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

