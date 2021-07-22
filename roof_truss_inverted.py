import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os
import framing, stud

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "Inverted" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class Inverted_Command:
	def GetResources(slf):
		#print 'Run getResources() for Inverted_Command' 
		icon_path = framing.getIconImage( "invertedtruss")
		return {'MenuText': 'Inverted', 
			'ToolTip': 'Tooltip for Inverted command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'Inverted command is NOT active' 
			return False 
		else: 
			#print 'Inverted command IS active' 
			return True 
 
	def Activated(self): 
		newtruss = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "InvertedTruss")
		ViewProviderInverted(newtruss.ViewObject)
		Inverted ( newtruss )		
		newtruss.Visibility = True
		FreeCAD.ActiveDocument.recompute()  
		FreeCADGui.SendMsgToActiveView("ViewFit")
 
#		#print 'InvertedCommand activated' 
 #
#		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','Inverted') 
#		newsampleobject = Inverted(b) 
#		b.ViewObject.Proxy=0 
#		FreeCAD.ActiveDocument.recompute()  
		
#		framing.populateStuds  ( b, "Truss" )
class Inverted:
	def __init__(self, obj):
		obj.addProperty("App::PropertyLength", "Rise", "Lumber Dimension", "The Rise of the roof.").Rise = "48 in"
		obj.addProperty("App::PropertyLength", "Run", "Lumber Dimension", "The Run of the roof").Run = "48 in"
		obj.Proxy = self		


		newsketch = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','InvertedSketch') 
		InvertedSketch(newsketch) 
		newsketch.ViewObject.Proxy=0
		newsketch.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000,0.000000,0.000000),FreeCAD.Rotation(0.500000, 0.500000, 0.500000, 0.500000))

		newsketch.Visibility = True

		obj.addObject( newsketch )


		newsketch.recompute()
		print ( obj.Content )
		print ( newsketch.Content )

		print ( newsketch.Shape )
		print ( newsketch.Shape.Content )

		truss_studs = framing.populateStuds( newsketch, "Truss" )
		
		print ( truss_studs )
		
#		print ( newsketch.Shape.Edges )
#		framing.populateStuds( newsketch, "Truss" )

		for stud in truss_studs:
			obj.addObject( stud )

	def onChanged(self, fp, prop):
		pass

	def execute(self,fp):	
		pass
		
class InvertedSketch: 
 
 
	def __init__(self, obj):
 
		#print 'The Inverted class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-1219.2, 0.0, 0.0), App.Vector (596.5603754867757, 1063.28, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (596.5603754867757, 1063.28, 0.0), App.Vector (0.0, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1219.2, 0.0, 0.0), App.Vector (0.0, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-765.2599061283062, 265.82000000000005, 0.0), App.Vector (-609.6, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (142.6202816150817, 797.4600000000002, 0.0), App.Vector (298.28018774338784, 531.64, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 0.0, 0.0), App.Vector (-311.3198122566123, 531.64, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-609.6, 0.0, 0.0), App.Vector (-311.3198122566123, 531.64, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (298.28018774338784, 531.64, 0.0), App.Vector (-311.3198122566123, 531.64, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',1,1,0,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,-1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,1,2 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,2,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,2,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,1,1,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,1,3,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,2,5,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,2,5,2 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',7 ) )
		constraintList.append( Sketcher.Constraint('Symmetric',0,2,0,1,5))
		named_constraint = Sketcher.Constraint('DistanceX',2,1,2,2,1219.2)
		named_constraint.Name = "Run"
		constraintList.append( named_constraint )
		constraintList.append( Sketcher.Constraint('Symmetric',5,2,0,1,3))
		constraintList.append( Sketcher.Constraint('Symmetric',0,2,5,2,4))
		constraintList.append( Sketcher.Constraint('PointOnObject',4,1,0 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,1,4,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,1,0 ) )
		named_constraint = Sketcher.Constraint('DistanceY',-1,1,0,2,1063.28)
		named_constraint.Name = "Rise"
		constraintList.append( named_constraint )

		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

		obj.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000, 0.000000, 0.000000), FreeCAD.Rotation(0.500000, 0.500000, 0.500000, 0.500000))

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print (' Inverted Class executed() ') 

class ViewProviderInverted:
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
static char * invertedtruss_xpm[] = {
"64 45 77 1",
" 	c None",
".	c #000000",
"+	c #980000",
"@	c #C60000",
"#	c #950000",
"$	c #970000",
"%	c #FF0000",
"&	c #910000",
"*	c #C40000",
"=	c #C50000",
"-	c #8E0000",
";	c #890000",
">	c #880000",
",	c #C20000",
"'	c #850000",
")	c #220000",
"!	c #020000",
"~	c #0E0000",
"{	c #CF0000",
"]	c #F40000",
"^	c #800000",
"/	c #8A0000",
"(	c #DF0000",
"_	c #DE0000",
":	c #030000",
"<	c #CA0000",
"[	c #F10000",
"}	c #7B0000",
"|	c #100000",
"1	c #070000",
"2	c #A20000",
"3	c #770000",
"4	c #4A0000",
"5	c #B90000",
"6	c #490000",
"7	c #B70000",
"8	c #FB0000",
"9	c #610000",
"0	c #E40000",
"a	c #A90000",
"b	c #060000",
"c	c #A10000",
"d	c #760000",
"e	c #B80000",
"f	c #CE0000",
"g	c #0D0000",
"h	c #210000",
"i	c #2A0000",
"j	c #AC0000",
"k	c #570000",
"l	c #5E0000",
"m	c #BC0000",
"n	c #A80000",
"o	c #1D0000",
"p	c #860000",
"q	c #D10000",
"r	c #F00000",
"s	c #3D0000",
"t	c #F30000",
"u	c #C80000",
"v	c #F90000",
"w	c #780000",
"x	c #7E0000",
"y	c #D50000",
"z	c #340000",
"A	c #460000",
"B	c #F60000",
"C	c #CD0000",
"D	c #920000",
"E	c #960000",
"F	c #390000",
"G	c #B50000",
"H	c #C10000",
"I	c #620000",
"J	c #6D0000",
"K	c #B30000",
"L	c #310000",
"  ...                                                           ",
" .+@#.                                                          ",
".$%%%&.                                                         ",
".*%%%=.                                                         ",
".-%%%;.                                                         ",
" .>,'...                                                        ",
"  .... ..                                                       ",
"    ..  ...                                                     ",
"     .    ..                                                    ",
"     ..    ...                                                  ",
"      .      ....)!.                                            ",
"      ..      .~{%]^.                                           ",
"      ..      ./%%%(.                                           ",
"       .      .>%%%_.                                           ",
"       ..      :<%[}.                                           ",
"        .      ..|.....                                         ",
"        ..     .      ..                                        ",
"         .    ..       ...                                      ",
"         .   ..          ..                                     ",
"         .....            ... ....                              ",
"        .12,3.              ..4556.                             ",
"        .7%%89.              .0%%0.                             ",
"        .(%%%a...............)%%%%).                            ",
"        .7%%89.              .0%%0.                             ",
"        .bc,d.               .65e6..                            ",
"          ...                ..... ...                          ",
"            ..              ..   .   ..                         ",
"             .              .    ..   ...                       ",
"             ..            ..     .     ..                      ",
"             ..           ..      ..     .....|..               ",
"              .           .        .       .}[%<:               ",
"              ..         ..        .       ._%%%>.              ",
"               .        ..         ..      .(%%%/.              ",
"               ..       .           .      .^]%fg.              ",
"               ..      ..           ..      .!h....             ",
"                .     ..             .     ..     ...           ",
"                ..    .              ..   ..        ..          ",
"                 .   ..              ..   .          ...        ",
"                 .....                .....            ..  ...  ",
"                .ij5k.               .lmno.             ...p,>. ",
"                .q%%ri.             .st%%u.              .;%%%-.",
"                .v%%%w...............x%%%r................=%%%*.",
"                .y%%tz.             .AB%%C.              .D%%%E.",
"                .FGHI.               .J,KL.               .#=$. ",
"                 ....                 ....                 ...  "};				
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
		
FreeCADGui.addCommand('Inverted',Inverted_Command() ) 
