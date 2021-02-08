import FreeCAD, FreeCADGui, Part, Draft
import os
import math

__title__ = "FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"

__command_name__ = "Plate"
__command_group__ = "Members"

story_levels = [
    'None', 'Basement', '1st Floor', 'Second Floor', 'Third Floor', 'Attic'
]


def makeStory(name):

    newstory = FreeCAD.ActiveDocument.addObject("App::GeometryPython", name)

    #TODO: Make translatable ala Arch style translate
    #obj.Label = translate("Arch","BuildingPart")

    Story(newstory)
    ViewProviderCeilingJoist(newstory.ViewObject)

    FreeCAD.ActiveDocument.recompute()
    return newstory


class Story_Command:
    """
	The Story is a container for a single level of the construction.	
	"""
    def GetResources(self):

        #TODO: Move Icons to a resource file and all the path checking up to
        #		the framing class

		image_path = "/" + framing.mod_name + '/icons/story.png'
#        image_path = '/stickframe/icons/story.png'
        global_path = FreeCAD.getHomePath() + "Mod"
        user_path = FreeCAD.getUserAppDataDir() + "Mod"
        icon_path = ""

        if os.path.exists(user_path + image_path):
            icon_path = user_path + image_path
        elif os.path.exists(global_path + image_path):
            icon_path = global_path + image_path
        return {
            "MenuText": "Story",
            "ToolTip": "Add a Story container to the Construction",
            'Pixmap': str(icon_path)
        }

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
            return False
        else:
            return True

    def Activated(self):

        #:TODO: Create a Transaction

        #newstory = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "Story")
        newstory = FreeCAD.ActiveDocument.addObject("App::GeometryPython",
                                                    "BuildingPart")

        FreeCADGui.addModule("Draft")
        Draft.autogroup(newstory)

        ViewProviderStory(newstory.ViewObject)
        Story(newstory)

        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")


class Story():
    def __init__(self, obj):

        obj.Proxy = self

        obj.addExtension('App::GroupExtensionPython', self)

        obj.addProperty("App::PropertyPlacement", "Placement", "Base",
                        "Location of this Member")
        obj.addProperty("App::PropertyString", "MemberName", "Member",
                        "Where this member is being used").MemberName = "Story"

        ViewProviderStory(obj.ViewObject)
        obj.ViewObject.Visibility = True

        FreeCAD.ActiveDocument.recompute()

    def onChanged(self, fp, prop):

#        print("Executing Change")

        if prop == "Length" or prop == "Width" or prop == "Height":
#            print("Property Changed")

            #self.Placement.Base = self.Placement.Base.mulitply ( fp.Placement )
            fp.getObject("CeilingJoistCuts").base.Shape = Part.makeBox(
                fp.Length, fp.Width, fp.Height)

        if prop == "Placement":
#            print("Placement Changed by name")

             pass

    def execute(self, fp):

        fp.recompute()


class ViewProviderStory:
    def __init__(self, vobj):

        #		vobj.addExtension("Gui::ViewProviderGroupExtensionPython", self)

        vobj.Proxy = self

    def getDisplayModes(self, obj):
        ''' Return a list of display modes. '''
        modes = []
        return modes

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Lines"

    def setDisplayMode(self, mode):
        ''' Map the display mode defined in attach with those defined in getDisplayModes.
		Since they have the same names nothing needs to be done. This method is optional.
		'''
        return mode

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

    def __setstate__(self, state):
        ''' When restoring the pickled object from document we have the chance to set some
		internals here. Since no data were pickled nothing needs to be done here.
		'''
        return None


FreeCADGui.addCommand('Story', Story_Command())
