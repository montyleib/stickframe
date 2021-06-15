import FreeCAD,FreeCADGui,Part, Draft
import os
import math
import framing

__title__="FreeCAD Framing"
__author__ = "Paul C. Randall"
__url__ = "http://www.freecad.info"

__command_name__ = "CollarBeam"
__command_group__ = "Members"

def makeCollar(name):
	newcollar = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", name)
	CollarBeam(newcollar)
	ViewProviderCollarBeam(newcollar.ViewObject)

#Single Story Placement
	newcollar.Placement = FreeCAD.Placement( FreeCAD.Vector (35.3317,-523.477,3243.03),FreeCAD.Rotation (0.0, 0.0, 0.7071067811865476, -0.7071067811865475) )

	FreeCAD.ActiveDocument.recompute()
	return newcollar

class CollarBeam_Command:
	"""
	The collar tie is a pre-determined size lumber that hsa a 
	relationship to Rafter angles, Wall Top Plates and other collar sub-components.
	"""

	def GetResources(self):
		icon_path = framing.getIconImage( "collartie" ) 	


#		image_path = "/" + framing.mod_name + '/icons/collartie.png'
		# image_path = '/stickframe/icons/collartie.png'
		# global_path = FreeCAD.getHomePath()+"Mod"
		# user_path = FreeCAD.getUserAppDataDir()+"Mod"
		# icon_path = ""
		 
		# if os.path.exists(user_path + image_path):
		# 	icon_path = user_path + image_path
		# elif os.path.exists(global_path + image_path):
		# 	icon_path = global_path + image_path
		return {"MenuText": "Collar Beam",
			"ToolTip": "Add a Collar Beam to the Construction",
			'Pixmap' : str(icon_path) } 

	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):

		newcollar = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "CollarTie")
		ViewProviderCollarBeam(newcollar.ViewObject)
		CollarBeam( newcollar )	

		framing.defaultAttachment( newcollar )

		newcollar.Placement = FreeCAD.Placement( FreeCAD.Vector (35.3317,-523.477,3243.03),FreeCAD.Rotation (0.0, 0.0, 0.7071067811865476, -0.7071067811865475) )

		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.SendMsgToActiveView("ViewFit")	

class CollarBeam():

	def __init__(self, obj):

		obj.addProperty("App::PropertyPlacement","Placement","Base","Location of this Member")
		obj.addProperty("App::PropertyLength","Length","Lumber Dimension","Change the board length of the Collar").Length = "48 in"
		obj.addProperty("App::PropertyLength","Width","Lumber Dimension","Change the board width of the Collar").Width = "1.5 in"
		obj.addProperty("App::PropertyLength","Height","Lumber Dimension","Change the board height of the Collar").Height = "3.5 in"

		obj.addProperty("App::PropertyLength","Centers","Construction Dimensions", "Distance between centers of this member.").Centers="16 in"
#		obj.addProperty("App::PropertyLength","Centers","Construction Dimensions", "Roof Slope determines cutoff angle").RoofSlope="7.5"
		obj.addProperty("App::PropertyFloat","Cost","Member","Enter the cost of the construction member").Cost = 2.99
		obj.addProperty("App::PropertyString","Function","Member","Where this member is being used").Function = "Collar"
		obj.addProperty("App::PropertyString","MemberName","Member","Where this member is being used").MemberName = "Joist"
		obj.Proxy = self

#		obj.addExtension('Part::AttachExtensionPython', obj)
		
		newcollar = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","CollarBeam")	
		collar = Part.makeBox(obj.Length,obj.Width,obj.Height, FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1 ) )

		newchamfer = FreeCAD.ActiveDocument.addObject("Part::Chamfer","CollarBeamCuts")
		newchamfer.Base = newcollar

		__fillets__ = []
		__fillets__.append((2,76.20,76.20))
		__fillets__.append((6,76.20,76.20))

		newchamfer.Edges = __fillets__
		newcollar.Shape = collar

		newchamfer.Placement = FreeCAD.Placement( FreeCAD.Vector (35.3317,-523.477,3243.03),FreeCAD.Rotation (0.0, 0.0, 0.7071067811865476, -0.7071067811865475) )

		ViewProviderCollarBeam(obj.ViewObject)	

		obj.addObject( newchamfer )
		obj.addObject( newcollar )


		obj.ViewObject.Visibility = True

		FreeCAD.ActiveDocument.recompute()
		
	def onChanged(self, fp, prop):

		if prop == "Length" or prop == "Width" or prop == "Height":
			fp.Group[0].Base.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height)
			FreeCAD.ActiveDocument.recompute()
		print ( fp.TypeId )
		
	def execute(self,fp):


#		fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height, FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0 ) )
		fp.recompute()

class ViewProviderCollarBeam:
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
			static char * collartie_xpm[] = {
			"64 39 139 2",
			"  	c None",
			". 	c #424300",
			"+ 	c #464700",
			"@ 	c #CED200",
			"# 	c #989B00",
			"$ 	c #A1A400",
			"% 	c #AFB200",
			"& 	c #A6A900",
			"* 	c #F1F600",
			"= 	c #979900",
			"- 	c #A0A300",
			"; 	c #DFE300",
			"> 	c #A9AC00",
			", 	c #A3A600",
			"' 	c #EAEE00",
			") 	c #F0F400",
			"! 	c #A1A300",
			"~ 	c #DDE000",
			"{ 	c #ECF000",
			"] 	c #BDC000",
			"^ 	c #C1C400",
			"/ 	c #E9ED00",
			"( 	c #BFC300",
			"_ 	c #A0A200",
			": 	c #ACB000",
			"< 	c #AEB000",
			"[ 	c #BDC100",
			"} 	c #BFC200",
			"| 	c #EBEF00",
			"1 	c #B7BB00",
			"2 	c #9D9F00",
			"3 	c #EDF100",
			"4 	c #B0B200",
			"5 	c #B5B700",
			"6 	c #F3F700",
			"7 	c #DEE200",
			"8 	c #7C7F00",
			"9 	c #8A8C00",
			"0 	c #999C00",
			"a 	c #848600",
			"b 	c #EEF200",
			"c 	c #A7AA00",
			"d 	c #B2B400",
			"e 	c #888B00",
			"f 	c #252600",
			"g 	c #272800",
			"h 	c #7B7D00",
			"i 	c #BBBF00",
			"j 	c #A9AB00",
			"k 	c #707200",
			"l 	c #6A6C00",
			"m 	c #939500",
			"n 	c #868800",
			"o 	c #939600",
			"p 	c #B3B500",
			"q 	c #888A00",
			"r 	c #787B00",
			"s 	c #767800",
			"t 	c #757800",
			"u 	c #9EA100",
			"v 	c #919300",
			"w 	c #919400",
			"x 	c #9A9D00",
			"y 	c #B1B300",
			"z 	c #787A00",
			"A 	c #B1B500",
			"B 	c #ECF100",
			"C 	c #7D7F00",
			"D 	c #828500",
			"E 	c #EDF200",
			"F 	c #6A6A00",
			"G 	c #D9DB00",
			"H 	c #D8DA00",
			"I 	c #DBDD00",
			"J 	c #909100",
			"K 	c #8B8D00",
			"L 	c #DADD00",
			"M 	c #DDDF00",
			"N 	c #848500",
			"O 	c #AA8400",
			"P 	c #BE9300",
			"Q 	c #BC9100",
			"R 	c #BD9200",
			"S 	c #BB9100",
			"T 	c #8C6D00",
			"U 	c #D3A300",
			"V 	c #D1A200",
			"W 	c #A88300",
			"X 	c #947300",
			"Y 	c #CFA000",
			"Z 	c #CFA100",
			"` 	c #BD9300",
			" .	c #525300",
			"..	c #787000",
			"+.	c #756E00",
			"@.	c #7E7700",
			"#.	c #3B3300",
			"$.	c #3A2D00",
			"%.	c #392C00",
			"&.	c #3B2E00",
			"*.	c #3B3200",
			"=.	c #777000",
			"-.	c #766F00",
			";.	c #5B5C00",
			">.	c #F1F500",
			",.	c #F2F600",
			"'.	c #F4F800",
			").	c #898B00",
			"!.	c #A8AB00",
			"~.	c #F5F900",
			"{.	c #A1A500",
			"].	c #9C9F00",
			"^.	c #C2C500",
			"/.	c #ADB000",
			"(.	c #808200",
			"_.	c #AAAE00",
			":.	c #8D9000",
			"<.	c #A9AD00",
			"[.	c #ABAE00",
			"}.	c #C0C300",
			"|.	c #EEF300",
			"1.	c #F3F800",
			"2.	c #8C8F00",
			"3.	c #9FA200",
			"4.	c #616300",
			"5.	c #828400",
			"6.	c #7A7C00",
			"7.	c #6D6F00",
			"8.	c #868900",
			"9.	c #6C6D00",
			"0.	c #757700",
			"a.	c #8D8F00",
			"b.	c #949600",
			"c.	c #333300",
			"d.	c #6C6E00",
			"e.	c #6B6D00",
			"f.	c #696B00",
			"g.	c #5F6000",
			"h.	c #404100",
			"                                                              . +                                                               ",
			"                                                            @ # $ %                                                             ",
			"                                                          & * = - ; >                                                           ",
			"                                                        , ' ) = ! ~ { ]                                                         ",
			"                                                      ^ ' / ) = ! ~ / ' (                                                       ",
			"                                                    _ ' / / ) = ! ~ / / { :                                                     ",
			"                                                  < ' / / / ) = ! ~ / / / { [                                                   ",
			"                                                } | / / / / ) = ! ~ / / / / ' 1                                                 ",
			"                                              2 ' / / / / / ) = ! ~ / / / / / 3 >                                               ",
			"                                            4 ' / / / / / / ) = ! ~ / / / / / / { [                                             ",
			"                                          5 { / / / / / / / 6 # $ 7 / / / / / / / ' %                                           ",
			"                                        = ' / / / / / / / | 8 9 0 a b / / / / / / / 3 c                                         ",
			"                                      d ' / / / / / / / { e   f g   h ' / / / / / / / | i                                       ",
			"                                    j { / / / / / / / 3 k             l { / / / / / / / | &                                     ",
			"                                  m ' / / / / / / / | n                 o 3 / / / / / / / 3 &                                   ",
			"                                p ' / / / / / / / 3 q                     r ' / / / / / / / ' 1                                 ",
			"                              2 { / / / / / / / { s                         t { / / / / / / / | u                               ",
			"                            v ' / / / / / / / | w                             x { / / / / / / / 3 &                             ",
			"                          y | / / / / / / / 3 q                                 z ' / / / / / / / ' A                           ",
			"                        m { / / / / / / / B C                                     D E / / / / / / / { #                         ",
			"                      F G H H H H H H H I J                                         K L H H H H H H H M N                       ",
			"                    O P Q Q Q Q Q Q Q Q Q R P R R R R R R R R R R R R R R R R R R R R Q Q Q Q Q Q Q Q Q P S                     ",
			"                  T U V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V W                   ",
			"                X Y Y Y Y Y Y Y Y Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Z Y Y Y Y Y Y Y Y `                 ",
			"               ...+.+.+.+.+.+.+.@.#.$.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.&.*.=.+.+.+.+.+.+.+.-.;.              ",
			"            o >.,.,.,.,.,.,.* '.).                                                            !.~.,.,.,.,.,.,.,.>.{.            ",
			"          > / / / / / / / / b q                                                                 ].' / / / / / / / ' ^.          ",
			"        /.b / / / / / / / ,.(.                                                                    a ' / / / / / / / ' _.        ",
			"      :.' / / / / / / / ' n                                                                         <.{ / / / / / / / ' -       ",
			"    [.' / / / / / / / ) 9                                                                             x ' / / / / / / / ' }.    ",
			"  $ |./ / / E >.>.>.1.a                                                                                 2.>.>.>.>.b / / / ' 3.  ",
			"4./ / / / { 5.                                                                                                    6./ / / / ' a ",
			"7./ / / / 3 n                                                                                                     n / / / / / K ",
			"7./ / / / 3 n                                                                                                     n / / / / / K ",
			"7./ / / / 3 8.                                                                                                    n / / / / / K ",
			"7./ / / / 1.9.                                                                                                    0.3 / / / / K ",
			"7./ / / b a.                                                                                                        :.| / / / K ",
			"7./ / | b.                                                                                                            {.{ / / K ",
			"c.d.e.f.                                                                                                                g.9.d.h."};
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


FreeCADGui.addCommand('CollarBeam', CollarBeam_Command())

