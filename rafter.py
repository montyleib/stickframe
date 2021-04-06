import FreeCAD
import FreeCADGui
import Part
import Draft
import Sketcher
import os

import rafter_sketch
import framing

__title__ = "FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"

__command_name__ = "Rafter"  # Name of the command to appear in Toolbar
__command_group__ = ""  # Name of Toolbar to assign the command


#def makeRafter(name):

#	newgrpobj = FreeCAD.ActiveDocument.addObject( "App::DocumentObjectGroupPython", "Rafter")
#	newsketch = FreeCAD.ActiveDocument.addObject( 'Sketcher::SketchObjectPython', "RafterSketch")
#	(newsketch)

#	moveobj = FreeCAD.ActiveDocument.getObject(newsketch.Name)
#	moveobj.Placement = FreeCAD.Placement(FreeCAD.Vector(1.50019e-13, -1111.25, 1993.25 + 38.1), FreeCAD.Rotation( 0.5015264712616718, -0.4992350141084935, -0.4992350141084935, 0.5000000000000001))



#	newgrpobj.addObject(extrusion)
#	ViewProviderRafter(newgrpobj.ViewObject)
#	FreeCAD.ActiveDocument.recompute()

#	FreeCADGui.SendMsgToActiveView("ViewFit")

#	return newgrpobj

def makeRafter(name):
	newrafter = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "Rafter")
	Rafter(newrafter)
	ViewProviderRafter(newrafter.ViewObject)
	return newrafter;

#Single Story Placement
	newrafter.Placement = FreeCAD.Placement( FreeCAD.Vector (1.50019e-13, -1111.25, 1993.25 + 38.1),FreeCAD.Rotation ( 0.5015264712616718, -0.4992350141084935, -0.4992350141084935, 0.5000000000000001) )
	FreeCAD.ActiveDocument.recompute()
	return newrafter

class Rafter_Command:
	def GetResources(self):
		icon_path = framing.getIconImage( "rafter" ) 	

#		image_path = "/" + framing.mod_name + '/icons/rafter.png'
		# image_path = '/stickframe/icons/rafter.png'
		# global_path = FreeCAD.getHomePath()+'Mod'
		# user_path = FreeCAD.getUserAppDataDir()+'Mod'
		# icon_path = ''

		# if os.path.exists(user_path + image_path):
		# 	icon_path = user_path + image_path
		# elif os.path.exists(global_path + image_path):
		# 	icon_path = global_path + image_path
		return {'MenuText': 'Rafter',
			'ToolTip': 'Add a roof rafter to the construction.',
			'Pixmap': str(icon_path)}

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			# print 'Rafter command is NOT active'
			return False
		else:
			# print 'Rafter command IS active'
			return True

	def Activated(self):

		newrafter = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "Rafter")
#		newrafter = FreeCAD.ActiveDocument.addObject("App::GeoFeatureGroupExtensionPython", "Rafter")
#		newrafter = FreeCAD.ActiveDocument.addObject("Part::Feature", "Rafter")

#		newrafter.addExtension('App::GroupExtensionPython',obj )
#		newrafter.addExtension('App::GeoFeatureGroupExtensionPython',obj )

		ViewProviderRafter(newrafter.ViewObject)
		Rafter(newrafter)

		newrafter.Visibility = True

#		newrafter.Placement = FreeCAD.Placement( FreeCAD.Vector (1.50019e-13, -1111.25, 1993.25 + 38.1),FreeCAD.Rotation ( 0.5015264712616718, -0.4992350141084935, -0.4992350141084935, 0.5000000000000001) )

		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.SendMsgToActiveView("ViewFit")


class Rafter:

	def __init__(self, obj):
		
		obj.addProperty("App::PropertyLength", "Rise", "Lumber Dimension", "The Rise of the roof.").Rise = "48 in"
		obj.addProperty("App::PropertyLength", "Run", "Lumber Dimension", "The Run of the roof").Run = "48 in"
		obj.addProperty("App::PropertyLength", "BoardLength", "Lumber Dimension", "The Run of the roof").BoardLength = "96 in"

		obj.addProperty("App::PropertyFloat", "Cost", "Member","Enter the cost of the construction member").Cost = 2.99
		obj.addProperty("App::PropertyEnumeration", "Function", "Member", "Where this member is being used").Function = ['Roof Rafter']
		obj.addProperty("App::PropertyString", "MemberName", "Member","Where this member is being used").MemberName = "Rafter"
		obj.Proxy = self

#		obj.addExtension("App::GroupExtensionPython",self)
#		obj.addExtension('App::GeoFeatureGroupExtensionPython',obj )
#		obj.addExtension('App::GeoFeatureGroupExtensionPython',obj )
#		obj.addExtension('Part::OriginExtensionPython', obj)
#		obj.addExtension('App::PlacementExtensionPython', obj)
#		obj.addExtension('Part::AttachExtensionPython', obj)
#		obj.addExtension('Part::AttachExtensionPython', obj)
#		obj.addExtension('App::OriginGroupExtensionPython',None)

#		obj.Origin = FreeCAD.ActiveDocument.addObject('App::Origin','Origin')


		sketch = rafter_sketch.makeRafterSketch("RafterSketch" )
		sketch.Visibility = False
#		sketch.ShowInTree = False

		newextrusion = FreeCAD.ActiveDocument.addObject("Part::Extrusion", "RafterExtrusion")
#		newextrusion.addExtension('App::GeoFeatureGroupExtensionPython',obj )
		
		newextrusion.Base = FreeCAD.ActiveDocument.getObject(sketch.Name)
		newextrusion.Dir = (1,0 , 0)
		newextrusion.LengthFwd = '1.5 in'
		newextrusion.Solid = True

		obj.addObject( sketch )
		obj.addObject( newextrusion )

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#print ("Property Changed" )
		if prop == "Length" or prop == "Width" or prop == "Height":
			fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height)


#		print ( 'Changed property: ' + name + 'to ' + newvalue + '' )
#		FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 
		if prop == "Rise":
		#>>> App.getDocument('Unnamed').getObject('RafterSketch').setDatum(25,App.Units.Quantity('1100.000000 mm'))
			#print ("rise Changed" )
			fp.Group[0].setDatum(32, fp.Rise )
		if prop == "Run":
			fp.Group[0].setDatum(25, fp.Run )
		if prop == "BoardLength":
			#need a check as board length can't be less than hypotenuese
			#print ("BoardLength Changed" )
			fp.Group[0].setDatum(34, fp.BoardLength )

	def execute(self,fp):	
		fp.recompute()
#		print ' Rafter Class executed()'

class ViewProviderRafter:
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
static char * rafter2_xpm[] = {
"64 64 3 1",
" 	c None",
".	c #040A00",
"+	c #E1B313",
"                                                        .       ",
"                                                       ..       ",
"                                                      .+.       ",
"                                                     .++.       ",
"                                                    .+++.       ",
"                                                   .++++.       ",
"                                                  .+++++.       ",
"                                                 .++++++.       ",
"                                                .+++++++.       ",
"                                               .++++++++.       ",
"                                              .+++++++++.       ",
"                                             .++++++++++.       ",
"                                            .+++++++++++.       ",
"                                           .++++++++++++.       ",
"                                          .++++++++++++.        ",
"                                         .++++++++++++.         ",
"                                        .++++++++++++.          ",
"                                       .++++++++++++.           ",
"                                      .++++++++++++.            ",
"                                     .++++++++++++.             ",
"                                    .++++++++++++.              ",
"                                   .++++++++++++.               ",
"                                  .++++++++++++.                ",
"                                 .++++++++++++.                 ",
"                                .++++++++++++.                  ",
"                               .++++++++++++.                   ",
"                              .++++++++++++.                    ",
"                             .++++++++++++.                     ",
"                            .++++++++++++.                      ",
"                           .++++++++++++.                       ",
"                          .++++++++++++.                        ",
"                         .++++++++++++.                         ",
"                        .++++++++++++.                          ",
"                       .++++++++++++.                           ",
"                      .++++++++++++.                            ",
"                     .++++++++++++.                             ",
"                    .++++++++++++.                              ",
"                   .++++++++++++.                               ",
"                  .++++++++++++.                                ",
"                 .++++++++++++.                                 ",
"                .++++++++++++.                                  ",
"               .++++++++++++.                                   ",
"              .++++++++++++.                                    ",
"             .++++++++++++.                                     ",
"            .++++++++++++.                                      ",
"           .++++++++++++.                                       ",
"          .++++++++++++.                                        ",
"         .++++++++++++.                                         ",
"        .++++++++++++.                                          ",
"       .+++++++......                                           ",
"       .+++++++.                                                ",
"       .+++++++.                                                ",
"       .+++++++.                                                ",
"       .+++++++.                                                ",
"       .+++++++.                                                ",
"       .++++++.                                                 ",
"       .+++++.                                                  ",
"       .++++.                                                   ",
"       .+++.                                                    ",
"       .++.                                                     ",
"       .+.                                                      ",
"       ..                                                       ",
"       .                                                        ",
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


FreeCADGui.addCommand('Rafter',Rafter_Command() ) 
