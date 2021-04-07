import FreeCAD,FreeCADGui,Part, Draft
import os
import math
import framing

__title__="FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"

__command_name__ = "CeilingJoist"
__command_group__ = "Members"

def makeJoist(name):

	newjoist = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", name)
	CeilingJoist(newjoist)
	ViewProviderCeilingJoist(newjoist.ViewObject)

	#TODO: Get placement to Work with Group objects
	#TODO: Create a storage mechanisms for default placements, perhaps centralized.
	#TODO: 2nd, 3rd etc., Stories should be calculated as an offset so that the height of a Story is parametric.

	#Single Story Placement
	newjoist.Placement = FreeCAD.Placement( FreeCAD.Vector (50.79,88.89,2466.98),FreeCAD.Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )

	FreeCAD.ActiveDocument.recompute()
	return newjoist

class CeilingJoist_Command:
	"""
	The ceiling joist is a pre-determined size lumber that has a 
	relationship to Rafter angles, Wall Top Plates and other ceiling sub-components.
	"""

	def GetResources(self):
		icon_path = framing.getIconImage( "ceilingjoist" ) 	


#		image_path = "/" + framing.mod_name + '/icons/ceilingjoist.png'
		# image_path = '/stickframe/icons/ceilingjoist.png'
		# global_path = FreeCAD.getHomePath()+"Mod"
		# user_path = FreeCAD.getUserAppDataDir()+"Mod"
		# icon_path = ""
		 
		# if os.path.exists(user_path + image_path):
		# 	icon_path = user_path + image_path
		# elif os.path.exists(global_path + image_path):
		# 	icon_path = global_path + image_path
		return {"MenuText": "Joist",
			"ToolTip": "Add a Ceiling Joist to the Construction",
			'Pixmap' : str(icon_path) } 

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):

		newjoist = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "CeilingJoist")
		ViewProviderCeilingJoist(newjoist.ViewObject)
		CeilingJoist( newjoist )

		framing.defaultAttachment( newjoist )

		newjoist.Placement = FreeCAD.Placement( FreeCAD.Vector (50.79, 88.89, 2466.98),FreeCAD.Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )

		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.SendMsgToActiveView("ViewFit")	
		FreeCADGui.activeDocument().activeView().viewIsometric()

class CeilingJoist():

	def __init__(self, obj):

		obj.addProperty("App::PropertyPlacement","Placement","Base","Location of this Member")

		obj.addProperty("App::PropertyLength","Length","Lumber Dimension","The board foot length ( cut length ) dimension").Length = "96 in"
		obj.addProperty("App::PropertyLength","Width","Lumber Dimension","Change the board width of the Joist").Width = "1.5 in"
		obj.addProperty("App::PropertyLength","Height","Lumber Dimension","Change the board height of the Joist").Height = "7.5 in"

		obj.addProperty("App::PropertyLength","Centers","Construction Dimensions", "Distance between centers of this member.").Centers="16 in"
#		obj.addProperty("App::PropertyLength","Centers","Construction Dimensions", "Roof Slope determines cutoff angle").RoofSlope="7.5"
		obj.setEditorMode("Centers", 1)

		obj.addProperty("App::PropertyFloat","Cost","Member","Enter the cost of the construction member").Cost = 2.99
		obj.addProperty("App::PropertyString","Function","Member","Where this member is being used").Function = "Ceiling"
		obj.addProperty("App::PropertyString","MemberName","Member","Where this member is being used").MemberName = "Joist"
		obj.Proxy = self

		obj.addExtension('Part::AttachExtensionPython')
 
		newjoist = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "CeilingJoistBoard")
		joist = Part.makeBox(obj.Length,obj.Width,obj.Height, FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1 ) )

		newchamfer = FreeCAD.ActiveDocument.addObject("Part::Chamfer","CeilingJoistCuts")
		newchamfer.Base = newjoist


		__fillets__ = []
		__fillets__.append((2,76.20,76.20))
		__fillets__.append((6,76.20,76.20))

		newchamfer.Edges = __fillets__
		newjoist.Shape = joist

		# TODO: Read somewhere that you shouldn't use FreeCAD directly instead use an intance of the document.		

		newchamfer.Placement = FreeCAD.Placement( FreeCAD.Vector (50.79,88.89,2466.98),FreeCAD.Rotation (0.0, 0.0, -0.7071067811865475, 0.7071067811865476) )

		ViewProviderCeilingJoist(obj.ViewObject)						

		obj.addObject ( newchamfer )
		obj.addObject ( newjoist )

# 		TODO: Change to address the actual object created and set to false
#		FreeCADGui.ActiveDocument.CeilingJoist.Visibility = True
		obj.ViewObject.Visibility = True
		FreeCAD.ActiveDocument.recompute()

		
	def onChanged(self, fp, prop):

		if prop == "Length" or prop == "Width" or prop == "Height":
			fp.Group[0].Base.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height)
			FreeCAD.ActiveDocument.recompute()

		if prop == "Placement":
#			print ( "Placement Changed by name" )			

#		if isinstance ( prop, FreeCAD.Placement ):
#			print ( "Placement Changed by class" )			

			pass

	def execute(self,fp):

#		fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height, FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0 ) )
		fp.positionBySupport()

		
		#FreeCAD.ActiveDocument.recompute()
		fp.recompute()

class ViewProviderCeilingJoist:
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
			static char * ceilingjoist_xpm[] = {
			"64 64 4 1",
			" 	c None",
			".	c #010100",
			"+	c #DFAD00",
			"@	c #F2F466",
			"                  .   .          .+++.+++++++++.   .            ",
			"                 .   .          .+++.+++++++++.   .             ",
			"                .   .          .+++.+++++++++.   .             .",
			"               .   .          .+++.+++++++++.   .             . ",
			"              .   .          .+++.+++++++++.   .             .  ",
			"             .   .          .+++.+++++++++.   .             .   ",
			"            .   .          .+++.+++++++++.   .             .   .",
			"           .   .          .+++.+++++++++.   .             .   . ",
			"          .   .          .+++.+++++++++.   .             .   .  ",
			"         .   .          .+++.+++++++++.   .             .   .   ",
			"        .   .          .+++.+++++++++.   .             .   .    ",
			"       .   .          .+++.+++++++++.   .             .   .     ",
			"      .   .          .+++.+++++++++.   .             .   .      ",
			"     .   .          .+++.+++++++++.   .             .   .       ",
			"    .   .          .+++.+++++++++.   .             .   .        ",
			"   .   .          .+++.+++++++++.   .             .   .         ",
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
			"  .   .          .+++.+++++++++.   .           .@.   .          ",
			"  .   .          .+++.+++++++++.   .          .@@.   .          ",
			"  .   .         ..+++.+++++++++.   .         .@@@.   .         .",
			"  .   .        .@.+++.++++++++..   .        .@@@@.   .        .@",
			"  .   .       .@@.+++.+++++++.@.   .       .@@@@@.   .       .@@",
			"  .   .      .@@@.+++.++++++.@@.   .      .@@@@@@.   .      .@@@",
			"  .   .     .@@@@.+++.+++++.@@@.   .     .@@@@@@@.   .     .@@@@",
			"  .   .    .@@@@@.+++.++++.@@@@.   .    .@@@@@@@@.   .    .@@@@@",
			"  .   .   .@@@@@@.+++.+++.@@@@@.   .   .@@@@@@@@@.   .   .@@@@@@",
			"  .   .  .@@@@@@@.+++.++.@@@@@@.   .  .@@@@@@@@@@.   .  .@@@@@@@",
			"  .   . .@@@@@@@@.+++.+.@@@@@@@.   . .@@@@@@@@@@@.   . .@@@@@@@@",
			"  .   ..@@@@@@@@@.+++..@@@@@@@@.   ..@@@@@@@@@@@@.   ..@@@@@@@@@",
			"  .....@@@@@@@@@@.....@@@@@@@@@.....@@@@@@@@@@@@@.....@@@@@@@@@@",
			"  .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
			"  ..............................................................",
			"  .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
			"  .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
			"  .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
			"  .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
			"  ..............................................................",
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


FreeCADGui.addCommand('Ceiling Joist', CeilingJoist_Command())

