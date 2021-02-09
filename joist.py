import FreeCAD,FreeCADGui,Part, Draft
import os
import math
import framing

class FloorJoist_Command:	
	"""
	The floor joist is a pre-dtermined size lumber that hsa a 
	relationship to rim joists and other flooring sub-componants.
	"""

	def GetResources(self):

#		image_path = "/" + framing.mod_name + '/icons/floorjoist.png'
		image_path = '/stickframe/icons/floorjoist.png'
		global_path = FreeCAD.getHomePath()+"Mod"
		user_path = FreeCAD.getUserAppDataDir()+"Mod"
		icon_path = ""
		 
		if os.path.exists(user_path + image_path):
			icon_path = user_path + image_path
		elif os.path.exists(global_path + image_path):
			icon_path = global_path + image_path
		return {"MenuText": "Joist",
			"ToolTip": "Add a Joist to the Construction",
			'Pixmap' : str(icon_path) } 

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		thisjoist=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","FloorJoist")
		thisjoist.ViewObject.Proxy=0
		newjoist = Joist(thisjoist)
		FreeCAD.ActiveDocument.recompute() 

class FloorJoist():

	def __init__(self, obj):
		obj.addProperty("App::PropertyLength","Length","Dimension","Change the length of the Joist").Length = "96 in"

		obj.addProperty("App::PropertyFloat","Cost","Member","Enter the cost of the construction member").Cost = 2.99
		obj.addProperty("App::PropertyString","Function","Member","Where this member is being used").Function = "Floor"
		obj.addProperty("App::PropertyString","MemberName","Member","Where this member is being used").MemberName = "Joist"
		obj.Proxy = self
		
	def onChanged(self, fp, prop):
		''' Do something here '''
		#fp.getPropertyByName("GhostName") = str(prop)

	def execute(self,fp):

		joist = Part.makeBox(190.5,38.10,2438.40)

		fp.Shape = joist
		fp.ViewObject.Proxy=0

FreeCADGui.addCommand('Floor Joist', FloorJoist_Command())

