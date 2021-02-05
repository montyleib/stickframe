import FreeCADGui 
class StickFrameWorkbench ( FreeCADGui.Workbench ):
	"""Stick Framing workbench object"""

	MenuText = "Stick Frame Workbench"
	ToolTip = "A workbench for educational purposes,ie., how to make a workbench"

	def GetClassName(self):
		return "Gui::PythonWorkbench"
 	
	def Initialize(self):
		import stud, plate, framingreload
		self.appendToolbar("StickFrame",["Stud","Plate","Reload"])
		self.appendMenu("StickFrame", ["Stud","Plate","Reload"])
		Log ("The StickFrame Module Initialize method has been run \n")
 
	def Activated(self):
		# do something here if needed...
		Msg ("StickFrameWorkbench.Activated()\n")

	def Deactivated(self):
		# do something here if needed...
		Msg ("StickFrameWorkbench.Deactivated()\n")

