

class NewStickFrameWorkbench (Workbench):
    "Stick Framing workbench object"
    Icon = "./icons/logo.svg"
	
# logo.xpm removed

    MenuText = "Stick Frame Workbench"
    ToolTip = "A workbench for educational purposes,ie., how to make a workbench"

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        import os
        import fnmatch


# This is an attempt at a command autoloader, to make adding commands easier.

#        cmds_path = FreeCAD.getUserAppDataDir()+"Mod/framing/commands"

#        print(cmds_path)
#        listOfFiles = os.listdir(cmds_path)
#        pattern = "*.py"
#        for entry in listOfFiles:
#            if fnmatch.fnmatch(entry, pattern):
#                print(entry)
#                mod_name = entry.split(".")[0]
#                print("Module Name: ", mod_name)
#				com_name = str(mod_name).capitalize()
#				print ( "Command Name: ",com_name )

# TODO : add code to exclude empty __init__.py, 	empty __init__.py is added
#		to sub-directories so that the files may be imported otherwise
#		python blocks them, for security.

#				try:
                # module = __import__ ("commands." + mod_name)
#					module = __import__ (mod_name)
#					print ( module )
#					com_name = module.__command_name__
#					print ( "Command Name: ",com_name )
#
#				except ImportError as ie:
#					raise ImportError("Error: {} when importing {}".format( ie, mod_name))
#
#				if module.__command_group__ == "Members":
#					self.appendToolbar("Members",[ com_name ] )
#				if module.__command_group__ == "Constructions":
#					self.appendToolbar("Constructions",[ com_name ] )
#
#				self.appendMenu("StickFrame", [ com_name ] )

# Eventually for drop down list
#		panelscmdlist = ['Panel','FloorPanel','CeilingPanel','RoofPanel']
#		panelscmdgrp = ['Framing_PanelTools']

#        FreeCADGui.addCommand('Framing_PanelTools', PathCommandGroup(panelscmdlist, QtCore.QT_TRANSLATE_NOOP("Framing", 'Panel Types')))

        import stud , plate, studspacer, floorjoist, ceilingjoist, rafter, collarbeam, ridgebeam, stringer, story
        import panel ,roofpanel, floorpanel, ceilingpanel
        import wall, simplewall, window, roof, door, ceiling
        import floor, wall, simplewall, window, roof, door, ceiling
        import header
		#        import joist_tool
        import staircase
        import stringer_sketch
        import rafter_sketch
        import roof_truss_kingpost, roof_truss_queenpost,roof_truss_assymetric, roof_truss_inverted, roof_truss_monoa, roof_truss_monob, roof_truss_openplan, roof_truss_storage

        import floorplanview
        import framingreload

        self.appendMenu("Stick Framing", ["Stud", "Plate", "Studspacer", "Floor Joist", "Ceiling Joist", "CollarBeam", "Rafter", "Stringer", "Ridgebeam", "Story"])
        self.appendMenu("Stick Framing", ["FloorPanel", "Floor", "Wall", "Window", "Door", "Ceiling", "RoofPanel", "Roof", "Stringer", "StairCase"])
        self.appendMenu("Stick Framing Roof Trusses", ["KingPost","QueenPost","MonoA","MonoB","CruckBlade","Assymetric","Inverted","OpenPlan","Storage"])
        self.appendMenu("Stick Framing Utilites", ["FloorPlanView"])

        self.appendToolbar("Members", ["Stud", "Plate", "Studspacer", "Floor Joist", "Ceiling Joist", "CollarBeam", "Rafter", "Stringer", "Ridgebeam","Story"])
#        self.appendToolbar("Timber", ["CruckBlade","Purlin","WindBrace","Brace","CornerPost","KingPost","Spurs","Girt","Nogging" ])
        
        self.appendToolbar("DoorandWindow", ["Header"])
        self.appendToolbar("Panels", ["Panel", "FloorPanel", "CeilingPanel", "RoofPanel"])
        self.appendToolbar("Constructions", ["Floor", "Window", "Door", "Wall", "SimpleWall", "Ceiling", "Roof", "StairCase"])
        self.appendToolbar("Roof Truss", ["KingPost","QueenPost","MonoA","MonoB","CruckBlade","Assymetric","Inverted","OpenPlan","Storage"])
        self.appendToolbar("Testing", ["Stringer_Sketch", "Rafter_Sketch"])

        self.appendToolbar("Utilities", ["FramingReload","FloorPlanView"])

        print( "Stickframe check ????")
        Log ("The StickFrame Module Initialize method has been run \n")

#        from PySide import QtGui ,QtCore
#        QtGui.QMessageBox.information(None, "WARNING!!!", "This Workbench is extremely unstable. It was created for the educational oppurtunities. \n\n It is more like an extreme Macro than a well coded workbench. \n\n I thought others #MIGHT be able to use it. Likely it will only frustrrate you. You have been warned")

		

    def Activated(self):
        # do something here if needed...
        Log ("FramingWorkbench.Activated()\n")
        pass

    def Deactivated(self):
        # do something here if needed...
        Log ("FramingWorkbench.Deactivated()\n")
        pass


FreeCADGui.addWorkbench(NewStickFrameWorkbench)
