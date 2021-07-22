import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os
import framing, stud

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "MonoB" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class MonoB_Command:
	def GetResources(slf):
		icon_path = framing.getIconImage( "monobtruss" ) 	

		return {'MenuText': 'MonoB Truss', 
			'ToolTip': 'Add a MonoB style roof truss out to the construction.', 
			'Pixmap' : str(icon_path) } 

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'MonoB command is NOT active' 
			return False 
		else: 
			#print 'MonoB command IS active' 
			return True 
 
	def Activated(self): 
 
		#print 'MonoBCommand activated'
		
		
		newtruss = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "MonoBTruss")
		ViewProviderMonoB(newtruss.ViewObject)
		MonoB ( newtruss )		
		newtruss.Visibility = True
		FreeCAD.ActiveDocument.recompute()  
		FreeCADGui.SendMsgToActiveView("ViewFit") 
 
#		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','MonoBTruss') 
#		b.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000,0.000000,0.000000),FreeCAD.Rotation(0,0,0,0))
		
#		newsketch = MonoB(b) 
#		b.ViewObject.Proxy=0 
		
#		FreeCAD.ActiveDocument.recompute()  

#		framing.populateStuds( b, "Truss" )

class MonoB:
	def __init__(self, obj):
		obj.addProperty("App::PropertyLength", "Rise", "Lumber Dimension", "The Rise of the roof.").Rise = "48 in"
		obj.addProperty("App::PropertyLength", "Run", "Lumber Dimension", "The Run of the roof").Run = "48 in"
		obj.Proxy = self		


		newsketch = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','MonoBSketch') 
		MonoBSketch(newsketch) 
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

		
		
	
class MonoBSketch: 
 
 
	def __init__(self, obj):
 
		#print 'The MonoB class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (0.0, 1219.2, 0.0), App.Vector (0.0, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 7.085782418561855e-30, 0.0), App.Vector (1219.2, 7.085782418561855e-30, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (1219.2, 7.085782418561855e-30, 0.0), App.Vector (0.0, 1219.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 7.085782418561855e-30, 0.0), App.Vector (365.5288121208204, 853.6711878791797, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (365.5288121208204, 853.6711878791797, 0.0), App.Vector (640.3434918265771, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (640.3434918265771, 0.0, 0.0), App.Vector (813.89068, 405.30932, 0.0)))

		constructionList.append( Part.LineSegment( App.Vector (0.0, 1219.2, 0.0), App.Vector (609.5999999999999, 812.8, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (609.5999999999999, 812.8, 0.0), App.Vector (1219.2, 406.4, 0.0)))
		constructionList.append( Part.LineSegment( App.Vector (1219.2, 406.4, 0.0), App.Vector (1828.8, 0.0, 0.0)))

		constraintList.append( Sketcher.Constraint('Vertical',0 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,1,1,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,1,0,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,2,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,1,3,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,2,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,1,4,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',5,2,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,1,0,2 ) )
		named_constraint = Sketcher.Constraint('DistanceY',0,2,0,1,1219.2)
		named_constraint.Name = "Rise"
		constraintList.append( named_constraint )
		constraintList.append( Sketcher.Constraint('Coincident',0,2,-1,1 ) )
		constraintList.append( Sketcher.Constraint('Parallel',5,3))
		named_constraint = Sketcher.Constraint('DistanceX',1,1,1,2,1828.8)
		named_constraint.Name = "Run"
		constraintList.append( named_constraint )
		
		constraintList.append( Sketcher.Constraint('Coincident',7,1,6,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,1,7,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Equal',6,7))
		constraintList.append( Sketcher.Constraint('Equal',7,8))
		constraintList.append( Sketcher.Constraint('Coincident',6,2,3,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,2,7,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,2,1,2 ) )

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
		print (' MonoB Class executed() ') 
		
class ViewProviderMonoB:
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
static char * monobtruss_xpm[] = {
"64 64 63 1",
" 	c None",
".	c #000000",
"+	c #A10000",
"@	c #D10000",
"#	c #7E0000",
"$	c #640000",
"%	c #FF0000",
"&	c #F20000",
"*	c #A00000",
"=	c #D20000",
"-	c #7D0000",
";	c #720000",
">	c #B00000",
",	c #630000",
"'	c #3D0000",
")	c #F80000",
"!	c #F00000",
"~	c #050000",
"{	c #590000",
"]	c #FD0000",
"^	c #230000",
"/	c #B90000",
"(	c #EB0000",
"_	c #A80000",
":	c #1D0000",
"<	c #770000",
"[	c #330000",
"}	c #DB0000",
"|	c #EC0000",
"1	c #270000",
"2	c #130000",
"3	c #730000",
"4	c #CB0000",
"5	c #E10000",
"6	c #0D0000",
"7	c #490000",
"8	c #090000",
"9	c #670000",
"0	c #DD0000",
"a	c #CF0000",
"b	c #080000",
"c	c #BF0000",
"d	c #E20000",
"e	c #870000",
"f	c #B50000",
"g	c #E40000",
"h	c #930000",
"i	c #D70000",
"j	c #860000",
"k	c #6D0000",
"l	c #F60000",
"m	c #CA0000",
"n	c #9B0000",
"o	c #740000",
"p	c #5C0000",
"q	c #BB0000",
"r	c #A90000",
"s	c #940000",
"t	c #C10000",
"u	c #5D0000",
"v	c #890000",
"w	c #C40000",
"x	c #690000",
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
"                                                         ...    ",
"                                                        .+@#.   ",
"                                                        $%%&.   ",
"                                                        $%%&.   ",
"                                                       ..*=-.   ",
"                                                      .. ...    ",
"                                                    ..    .     ",
"                                                   ..     .     ",
"                                                  ..      .     ",
"                                                ..        .     ",
"                                               ..         .     ",
"                                          .  ..           .     ",
"                                        .;>,..            .     ",
"                                        ')%!~             .     ",
"                                        {%%]^             .     ",
"                                        ./(_.             .     ",
"                                      .......             .     ",
"                                     .. ..  .             .     ",
"                                   ..   .   ..            .     ",
"                                  ..    .    .            .     ",
"                                ..     .      .           .     ",
"                               ..      .      ..          .     ",
"                              ..      .        .          .     ",
"                            ..        .         .         .     ",
"                           ..        ..         .         .     ",
"                      :<[..          .           .        .     ",
"                     .}%|1           .           ..       .     ",
"                     2%%%3          .             .       .     ",
"                     .4%56          .              .      .     ",
"                    ...78.         .               ..     .     ",
"                  ..     .         .                .     .     ",
"                 ..      ..       ..                 .    .     ",
"               ..         .       .                  .    .     ",
"              ..           .     ..                   .   .     ",
"             ..            ..    .                    ..  .     ",
"           ..               .    .                     .  .     ",
"          ..                 .  .                       . .     ",
"    ... ..                   ....                       ....    ",
"    90a[.                    bcde.                      .fgh.   ",
"   .i%%_.....................j%%(.......................k%%l.   ",
"   .m%%n.                   .o%%5.                     .p]%|.   ",
"    'qr.                     .stu.                      .vwx.   ",
"     ..                       ..                         ..     ",
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
		"""                                                                                                                                                                                                                                                                                                                                                                                                                                                 "};"""

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
		
		
FreeCADGui.addCommand('MonoB',MonoB_Command() ) 
