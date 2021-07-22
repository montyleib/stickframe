import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os
import framing, stud

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "Storage" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class Storage_Command:
	def GetResources(slf):
		#print 'Run getResources() for Storage_Command' 
		icon_path = framing.getIconImage( "storage")
		
		return {'MenuText': 'Storage', 
			'ToolTip': 'Tooltip for Storage command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'Storage command is NOT active' 
			return False 
		else: 
			#print 'Storage command IS active' 
			return True 
 
	def Activated(self): 
	
		newtruss = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "StorageTruss")
		ViewProviderStorage(newtruss.ViewObject)
		Storage ( newtruss )		
		newtruss.Visibility = True
		FreeCAD.ActiveDocument.recompute()  
		FreeCADGui.SendMsgToActiveView("ViewFit")
 
#		#print 'StorageCommand activated' 
 
#		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','Storage') 
#		newsampleobject = Storage(b) 
#		b.ViewObject.Proxy=0 
#		FreeCAD.ActiveDocument.recompute() 
		
#		framing.populateStuds( b, "Truss" ) 
class Storage:
	def __init__(self, obj):
		obj.addProperty("App::PropertyLength", "Rise", "Lumber Dimension", "The Rise of the roof.").Rise = "48 in"
		obj.addProperty("App::PropertyLength", "Run", "Lumber Dimension", "The Run of the roof").Run = "48 in"
		obj.Proxy = self		


		newsketch = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','StorageSketch') 
		StorageSketch(newsketch) 
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


class StorageSketch: 
 
 
	def __init__(self, obj):
 
		#print 'The Storage class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-405.530396, -1.1737312160261198e-31, 0.0), App.Vector (0.0, 390.17266173470676, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1.2127674758214812e-29, 390.17266173470676, 0.0), App.Vector (405.5303959999999, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (405.5303959999999, -1.1737312160261198e-31, 0.0), App.Vector (-405.530396, -1.1737312160261198e-31, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-198.78692216059636, -1.1737312160261198e-31, 0.0), App.Vector (-198.78692216059636, 198.91394647566653, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-198.78692216059636, 198.91394647566653, 0.0), App.Vector (198.78692216059636, 198.91394647566653, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (198.78692216059636, 198.91394647566653, 0.0), App.Vector (198.78692216059636, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1.2127674758214812e-29, 198.91394647566653, 0.0), App.Vector (-1.2127674758214812e-29, 390.17266173470676, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-198.78692216059636, -1.1737312160261198e-31, 0.0), App.Vector (-298.1698231166517, 103.29474905071974, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (198.78692216059636, -1.1737312159974212e-31, 0.0), App.Vector (298.1698231166517, 103.29474905071969, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',0,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,-1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,2,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,0,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',0,2,-2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,1,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,2,0 ) )
		constraintList.append( Sketcher.Constraint('Vertical',3 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,1,3,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,2,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',4 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,1,4,2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',5 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,2,0,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,1,3,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',7,2,0 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,1,5,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',8,2,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',5,2,2 ) )
		constraintList.append( Sketcher.Constraint('Perpendicular',1,0,8 ) )
		constraintList.append( Sketcher.Constraint('Perpendicular',0,0,7 ) )
		constraintList.append( Sketcher.Constraint('Symmetric',3,2,4,2,6))


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
		print (' Storage Class executed() ') 

class ViewProviderStorage:
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
static char * storage_xpm[] = {
"64 42 61 1",
" 	c None",
".	c #000000",
"+	c #620000",
"@	c #DC0000",
"#	c #CD0000",
"$	c #FF0000",
"%	c #C20000",
"&	c #C10000",
"*	c #370000",
"=	c #B90000",
"-	c #8D0000",
";	c #AC0000",
">	c #480000",
",	c #1A0000",
"'	c #A20000",
")	c #8A0000",
"!	c #DF0000",
"~	c #BA0000",
"{	c #AB0000",
"]	c #F40000",
"^	c #CF0000",
"/	c #F50000",
"(	c #440000",
"_	c #F20000",
":	c #9F0000",
"<	c #750000",
"[	c #EB0000",
"}	c #910000",
"|	c #D70000",
"1	c #A50000",
"2	c #360000",
"3	c #FC0000",
"4	c #6F0000",
"5	c #700000",
"6	c #930000",
"7	c #DB0000",
"8	c #A80000",
"9	c #4F0000",
"0	c #C00000",
"a	c #B00000",
"b	c #190000",
"c	c #A60000",
"d	c #C40000",
"e	c #630000",
"f	c #DA0000",
"g	c #AA0000",
"h	c #970000",
"i	c #E70000",
"j	c #D90000",
"k	c #E20000",
"l	c #F10000",
"m	c #7C0000",
"n	c #E10000",
"o	c #D50000",
"p	c #420000",
"q	c #340000",
"r	c #CE0000",
"s	c #E40000",
"t	c #8B0000",
"u	c #8C0000",
"v	c #430000",
"                              ....                              ",
"                             .+@@+.                             ",
"                             .#$$#.                             ",
"                             .%$$&.                             ",
"                              *==*                              ",
"                             ......                             ",
"                            .. .. ..                            ",
"                            .  ..  .                            ",
"                           .   ..   .                           ",
"                          .    ..    .                          ",
"                         ..    ..    ..                         ",
"                        ..     ..     ..                        ",
"                        .      ..      .                        ",
"                       .       ..       .                       ",
"                      .        ..        .                      ",
"                     ..        ..        ..                     ",
"                    ..         ..         ..                    ",
"                    .          ..          .                    ",
"                ....           ..           ....                ",
"               .-;>.          ,'',          .>;-.               ",
"              .)$$!.         .~$$~.         .!$$).              ",
"              .{$$]...........^$$^.........../$${.              ",
"               (!_:.         .<[[<.         .:_!(               ",
"               ....           ....           ....               ",
"              .  .                            .  .              ",
"             ..  .                            .  ..             ",
"            ..   .                            .   ..            ",
"           ..    .                            .    ..           ",
"           .     .                            .     .           ",
"       ....      .                            .      ....       ",
"      .}|1.      .                            .      .1|}.      ",
"      23$$4      .                            .      4$$32      ",
"      *3$$5      .                            .      5$$32      ",
"      .678.      .                            .      .876.      ",
"      .... ..    .                            .    .. ....      ",
"     ..     ..   .                            .   ..     ..     ",
"  ....       .. ..                            .. ..       ....  ",
".90ab         ..cde.                        .edc..         ba09.",
".f$$g.        .h$$i.                        .i$$h.        .{$$j.",
".k$$~..........c$$l..........................l$$c..........~$$k.",
".mnop          qrst.                        .usrq          vonm.",
" ...            ...                          ...            ... "};				
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

		
FreeCADGui.addCommand('Storage',Storage_Command() ) 
