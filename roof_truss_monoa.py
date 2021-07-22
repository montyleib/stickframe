import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os
import framing, stud

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "MonoA" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class MonoA_Command:
	def GetResources(slf):
	
		icon_path = framing.getIconImage( "monoatruss" ) 	

		return {'MenuText': 'MonoA Truss', 
			'ToolTip': 'Add a MonoA style roof truss out to the construction.', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'MonoA command is NOT active' 
			return False 
		else: 
			#print 'MonoA command IS active' 
			return True 
 
	def Activated(self): 
 
		newtruss = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "MonoATruss")
		ViewProviderMonoA(newtruss.ViewObject)
		MonoA ( newtruss )		
		newtruss.Visibility = True
		FreeCAD.ActiveDocument.recompute()  
		FreeCADGui.SendMsgToActiveView("ViewFit")
		
#		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','MonoATruss') 
#		newsketch = MonoA(b) 
		
#		b.ViewObject.Proxy=0 
#		FreeCAD.ActiveDocument.recompute()  
	
#		framing.populateStuds( b, "Truss" )
class MonoA: 
	def __init__(self, obj):
		obj.addProperty("App::PropertyLength", "Rise", "Lumber Dimension", "The Rise of the roof.").Rise = "48 in"
		obj.addProperty("App::PropertyLength", "Run", "Lumber Dimension", "The Run of the roof").Run = "48 in"
		obj.Proxy = self		


		newsketch = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','MonoASketch') 
		MonoASketch(newsketch) 
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
		
class MonoASketch: 
 
 
	def __init__(self, obj):
 
		#print 'The MonoA class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (0.0, 0.0, 0.0), App.Vector (0.0, 1219.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (1219.2, 0.0, 0.0), App.Vector (0.0, 1219.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 0.0, 0.0), App.Vector (609.6, 609.6, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (609.6, 0.0, 0.0), App.Vector (609.6, 609.6, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 0.0, 0.0), App.Vector (1219.2, 0.0, 0.0)))


		constraintList.append( Sketcher.Constraint('Vertical',0 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,1,-1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,0,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,2,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',0,1,-1,1 ) )
		named_constraint = Sketcher.Constraint('DistanceY',0,1,0,2,1219.2)
		named_constraint.Name = "Rise"
		constraintList.append( named_constraint )
		constraintList.append( Sketcher.Constraint('Symmetric',0,1,1,1,3))
		constraintList.append( Sketcher.Constraint('PointOnObject',2,2,1 ) )
		named_constraint = Sketcher.Constraint('DistanceX',4,1,4,2,2438.4)
		named_constraint.Name = "Run"
		constraintList.append( named_constraint )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,1,4 ) )


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
		print (' MonoA Class executed() ') 

class ViewProviderMonoA:
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
static char * monoatruss_xpm[] = {
"64 39 56 1",
" 	c None",
".	c #000000",
"+	c #160000",
"@	c #9C0000",
"#	c #AF0000",
"$	c #540000",
"%	c #CF0000",
"&	c #FF0000",
"*	c #F60000",
"=	c #370000",
"-	c #AE0000",
";	c #1A0000",
">	c #990000",
",	c #920000",
"'	c #F50000",
")	c #FE0000",
"!	c #CB0000",
"~	c #0F0000",
"{	c #200000",
"]	c #730000",
"^	c #DD0000",
"/	c #E50000",
"(	c #A30000",
"_	c #F10000",
":	c #7D0000",
"<	c #500000",
"[	c #A90000",
"}	c #E70000",
"|	c #FB0000",
"1	c #670000",
"2	c #510000",
"3	c #C30000",
"4	c #7F0000",
"5	c #110000",
"6	c #1F0000",
"7	c #FD0000",
"8	c #C60000",
"9	c #020000",
"0	c #930000",
"a	c #100000",
"b	c #9A0000",
"c	c #190000",
"d	c #2C0000",
"e	c #F80000",
"f	c #910000",
"g	c #470000",
"h	c #A70000",
"i	c #550000",
"j	c #CE0000",
"k	c #D50000",
"l	c #F30000",
"m	c #4A0000",
"n	c #150000",
"o	c #1E0000",
"p	c #9E0000",
"q	c #4E0000",
"                                                          ....  ",
"                                                         .+@#$. ",
"                                                         .%&&*$.",
"                                                        .=&&&&-.",
"                                                        .;*&&&>.",
"                                                        ..,')!~.",
"                                                      .....~{.. ",
"                                                    ...    ..   ",
"                                                  ...      ..   ",
"                                                ....       ..   ",
"                                               ...         ..   ",
"                                             ...           ..   ",
"                                           ...             ..   ",
"                                         ...               ..   ",
"                                       ....                ..   ",
"                                      ...                  ..   ",
"                              ..... ...                    ..   ",
"                             .]^/(...                      ..   ",
"                            .+_&&&:.                       ..   ",
"                            .<&&&&[.                       ..   ",
"                            ..}&&|1.                       ..   ",
"                           ...23%4...                      ..   ",
"                         ...  ....  ...                    ..   ",
"                       ...     ..     ...                  ..   ",
"                     ....      ..       ...                ..   ",
"                    ...        ..        ....              ..   ",
"                  ...          ..          ...             ..   ",
"                ...            ..            ...           ..   ",
"              ...              ..              ...         ..   ",
"            ....               ..                ...       ..   ",
"           ...                 ..                 ...      ..   ",
"   ..    ...                   ..                   ...    ..   ",
" ..{~.....                    .56..                   .....~{.. ",
".5!)',..                     .>*789.                    ..0')!a.",
".b&&&*c......................de&&&f......................;*&&&>.",
".-&&&&=......................g&&&&h......................=&&&&-.",
".i*&&j.                      .k&&lm.                     .%&&*$.",
" .$#@n.                      .op-q.                      .+@#$. ",
"  ....                        ....                        ....  "};
		"""                                                                                                                                                                                                                                                                                                                                                                                                                                                                  "};"""

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
		
		
FreeCADGui.addCommand('MonoA',MonoA_Command() ) 
