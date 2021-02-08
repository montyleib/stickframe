import FreeCAD
import FreeCADGui
import Part
import os

from importlib import reload



class FramingReload_Command:

    def GetResources(self):
        image_path = '/stickframe/icons/reload.png'
        global_path = FreeCAD.getHomePath()+"Mod"
        user_path = FreeCAD.getUserAppDataDir()+"Mod"
        icon_path = ""

        if os.path.exists(user_path + image_path):
            icon_path = user_path + image_path
        elif os.path.exists(global_path + image_path):
            icon_path = global_path + image_path
        return {"MenuText": "FramingReload",
                "ToolTip": "Reload my classes",
                'Pixmap': str(icon_path)}

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
            return False
        else:
            return True

    def Activated(self):

        import os
        import fnmatch
        cmds_path = FreeCAD.getUserAppDataDir()+"Mod/framing/commands"

        print (cmds_path)
        listOfFiles = os.listdir(cmds_path)
        pattern = "*.py"
        for entry in listOfFiles:
            if fnmatch.fnmatch(entry, pattern):
                print (entry)
                mod_name = entry.split(".")[0]
                print ("Module Name: ", mod_name)
#				com_name = str(mod_name).capitalize()
#				print ( "Command Name: ",com_name )

# TODO : add code to exclude empty __init__.py, 	empty __init__.py is added
#		to sub-directories so that the files may be imported otherwise
#		python blocks them, for security.

                try:
                    # TODO : Load from commands. directory
                    #module = __import__ ("commands." + mod_name)
                    module = __import__(mod_name)
                    print (module)
                    reload(module)
                except ImportError as ie:
                    raise ImportError(
                        "Error: {} when importing {}".format(ie, mod_name))

        # FreeCADGui.removeWorkbench("StickFrameWorkbench")

        #import StickFrameWorkbench
        #nw = FreeCADGui.Workbench
        #sf = StickFrameWorkbench
        # sf.StickFrameWorkbench.Initialize

        try:
            import stud
            import plate
            import floorjoist
            import floor
            import wall
            import staircase
            import door
            import window
            import ceilingjoist
            import rafter
            import collarbeam
            import studspacer
            import ridgebeam
            import header
            import panel
            import floorpanel
            import ceilingpanel
            import roofpanel
            import stringer
            from stringer import Stringer

        except:
            print ("Import Error")

        try:
            reload(stud)
            reload(plate)
            reload(floorjoist)
            reload(floor)
            reload(wall)
            reload(staircase)
            reload(door)
            reload(window)
            reload(ceilingjoist)
            reload(rafter)
            reload(collarbeam)
            reload(studspacer)
            reload(ridgebeam)
            reload(header)
            reload(panel)
            reload(floorpanel)
            reload(ceilingpanel)
            reload(roofpanel)
            reload(stringer)
            reload(Stringer)

        except:
            print ("Reload Error")

        print ("Framing Commands Reloaded")


FreeCADGui.addCommand('FramingReload', FramingReload_Command())
