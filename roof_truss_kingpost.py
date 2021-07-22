import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os
import framing, stud

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"

__command_name__ = "KingPost" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class KingPost_Command:
	def GetResources(slf):
	
		icon_path = framing.getIconImage( "kingposttruss" ) 	

		return {'MenuText': 'KingPost Truss', 
			'ToolTip': 'Add a KingPost style roof truss out to the construction.', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'KingPost command is NOT active' 
			return False 
		else: 
			#print 'KingPost command IS active' 
			return True 
 
	def Activated(self): 
	
		newtruss = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "KingPostTruss")
		ViewProviderKingPost(newtruss.ViewObject)
		KingPost ( newtruss )		
		newtruss.Visibility = True
		FreeCAD.ActiveDocument.recompute()  
		FreeCADGui.SendMsgToActiveView("ViewFit")	


class KingPost:
	def __init__(self, obj):
		obj.addProperty("App::PropertyLength", "Rise", "Lumber Dimension", "The Rise of the roof.").Rise = "48 in"
		obj.addProperty("App::PropertyLength", "Run", "Lumber Dimension", "The Run of the roof").Run = "48 in"
		obj.Proxy = self		


		newsketch = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','KingPostSketch') 
		KingPostSketch(newsketch) 
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


class KingPostSketch: 
 
	def __init__(self, obj):
 
		#print 'The KingPost class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 


		geometryList.append( Part.LineSegment( App.Vector (-2438.4, 0.0, 0.0), App.Vector (0.0, 1219.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 1219.2, 0.0), App.Vector (2438.4, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (2438.4, 0.0, 0.0), App.Vector (-2438.4, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 0.0, 0.0), App.Vector (0.0, 1219.2, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',0,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',1,2,-1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',1,2,2,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,0,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('Equal',0,1))
		constraintList.append( Sketcher.Constraint('Coincident',3,1,-1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,0,2 ) )
		constraintList.append( Sketcher.Constraint('Vertical',3 ) )

		named_constraint = Sketcher.Constraint('DistanceX',0,1,-1,1,2438.4)
		named_constraint.Name = "Run"
		constraintList.append( named_constraint )
		named_constraint = Sketcher.Constraint('DistanceY',-1,1,0,2,1219.2)
		named_constraint.Name = "Rise"
		constraintList.append( named_constraint )


		obj.addGeometry( geometryList, False)
		obj.addGeometry( constructionList, True)
		obj.addConstraint( constraintList )
		
		obj.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000, 0.000000, 0.000000), FreeCAD.Rotation(0.500000, 0.500000, 0.500000, 0.500000))
		
class ViewProviderKingPost:
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
static char * kingposttruss_xpm[] = {
"240 189 151 2",
"  	c None",
". 	c #000000",
"+ 	c #010000",
"@ 	c #230000",
"# 	c #3C0000",
"$ 	c #3D0000",
"% 	c #250000",
"& 	c #020000",
"* 	c #670000",
"= 	c #C30000",
"- 	c #E40000",
"; 	c #F90000",
"> 	c #FA0000",
", 	c #E60000",
"' 	c #C70000",
") 	c #710000",
"! 	c #140000",
"~ 	c #A30000",
"{ 	c #FF0000",
"] 	c #FC0000",
"^ 	c #B20000",
"/ 	c #180000",
"( 	c #A20000",
"_ 	c #FE0000",
": 	c #620000",
"< 	c #FB0000",
"[ 	c #FD0000",
"} 	c #7D0000",
"| 	c #CA0000",
"1 	c #D20000",
"2 	c #0B0000",
"3 	c #2C0000",
"4 	c #EB0000",
"5 	c #F10000",
"6 	c #430000",
"7 	c #560000",
"8 	c #F40000",
"9 	c #5E0000",
"0 	c #5A0000",
"a 	c #F60000",
"b 	c #5F0000",
"c 	c #350000",
"d 	c #ED0000",
"e 	c #4B0000",
"f 	c #D30000",
"g 	c #DA0000",
"h 	c #110000",
"i 	c #7A0000",
"j 	c #8E0000",
"k 	c #B60000",
"l 	c #C80000",
"m 	c #BB0000",
"n 	c #310000",
"o 	c #820000",
"p 	c #DE0000",
"q 	c #F50000",
"r 	c #E10000",
"s 	c #8D0000",
"t 	c #050000",
"u 	c #500000",
"v 	c #7E0000",
"w 	c #7F0000",
"x 	c #550000",
"y 	c #0D0000",
"z 	c #910000",
"A 	c #AC0000",
"B 	c #B50000",
"C 	c #1B0000",
"D 	c #990000",
"E 	c #B10000",
"F 	c #B30000",
"G 	c #9B0000",
"H 	c #660000",
"I 	c #770000",
"J 	c #A10000",
"K 	c #AD0000",
"L 	c #930000",
"M 	c #480000",
"N 	c #170000",
"O 	c #A50000",
"P 	c #E20000",
"Q 	c #030000",
"R 	c #300000",
"S 	c #F80000",
"T 	c #D00000",
"U 	c #460000",
"V 	c #630000",
"W 	c #B00000",
"X 	c #1F0000",
"Y 	c #260000",
"Z 	c #C90000",
"` 	c #E50000",
" .	c #EA0000",
"..	c #650000",
"+.	c #8A0000",
"@.	c #240000",
"#.	c #700000",
"$.	c #DD0000",
"%.	c #E90000",
"&.	c #2E0000",
"*.	c #540000",
"=.	c #F30000",
"-.	c #070000",
";.	c #DC0000",
">.	c #160000",
",.	c #A00000",
"'.	c #760000",
").	c #6F0000",
"!.	c #0E0000",
"~.	c #530000",
"{.	c #C00000",
"].	c #D80000",
"^.	c #920000",
"/.	c #450000",
"(.	c #F00000",
"_.	c #900000",
":.	c #5D0000",
"<.	c #F70000",
"[.	c #600000",
"}.	c #980000",
"|.	c #970000",
"1.	c #4D0000",
"2.	c #F20000",
"3.	c #940000",
"4.	c #790000",
"5.	c #190000",
"6.	c #E80000",
"7.	c #0A0000",
"8.	c #860000",
"9.	c #280000",
"0.	c #740000",
"a.	c #D90000",
"b.	c #120000",
"c.	c #DB0000",
"d.	c #750000",
"e.	c #9D0000",
"f.	c #090000",
"g.	c #DF0000",
"h.	c #8F0000",
"i.	c #440000",
"j.	c #060000",
"k.	c #6E0000",
"l.	c #AE0000",
"m.	c #9A0000",
"n.	c #200000",
"o.	c #850000",
"p.	c #BD0000",
"q.	c #C10000",
"r.	c #270000",
"s.	c #410000",
"t.	c #D10000",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                            . . . . . .                                                                                                                                                                                                                                         ",
"                                                                                                                                                                                                                                      . . . . . . . . . . . .                                                                                                                                                                                                                                   ",
"                                                                                                                                                                                                                                    . . . . . . . . . . . . . .                                                                                                                                                                                                                                 ",
"                                                                                                                                                                                                                                  . . . . . . . . . . . . . . . . .                                                                                                                                                                                                                             ",
"                                                                                                                                                                                                                                . . . . . . + @ # $ % & . . . . . .                                                                                                                                                                                                                             ",
"                                                                                                                                                                                                                              . . . . . . * = - ; > , ' ) . . . . . .                                                                                                                                                                                                                           ",
"                                                                                                                                                                                                                            . . . . . ! ~ > { { { { { { ] ^ / . . . . .                                                                                                                                                                                                                         ",
"                                                                                                                                                                                                                            . . . . . ( ] { { { { { { { { _ ^ + . . . .                                                                                                                                                                                                                         ",
"                                                                                                                                                                                                                            . . . . : < { { { { { { { { { { [ } . . . . .                                                                                                                                                                                                                       ",
"                                                                                                                                                                                                                          . . . . . | { { { { { { { { { { { { 1 2 . . . .                                                                                                                                                                                                                       ",
"                                                                                                                                                                                                                          . . . . 3 4 { { { { { { { { { { { { 5 6 . . . .                                                                                                                                                                                                                       ",
"                                                                                                                                                                                                                          . . . . 7 8 { { { { { { { { { { { { { 9 . . . .                                                                                                                                                                                                                       ",
"                                                                                                                                                                                                                          . . . . 0 a { { { { { { { { { { { { { b . . . .                                                                                                                                                                                                                       ",
"                                                                                                                                                                                                                          . . . . c d { { { { { { { { { { { { 8 e . . . .                                                                                                                                                                                                                       ",
"                                                                                                                                                                                                                          . . . . + f { { { { { { { { { { { { g h . . . .                                                                                                                                                                                                                       ",
"                                                                                                                                                                                                                            . . . . i _ { { { { { { { { { { { j . . . . .                                                                                                                                                                                                                       ",
"                                                                                                                                                                                                                            . . . . . k _ { { { { { { { { { l + . . . .                                                                                                                                                                                                                         ",
"                                                                                                                                                                                                                            . . . . . 3 m { { { { { { { { ' n . . . . .                                                                                                                                                                                                                         ",
"                                                                                                                                                                                                                          . . . . . . . . o p 8 _ _ q r s + . . . . . . .                                                                                                                                                                                                                       ",
"                                                                                                                                                                                                                        . . . . . . . . . . t u v w x y . . . . . . . . . . .                                                                                                                                                                                                                   ",
"                                                                                                                                                                                                                    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                                                                                 ",
"                                                                                                                                                                                                                  . . . . . . . .   . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                                                                               ",
"                                                                                                                                                                                                                . . . . . . . .       . . . . . . . . . . . .         . . . . . . .                                                                                                                                                                                                             ",
"                                                                                                                                                                                                            . . . . . . . .               . . . . . . . .               . . . . . . . .                                                                                                                                                                                                         ",
"                                                                                                                                                                                                          . . . . . . . .                     . . . .                     . . . . . . . .                                                                                                                                                                                                       ",
"                                                                                                                                                                                                        . . . . . . . .                       . . . .                         . . . . . . .                                                                                                                                                                                                     ",
"                                                                                                                                                                                                      . . . . . . .                           . . . .                           . . . . . . . .                                                                                                                                                                                                 ",
"                                                                                                                                                                                                  . . . . . . . .                             . . . .                             . . . . . . . .                                                                                                                                                                                               ",
"                                                                                                                                                                                                . . . . . . . .                               . . . .                               . . . . . . . .                                                                                                                                                                                             ",
"                                                                                                                                                                                              . . . . . . .                                   . . . .                                   . . . . . . . .                                                                                                                                                                                         ",
"                                                                                                                                                                                          . . . . . . . .                                     . . . .                                     . . . . . . . .                                                                                                                                                                                       ",
"                                                                                                                                                                                        . . . . . . . .                                       . . . .                                       . . . . . . . .                                                                                                                                                                                     ",
"                                                                                                                                                                                      . . . . . . . .                                         . . . .                                           . . . . . . .                                                                                                                                                                                   ",
"                                                                                                                                                                                  . . . . . . . .                                             . . . .                                             . . . . . . . .                                                                                                                                                                               ",
"                                                                                                                                                                                . . . . . . . .                                               . . . .                                               . . . . . . . .                                                                                                                                                                             ",
"                                                                                                                                                                              . . . . . . . .                                                 . . . .                                                 . . . . . . . .                                                                                                                                                                           ",
"                                                                                                                                                                            . . . . . . .                                                     . . . .                                                     . . . . . . . .                                                                                                                                                                       ",
"                                                                                                                                                                        . . . . . . . .                                                       . . . .                                                       . . . . . . . .                                                                                                                                                                     ",
"                                                                                                                                                                      . . . . . . . .                                                         . . . .                                                         . . . . . . . .                                                                                                                                                                   ",
"                                                                                                                                                                    . . . . . . . .                                                           . . . .                                                             . . . . . . .                                                                                                                                                                 ",
"                                                                                                                                                                . . . . . . . .                                                               . . . .                                                               . . . . . . . .                                                                                                                                                             ",
"                                                                                                                                                              . . . . . . . .                                                                 . . . .                                                                 . . . . . . . .                                                                                                                                                           ",
"                                                                                                                                                            . . . . . . . .                                                                   . . . .                                                                   . . . . . . . .                                                                                                                                                         ",
"                                                                                                                                                          . . . . . . .                                                                       . . . .                                                                       . . . . . . . .                                                                                                                                                     ",
"                                                                                                                                                      . . . . . . . .                                                                         . . . .                                                                         . . . . . . . .                                                                                                                                                   ",
"                                                                                                                                                    . . . . . . . .                                                                           . . . .                                                                           . . . . . . . .                                                                                                                                                 ",
"                                                                                                                                                  . . . . . . .                                                                               . . . .                                                                               . . . . . . .                                                                                                                                               ",
"                                                                                                                                              . . . . . . . .                                                                                 . . . .                                                                                 . . . . . . . .                                                                                                                                           ",
"                                                                                                                                            . . . . . . . .                                                                                   . . . .                                                                                   . . . . . . . .                                                                                                                                         ",
"                                                                                                                                          . . . . . . . .                                                                                     . . . .                                                                                     . . . . . . . .                                                                                                                                       ",
"                                                                                                                                      . . . . . . . .                                                                                         . . . .                                                                                         . . . . . . . .                                                                                                                                   ",
"                                                                                                                                    . . . . . . . .                                                                                           . . . .                                                                                           . . . . . . . .                                                                                                                                 ",
"                                                                                                                                  . . . . . . . .                                                                                             . . . .                                                                                             . . . . . . . .                                                                                                                               ",
"                                                                                                                                . . . . . . .                                                                                                 . . . .                                                                                                 . . . . . . .                                                                                                                             ",
"                                                                                                                            . . . . . . . .                                                                                                   . . . .                                                                                                   . . . . . . . .                                                                                                                         ",
"                                                                                                                          . . . . . . . .                                                                                                     . . . .                                                                                                     . . . . . . . .                                                                                                                       ",
"                                                                                                                        . . . . . . . .                                                                                                       . . . .                                                                                                         . . . . . . .                                                                                                                     ",
"                                                                                                                    . . . . . . . .                                                                                                           . . . .                                                                                                           . . . . . . . .                                                                                                                 ",
"                                                                                                                  . . . . . . . .                                                                                                             . . . .                                                                                                             . . . . . . . .                                                                                                               ",
"                                                                                                                . . . . . . . .                                                                                                               . . . .                                                                                                               . . . . . . . .                                                                                                             ",
"                                                                                                              . . . . . . .                                                                                                                   . . . .                                                                                                                   . . . . . . . .                                                                                                         ",
"                                                                                                          . . . . . . . .                                                                                                                     . . . .                                                                                                                     . . . . . . . .                                                                                                       ",
"                                                                                                        . . . . . . . .                                                                                                                       . . . .                                                                                                                       . . . . . . . .                                                                                                     ",
"                                                                                                      . . . . . . . .                                                                                                                         . . . .                                                                                                                           . . . . . . .                                                                                                   ",
"                                                                                                  . . . . . . . .                                                                                                                             . . . .                                                                                                                             . . . . . . . .                                                                                               ",
"                                                                                                . . . . . . . .                                                                                                                               . . . .                                                                                                                               . . . . . . . .                                                                                             ",
"                                                                                              . . . . . . . .                                                                                                                                 . . . .                                                                                                                                   . . . . . . .                                                                                           ",
"                                                                                            . . . . . . .                                                                                                                                     . . . .                                                                                                                                     . . . . . . . .                                                                                       ",
"                                                                                        . . . . . . . .                                                                                                                                       . . . .                                                                                                                                       . . . . . . . .                                                                                     ",
"                                                                                      . . . . . . . .                                                                                                                                         . . . .                                                                                                                                         . . . . . . . .                                                                                   ",
"                                                                                    . . . . . . .                                                                                                                                             . . . .                                                                                                                                             . . . . . . .                                                                                 ",
"                                                                                . . . . . . . .                                                                                                                                               . . . .                                                                                                                                               . . . . . . . .                                                                             ",
"                                                                              . . . . . . . .                                                                                                                                                 . . . .                                                                                                                                                 . . . . . . . .                                                                           ",
"                                              . . . . . . . . .             . . . . . . . .                                                                                                                                               . . . . . . . .                                                                                                                                                 . . . . . . .             . . . . . . . . .                                           ",
"                                          . . . . . . . . . . . . .     . . . . . . . .                                                                                                                                               . . . . . . . . . . . .                                                                                                                                               . . . . . . . .     . . . . . . . . . . . . .                                       ",
"                                      . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                             . . . . . . . . . . . . . . . .                                                                                                                                             . . . . . . . . . . . . . . . . . . . . . . . .                                   ",
"                                    . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                             . . . . . . . . . . . . . . . . . .                                                                                                                                             . . . . . . . . . . . . . . . . . . . . . . . .                                 ",
"                                    . . . . . . $ z A B ~ v C . . . . . . . . .                                                                                                                                               . . . . . . + 9 D E F G H t . . . . . .                                                                                                                                               . . . . . . . . . h I J B K L M . . . . . .                                 ",
"                                  . . . . . N O 5 { { { { ] P I Q . . . . . .                                                                                                                                                 . . . . . R ' S { { { { ; T U . . . . .                                                                                                                                                 . . . . . . . V p < { { { { 8 W X . . . . .                               ",
"                                . . . . . Y Z { { { { { { { { ; L . . . . .                                                                                                                                                 . . . . . 7 ` { { { { { { { {  .... . . . .                                                                                                                                                 . . . . . +.a { { { { { { { { 1 @.. . . . .                             ",
"                                . . . . + ^ _ { { { { { { { { { > #.. . . . .                                                                                                                                               . . . . ! $.{ { { { { { { { { { %.&.. . . .                                                                                                                                               . . . . . *.=.{ { { { { { { { { { Z -.. . . .                             ",
"                                . . . . ..> { { { { { { { { { { { ;.>.. . . .                                                                                                                                               . . . . ,.{ { { { { { { { { { { { E . . . . .                                                                                                                                             . . . . + f { { { { { { { { { { { > '.. . . .                             ",
"                                . . . . E { { { { { { { { { { { { > ).. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . !.r { { { { { { { { { { { { - % . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ~.S { { { { { { { { { { { { {.. . . . .                           ",
"                              . . . . t ].{ { { { { { { { { { { { { ^.. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . /.(.{ { { { { { { { { { { { < 7 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . _.{ { { { { { { { { { { { { g . . . . .                           ",
"                              . . . . h $.{ { { { { { { { { { { { { ~ . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . :.<.{ { { { { { { { { { { { { [.. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . }.{ { { { { { { { { { { { { ` . . . . .                           ",
"                              . . . . -.g { { { { { { { { { { { { { |.. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1.2.{ { { { { { { { { { { { [ 0 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3.{ { { { { { { { { { { { { $.. . . . .                           ",
"                              . . . . . m { { { { { { { { { { { { [ 4.. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5., { { { { { { { { { { { { 6.n . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ..> { { { { { { { { { { { { Z . . . . .                           ",
"                                . . . . I [ { { { { { { { { { { { ` Y . . . .                                                                                                                                             . . . . . ^ { { { { { { { { { { { { {.+ . . . .                                                                                                                                             . . . . 7.p { { { { { { { { { { { ] 8.. . . .                             ",
"                                . . . . Q | { { { { { { { { { { [ j . . . . .                                                                                                                                               . . . . 9.4 { { { { { { { { { { 8 1.. . . .                                                                                                                                               . . . . . 0.< { { { { { { { { { { a.b.. . . .                             ",
"                                . . . . . # c.{ { { { { { { { [ ^ . . . . .                                                                                                                                                 . . . . . d.5 { { { { { { { { a v . . . . .                                                                                                                                                 . . . . t J [ { { { { { { { { - 1.. . . . .                             ",
"                                  . . . . . &.| > { { { { { 2.e.f.. . . . .                                                                                                                                                   . . . . . V g.[ { { { { [ ` 0.+ . . . .                                                                                                                                                   . . . . . Q h.d { { { { { < 1 i.. . . . .                               ",
"                                  . . . . . . j.k.l.T f | m.e . . . . . .                                                                                                                                                     . . . . . . n.o.p.1 1 q.+.r.. . . . . .                                                                                                                                                     . . . . . . s.|.l f t.F d.j.. . . . . .                               ",
"                                    . . . . . . . . . . . . . . . . . .                                                                                                                                                         . . . . . . . . . . . . . . . . . .                                                                                                                                                         . . . . . . . . . . . . . . . . . .                                 ",
"                                      . . . . . . . . . . . . . . . .                                                                                                                                                             . . . . . . . . . . . . . . . .                                                                                                                                                             . . . . . . . . . . . . . . . .                                   ",
"                                          . . . . . . . . . . . . .                                                                                                                                                                 . . . . . . . . . . . . . .                                                                                                                                                                 . . . . . . . . . . . . . .                                     ",
"                                            . . . . . . . . . .                                                                                                                                                                         . . . . . . . . . .                                                                                                                                                                         . . . . . . . . . .                                         ",
"                                                    . . .                                                                                                                                                                                       . .                                                                                                                                                                                       . . .                                                 ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ",
"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                "};"""

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


FreeCADGui.addCommand('KingPost',KingPost_Command() ) 
