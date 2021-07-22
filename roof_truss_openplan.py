import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os
import framing, stud

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "OpenPlan" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class OpenPlan_Command:
	def GetResources(slf):
		#print 'Run getResources() for OpenPlan_Command' 
		icon_path = framing.getIconImage( "OpenPlanSketch" ) 	
		return {'MenuText': 'OpenPlan', 
			'ToolTip': 'Tooltip for OpenPlan command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'OpenPlan command is NOT active' 
			return False 
		else: 
			#print 'OpenPlan command IS active' 
			return True 
 
	def Activated(self): 
	
		newtruss = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "OpenPlanTruss")
		ViewProviderOpenPlan(newtruss.ViewObject)
		OpenPlan ( newtruss )		
		newtruss.Visibility = True
		FreeCAD.ActiveDocument.recompute()  
		FreeCADGui.SendMsgToActiveView("ViewFit")
	
 
		#print 'OpenPlanCommand activated' 
 
#		b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','OpenPlan') 
#		newsampleobject = OpenPlan(b) 
#		b.ViewObject.Proxy=0 
#		FreeCAD.ActiveDocument.recompute()
		
# 		print ( newsampleobject.Name )

#		print ( b.Name )
		
#		print ( FreeCAD.ActiveDocument.Objects.index( b ) )
		
#		framing.populateStuds( b, "Truss" )
#		print ( b.Name )
#		print ( b.Shape )
#		print ( b.Shape.Edges )
#		print ( b.Shape.Edge7 )

#		b.setExpression(  'Constraints[26]','.Shape.Edge7.Length / 2'  )

class OpenPlan:
	def __init__(self, obj):
		obj.addProperty("App::PropertyLength", "Rise", "Lumber Dimension", "The Rise of the roof.").Rise = "48 in"
		obj.addProperty("App::PropertyLength", "Run", "Lumber Dimension", "The Run of the roof").Run = "48 in"
		obj.Proxy = self		


		newsketch = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','OpenPlanSketch') 
		OpenPlanSketch(newsketch) 
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
				
class OpenPlanSketch: 
 
 
	def __init__(self, obj):
 
		#print 'The OpenPlan class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		expressionslist = []
		#expressions = []
 
		geometryList.append( Part.LineSegment( App.Vector (-1219.2, 0.0, 0.0), App.Vector (0.0, 1219.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 1219.2, 0.0), App.Vector (1219.2, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-1219.2, 0.0, 0.0), App.Vector (1219.2, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-880.035865568838, 0.0, 0.0), App.Vector (-880.035865568838, 339.1641344311621, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-589.102861730807, 630.097138269193, 0.0), App.Vector (589.102861730807, 630.097138269193, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (880.035865568838, 339.1641344311621, 0.0), App.Vector (880.035865568838, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-880.035865568838, 0.0, 0.0), App.Vector (-1049.617932784419, 169.58206721558105, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (880.035865568838, 0.0, 0.0), App.Vector (1049.617932784419, 169.58206721558108, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 630.097138269193, 0.0), App.Vector (0.0, 1219.2, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',1,1,0,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,-1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,1,0,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,1,2 ) )
#	constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,1,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,2,0 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,1,0 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,2,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',4 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',5,1,1 ) )
		constraintList.append( Sketcher.Constraint('Vertical',5 ) )
		constraintList.append( Sketcher.Constraint('Vertical',3 ) )
		constraintList.append( Sketcher.Constraint('Symmetric',3,2,5,1,-2))
		constraintList.append( Sketcher.Constraint('PointOnObject',0,2,-2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',6,1,3,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',6,2,0 ) )
		constraintList.append( Sketcher.Constraint('Coincident',7,1,5,2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',7,2,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',8,1,4 ) )
		constraintList.append( Sketcher.Constraint('Coincident',8,2,0,2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',8 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',5,2,2 ) )
		constraintList.append( Sketcher.Constraint('Perpendicular',6,0,0 ) )
		constraintList.append( Sketcher.Constraint('Perpendicular',1,0,7 ) )
		named_constraint = Sketcher.Constraint('DistanceX',0,1,-1,1,2438.4)
		named_constraint.Name = "Run"
		constraintList.append( named_constraint )
		named_constraint = Sketcher.Constraint('DistanceY',-1,1,0,2,1219.2)
		named_constraint.Name = "Rise"
		constraintList.append( named_constraint )
		
#		constraintList.append( Sketcher.Constraint('Equal',0,1))
		constraintList.append( Sketcher.Constraint('DistanceY',3,1,3,2,660.3999999999999))
		constraintList.append( Sketcher.Constraint('Equal',3,5))
		constraintList.append( Sketcher.Constraint('DistanceY',8,1,8,2,610.9333333333333))	

#		expressionslist.append( ['Constraints[26]','.Shape.Edges[4].Length / 2'] )
		expressionslist.append( ['Constraints[28]','.Constraints.Rise / 3'] )
	

		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )

		for label,expression in expressionslist:
			print ( label,expression )
			obj.setExpression( label, expression )
	
		obj.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000, 0.000000, 0.000000), FreeCAD.Rotation(0.500000, 0.500000, 0.500000, 0.500000))

	def onChanged(self, fp, prop):
		name = str(prop)
		newvalue = str(fp.getPropertyByName(str(prop)))
		#FreeCAD.Console.print.writeMessage('Changed property: ' + name + 'to ' + newvalue + '') 

	def execute(self,fp):	
		fp.recompute()
		print (' OpenPlan Class executed() ') 

class ViewProviderOpenPlan:
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
static char * OpenPlanSketch_xpm[] = {
"64 37 82 1",
" 	c None",
".	c #000000",
"+	c #580000",
"@	c #CB0000",
"#	c #DF0000",
"$	c #FF0000",
"%	c #DE0000",
"&	c #F20000",
"*	c #A70000",
"=	c #FE0000",
"-	c #A60000",
";	c #4C0000",
">	c #A10000",
",	c #D20000",
"'	c #A80000",
")	c #5B0000",
"!	c #CA0000",
"~	c #5A0000",
"{	c #7D0000",
"]	c #8C0000",
"^	c #9B0000",
"/	c #F10000",
"(	c #3B0000",
"_	c #E70000",
":	c #EB0000",
"<	c #460000",
"[	c #A50000",
"}	c #FD0000",
"|	c #470000",
"1	c #E60000",
"2	c #0E0000",
"3	c #5E0000",
"4	c #180000",
"5	c #080000",
"6	c #4B0000",
"7	c #E00000",
"8	c #290000",
"9	c #B10000",
"0	c #970000",
"a	c #B00000",
"b	c #990000",
"c	c #770000",
"d	c #980000",
"e	c #D80000",
"f	c #A00000",
"g	c #760000",
"h	c #BA0000",
"i	c #BB0000",
"j	c #F30000",
"k	c #F40000",
"l	c #D50000",
"m	c #D40000",
"n	c #B30000",
"o	c #3A0000",
"p	c #340000",
"q	c #5F0000",
"r	c #170000",
"s	c #670000",
"t	c #7F0000",
"u	c #F90000",
"v	c #500000",
"w	c #EF0000",
"x	c #E40000",
"y	c #2D0000",
"z	c #2E0000",
"A	c #E50000",
"B	c #EE0000",
"C	c #B20000",
"D	c #590000",
"E	c #BF0000",
"F	c #F70000",
"G	c #280000",
"H	c #950000",
"I	c #720000",
"J	c #730000",
"K	c #BE0000",
"L	c #D30000",
"M	c #790000",
"N	c #AA0000",
"O	c #D60000",
"P	c #A90000",
"Q	c #2C0000",
"                              ....                              ",
"                             .+@@+.                             ",
"                             .#$$%.                             ",
"                             .&$$&.                             ",
"                             .*==-.                             ",
"                             ..;;..                             ",
"                            .. .. ..                            ",
"                           ..  ..  ..                           ",
"                          ..   ..   ..                          ",
"                      .....   ....   .....                      ",
"                     .>,'.   .)!!~.   .',>.                     ",
"                    .{$$$].  .#$$#.  .]$$${.                    ",
"                    .^$$$*....&$$/....*$$$^.                    ",
"                     (_$:<   .[}}[.   |:$1(                     ",
"                    ..234.    .||.    .432..                    ",
"                    .                      .                    ",
"                   .                        .                   ",
"                  .                          .                  ",
"             .5)...                           ..)5.             ",
"             6:$78                            87$:6             ",
"            .9$$$0.                          .0$$$a.            ",
"            .b$$$c.                          .c$$$d.            ",
"             .9ef.                            .fe9.             ",
"            .....                              .....            ",
"        .. ..  .                                .  .. ..        ",
"       .cg..   .                                .   ..cc.       ",
"      .h$$h.   .                                .   .i$$h.      ",
"      .j$$k.   .                                .   .k$$j.      ",
"      .l$$l.   .                                .   .l$$m.      ",
"      .(nno.   .                                .   .onno.      ",
"     ..... ..  .                                .  .. .....     ",
" .pq..      ..rs5.                            .5sr..      ..qp. ",
".tu$!.      .vw$xy                            zA$Bv.      .!$ut.",
".l$$$+.......C$$$b............................b$$$9.......D$$$l.",
".E$$FG.     .H$$$I.                          .J$$$H.     .GF$$K.",
".yKLM.       .NOb.                            .bOP.       .MLKQ.",
" ....         ...                              ...         .... "};		
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
		
FreeCADGui.addCommand('OpenPlan',OpenPlan_Command() ) 
