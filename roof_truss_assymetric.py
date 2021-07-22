import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os
import framing

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "Assymetric" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class Assymetric_Command:
	def GetResources(slf):
		#print 'Run getResources() for Assymetric_Command' 
		icon_path = framing.getIconImage( "assymetric")

		return {'MenuText': 'Assymetric', 
			'ToolTip': 'Tooltip for Assymetric command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'Assymetric command is NOT active' 
			return False 
		else: 
			#print 'Assymetric command IS active' 
			return True 
 
	def Activated(self): 
 
		newtruss = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "AssymetricTruss")
		ViewProviderAssymetric(newtruss.ViewObject)
		Assymetric ( newtruss )		
		newtruss.Visibility = True
		FreeCAD.ActiveDocument.recompute()  
		FreeCADGui.SendMsgToActiveView("ViewFit")
 
 
		#print 'AssymetricCommand activated' 
 
#		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','Assymetric') 
#		newsampleobject = Assymetric(b) 
#		b.ViewObject.Proxy=0 
#		FreeCAD.ActiveDocument.recompute()  
		
#		framing.populateStuds( b, "Truss" )
class Assymetric:
	def __init__(self, obj):
		obj.addProperty("App::PropertyLength", "Rise", "Lumber Dimension", "The Rise of the roof.").Rise = "48 in"
		obj.addProperty("App::PropertyLength", "Run", "Lumber Dimension", "The Run of the roof").Run = "48 in"
		obj.Proxy = self		


		newsketch = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','AssymetricSketch') 
		AssymetricSketch(newsketch) 
		newsketch.ViewObject.Proxy=0
		newsketch.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000,0.000000,0.000000),FreeCAD.Rotation(1,0,0,90))

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
		
	
class AssymetricSketch: 
 
 
	def __init__(self, obj):
 
		#print 'The Assymetric class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-1219.2, 0.0, 0.0), App.Vector (0.0, 1219.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-836.5152233413462, 382.68477665865373, 0.0), App.Vector (-836.5152233413462, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-836.5152233413462, 0.0, 0.0), App.Vector (-609.6, 609.6000000000001, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-609.6, 609.6000000000001, 0.0), App.Vector (-609.6, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-609.6, 0.0, 0.0), App.Vector (-248.13404006120254, 971.0659599387975, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-248.13404006120254, 971.0659599387975, 0.0), App.Vector (-248.13404006120254, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 1219.2, 0.0), App.Vector (0.0, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 1219.2, 0.0), App.Vector (609.6000000000001, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1219.2, 0.0, 0.0), App.Vector (609.6000000000001, 0.0, 0.0)))

		constructionList.append( Part.LineSegment( App.Vector (-1828.8, 0.0, 0.0), App.Vector (-1219.2, 0.0, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-1219.2, 0.0, 0.0), App.Vector (-609.6, 0.0, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-609.6, 0.0, 0.0), App.Vector (0.0, 0.0, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (-457.1999999999997, 0.0, 0.0), App.Vector (0.0, 0.0, 0.0)))


		constraintList.append( Sketcher.Constraint('PointOnObject',0,2,-2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,1,0 ) )
		constraintList.append( Sketcher.Constraint('Vertical',1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,2,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',2,2,0 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,3,1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',3 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,4,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,2,0 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,2,5,1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',5 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,1,0,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,2,-1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,1,0,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',7,2,-1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,-1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',5,2,-1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,2,7,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',0,1,8,1 ) )
		named_constraint = Sketcher.Constraint('DistanceX',0,1,6,2,1828.8)
		named_constraint.Name = "Run"
		constraintList.append( named_constraint )
		named_constraint = Sketcher.Constraint('DistanceY',6,2,6,1,1219.2)
		named_constraint.Name = "Rise"
		constraintList.append( named_constraint )
		named_constraint = Sketcher.Constraint('DistanceX',6,2,7,2,609.6)
		named_constraint.Name = "RunB"
		constraintList.append( named_constraint )

		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,8 ) )		
		constraintList.append( Sketcher.Constraint('PointOnObject',3,2,8 ) )


		constraintList.append( Sketcher.Constraint('Coincident',9,2,10,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',10,2,11,1 ) )		

		constraintList.append( Sketcher.Constraint('Coincident',9,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',9,2,1,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',10,2,3,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',11,2,5,2 ) )

		constraintList.append( Sketcher.Constraint('Equal',9,10))
		constraintList.append( Sketcher.Constraint('Equal',11,10))

		constraintList.append( Sketcher.Constraint('Coincident',12,1,11,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',12,2,-1,1 ) )
		constraintList.append( Sketcher.Constraint('Equal',12,11))


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
		print (' Assymetric Class executed() ') 


class ViewProviderAssymetric:
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
static char * assymetric_xpm[] = {
"64 39 86 1",
" 	c None",
".	c #000000",
"+	c #930000",
"@	c #E10000",
"#	c #C50000",
"$	c #1C0000",
"%	c #1B0000",
"&	c #F90000",
"*	c #FF0000",
"=	c #9E0000",
"-	c #160000",
";	c #F60000",
">	c #970000",
",	c #840000",
"'	c #D90000",
")	c #B60000",
"!	c #0D0000",
"~	c #580000",
"{	c #BB0000",
"]	c #980000",
"^	c #E70000",
"/	c #AE0000",
"(	c #AA0000",
"_	c #E40000",
":	c #4D0000",
"<	c #7B0000",
"[	c #5C0000",
"}	c #C60000",
"|	c #FC0000",
"1	c #800000",
"2	c #F50000",
"3	c #C40000",
"4	c #960000",
"5	c #F70000",
"6	c #EB0000",
"7	c #680000",
"8	c #C70000",
"9	c #D60000",
"0	c #410000",
"a	c #A50000",
"b	c #090000",
"c	c #5F0000",
"d	c #D20000",
"e	c #CA0000",
"f	c #440000",
"g	c #670000",
"h	c #D40000",
"i	c #360000",
"j	c #710000",
"k	c #C10000",
"l	c #2A0000",
"m	c #7C0000",
"n	c #D80000",
"o	c #BC0000",
"p	c #1D0000",
"q	c #DA0000",
"r	c #B70000",
"s	c #450000",
"t	c #D10000",
"u	c #E00000",
"v	c #BD0000",
"w	c #E90000",
"x	c #B20000",
"y	c #F10000",
"z	c #A30000",
"A	c #DC0000",
"B	c #C90000",
"C	c #E30000",
"D	c #C00000",
"E	c #ED0000",
"F	c #F40000",
"G	c #A70000",
"H	c #6B0000",
"I	c #550000",
"J	c #770000",
"K	c #DE0000",
"L	c #4A0000",
"M	c #810000",
"N	c #DF0000",
"O	c #CE0000",
"P	c #3A0000",
"Q	c #8B0000",
"R	c #2B0000",
"S	c #560000",
"T	c #DB0000",
"U	c #6A0000",
"                                             ...                ",
"                                            .+@#$               ",
"                                            %&**=.              ",
"                                            -;**>.              ",
"                                            .,')!               ",
"                                          .. ....               ",
"                                         ..   ...               ",
"                                        ..    . .               ",
"                                   .. ..      . ..              ",
"                                 .~{]..       .  .              ",
"                                 .^**+.       .  ..             ",
"                                 .&**/.       .   .             ",
"                                 .(&_:        .   .             ",
"                                ......        .    .            ",
"                              ..  ..          .    .            ",
"                             ..  ...          .     .           ",
"                            ..   . .          .     .           ",
"                       .<[..    .. .          .     ..          ",
"                      .}*|1.    .  .          .      .          ",
"                      .2**3.   ..  .          .      ..         ",
"                      .}*|1.   .   .          .       .         ",
"                     ...<[.    .   .          .       .         ",
"                    ......    .    .          .        .        ",
"                   .... .     .    .          .        .        ",
"                 ..  .  .    ..    .          .        ..       ",
"            ......  ..  .    .     .          .         .       ",
"           .4567.  ..   .   ..     .          .         ..      ",
"           .^**8.  .    .   .      .          .          .      ",
"           .9**/. ..    .  ..      .          .          .      ",
"           .0)ab ..     .  .       .          .           .     ",
"         ..  ..  .      .  .       .          .           .     ",
"        ..   .  ..      . .        .          .           ..    ",
"       ..    .  .       ...        .          .            .    ",
" ... ..     ....       ....       ...        ...           .... ",
".cdef.     .gh}i      .j9kl      .mnop      .,qr!          setc.",
".n**#.......u**v.......w**x.......y**z......-;**]..........#**n.",
".A**B.......C**D.......E**r.......F**G......%&**=..........B**A.",
".HAhI      .JKdL      .MNOP      .QueR      .+@3%          ShTU.",
" ....       ....       ...        ...        ...           .... "};		
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
FreeCADGui.addCommand('Assymetric',Assymetric_Command() ) 
