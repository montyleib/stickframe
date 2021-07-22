import Sketcher
import FreeCAD
import FreeCAD,FreeCADGui,Part, Draft
import os

import framing, stud

__title__="FreeCAD Stick Framers Toolkit"
__author__ = "Paul Randall"
__url = "http://www.mathcodeprint.com/"
__command_name__ = "QueenPost" #Name of the command to appear in Toolbar
__command_group__= "" #Name of Toolbar to assign the command

class QueenPost_Command:
	def GetResources(slf):
		#print 'Run getResources() for QueenPost_Command' 
		
		icon_path = framing.getIconImage( "queenposttruss" ) 	

		return {'MenuText': 'QueenPost', 
			'ToolTip': 'Tooltip for QueenPost command', 
			'Pixmap' : str(icon_path) }  

	def IsActive(self): 
		if FreeCAD.ActiveDocument == None: 
			#print 'QueenPost command is NOT active' 
			return False 
		else: 
			#print 'QueenPost command IS active' 
			return True 
 
	def Activated(self): 
 
		newtruss = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "QueenPostTruss")
		ViewProviderQueenPost(newtruss.ViewObject)
		QueenPost ( newtruss )		
		newtruss.Visibility = True
		FreeCAD.ActiveDocument.recompute()  
		FreeCADGui.SendMsgToActiveView("ViewFit")	
 
		#print 'QueenPostCommand activated' 
 
		#b=FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','QueenPostTruss') 
		#b.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000,0.000000,0.000000),FreeCAD.Rotation(0,0,0,0))
		#newsketch = QueenPostSketch(b) 
			
		#b.ViewObject.Proxy=0 
		#FreeCAD.ActiveDocument.recompute() 

		#framing.populateStuds( b, "Truss" )
		
		
		
class QueenPost:
	def __init__(self, obj):
		obj.addProperty("App::PropertyLength", "Rise", "Lumber Dimension", "The Rise of the roof.").Rise = "48 in"
		obj.addProperty("App::PropertyLength", "Run", "Lumber Dimension", "The Run of the roof").Run = "48 in"
		obj.Proxy = self		


		newsketch = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObjectPython','QueenPostSketch') 
		QueenPostSketch(newsketch) 
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
			
			
class QueenPostSketch: 
 
 
	def __init__(self, obj):
 
		#print 'The QueenPost class has been instantiated init' 
		obj.Proxy = self
		App = FreeCAD
		tmpCircle = None
		geometryList = [] 
		constructionList = [] 
		constraintList = [] 
 
		geometryList.append( Part.LineSegment( App.Vector (-1219.2, 0.0, 0.0), App.Vector (0.0, 1219.2, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 1219.2, 0.0), App.Vector (1219.2, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (1219.2, 0.0, 0.0), App.Vector (-1219.2, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (609.5998423997069, 609.6001576002932, 0.0), App.Vector (0.0, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (-609.6, 609.6, 0.0), App.Vector (0.0, 0.0, 0.0)))
		geometryList.append( Part.LineSegment( App.Vector (0.0, 0.0, 0.0), App.Vector (0.0, 1219.2, 0.0)))


		constraintList.append( Sketcher.Constraint('Coincident',0,2,1,1 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,1,1,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',2,2,0,1 ) )
		constraintList.append( Sketcher.Constraint('Horizontal',2 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,2,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',4,2,3,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,1,3,2 ) )
		constraintList.append( Sketcher.Constraint('Coincident',5,2,0,2 ) )
		constraintList.append( Sketcher.Constraint('Equal',3,4))
		constraintList.append( Sketcher.Constraint('Vertical',5 ) )
		constraintList.append( Sketcher.Constraint('Equal',0,1))
		named_constraint = Sketcher.Constraint('DistanceX',0,1,3,2,1219.2)
		named_constraint.Name = "Run"
		constraintList.append( named_constraint )
		named_constraint = Sketcher.Constraint('DistanceY',5,1,5,2,1219.2)
		named_constraint.Name = "Rise"
		constraintList.append( named_constraint )
		constraintList.append( Sketcher.Constraint('PointOnObject',3,1,1 ) )
		constraintList.append( Sketcher.Constraint('PointOnObject',4,1,0 ) )
		constraintList.append( Sketcher.Constraint('Perpendicular',0,0,4 ) )
		constraintList.append( Sketcher.Constraint('Coincident',3,2,-1,1 ) )

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
		print (' QueenPostSKetch Class executed() ') 
		
		
class ViewProviderQueenPost:
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
static char * queenposttruss_XPM[] = {
"128 73 99 2",
"  	c None",
". 	c #000000",
"+ 	c #430000",
"@ 	c #8F0000",
"# 	c #A70000",
"$ 	c #F90000",
"% 	c #FF0000",
"& 	c #A60000",
"* 	c #900000",
"= 	c #DE0000",
"- 	c #090000",
"; 	c #EF0000",
"> 	c #080000",
", 	c #E50000",
"' 	c #A90000",
") 	c #010000",
"! 	c #CA0000",
"~ 	c #7D0000",
"{ 	c #B90000",
"] 	c #310000",
"^ 	c #8E0000",
"/ 	c #A00000",
"( 	c #690000",
"_ 	c #6A0000",
": 	c #A10000",
"< 	c #820000",
"[ 	c #F20000",
"} 	c #FE0000",
"| 	c #D00000",
"1 	c #2A0000",
"2 	c #830000",
"3 	c #580000",
"4 	c #F80000",
"5 	c #C60000",
"6 	c #570000",
"7 	c #B80000",
"8 	c #FB0000",
"9 	c #370000",
"0 	c #CD0000",
"a 	c #5F0000",
"b 	c #CC0000",
"c 	c #BE0000",
"d 	c #FD0000",
"e 	c #3F0000",
"f 	c #BD0000",
"g 	c #680000",
"h 	c #FC0000",
"i 	c #D10000",
"j 	c #D20000",
"k 	c #670000",
"l 	c #9B0000",
"m 	c #FA0000",
"n 	c #E00000",
"o 	c #420000",
"p 	c #E10000",
"q 	c #520000",
"r 	c #B40000",
"s 	c #8B0000",
"t 	c #140000",
"u 	c #150000",
"v 	c #8C0000",
"w 	c #360000",
"x 	c #C20000",
"y 	c #A80000",
"z 	c #480000",
"A 	c #7E0000",
"B 	c #490000",
"C 	c #350000",
"D 	c #6C0000",
"E 	c #F00000",
"F 	c #F60000",
"G 	c #870000",
"H 	c #030000",
"I 	c #F70000",
"J 	c #100000",
"K 	c #EA0000",
"L 	c #F50000",
"M 	c #3E0000",
"N 	c #AA0000",
"O 	c #0F0000",
"P 	c #9D0000",
"Q 	c #BA0000",
"R 	c #9C0000",
"S 	c #6F0000",
"T 	c #920000",
"U 	c #930000",
"V 	c #6E0000",
"W 	c #DB0000",
"X 	c #210000",
"Y 	c #220000",
"Z 	c #DA0000",
"` 	c #450000",
" .	c #610000",
"..	c #440000",
"+.	c #9A0000",
"@.	c #760000",
"#.	c #040000",
"$.	c #770000",
"%.	c #6B0000",
"                                                                                                                          . . . . . .                                                                                                                           ",
"                                                                                                                        . . . . . . . .                                                                                                                         ",
"                                                                                                                      . . . + @ @ + . . .                                                                                                                       ",
"                                                                                                                    . . . # $ % % $ & . . .                                                                                                                     ",
"                                                                                                                    . . * % % % % % % @ . .                                                                                                                     ",
"                                                                                                                  . . . = % % % % % % = . . .                                                                                                                   ",
"                                                                                                                  . . - ; % % % % % % ; > . .                                                                                                                   ",
"                                                                                                                  . . . , % % % % % % , . . .                                                                                                                   ",
"                                                                                                                    . . ' % % % % % % ' . .                                                                                                                     ",
"                                                                                                                    . . ) ! % % % % ! . . .                                                                                                                     ",
"                                                                                                                    . . . . ~ { { ~ . . . .                                                                                                                     ",
"                                                                                                                  . . . . . . . . . . . . . .                                                                                                                   ",
"                                                                                                                  . . .   . . . . . .   . . .                                                                                                                   ",
"                                                                                                                . . .         . .         . . .                                                                                                                 ",
"                                                                                                              . . .           . .           . . .                                                                                                               ",
"                                                                                                            . . .             . .             . . .                                                                                                             ",
"                                                                                                          . . .               . .               . . .                                                                                                           ",
"                                                                                                        . . .                 . .                 . . .                                                                                                         ",
"                                                                                                      . . .                   . .                   . . .                                                                                                       ",
"                                                                                                    . . .                     . .                     . . .                                                                                                     ",
"                                                                                                  . . .                       . .                       . . .                                                                                                   ",
"                                                                                                . . . .                       . .                       . . . .                                                                                                 ",
"                                                                                              . . . .                         . .                         . . . .                                                                                               ",
"                                                                                            . . . .                           . .                           . . . .                                                                                             ",
"                                                                                          . . . .                             . .                             . . . .                                                                                           ",
"                                                                                        . . . .                               . .                               . . . .                                                                                         ",
"                                                                                      . . . .                                 . .                                 . . . .                                                                                       ",
"                                                                                    . . . .                                   . .                                   . . . .                                                                                     ",
"                                                                                  . . . .                                     . .                                     . . . .                                                                                   ",
"                                                                                . . . .                                       . .                                       . . . .                                                                                 ",
"                                                                              . . . .                                         . .                                         . . . .                                                                               ",
"                                                                . . . . .   . . . .                                           . .                                           . . . .   . . . . .                                                                 ",
"                                                            . . . . . . . . . . .                                             . .                                             . . . . . . . . . . .                                                             ",
"                                                          . . . ] ^ / ( . . . .                                               . .                                               . . . . _ : ^ ] . . .                                                           ",
"                                                        . . . < [ % % } | 1 . .                                               . .                                               . . 1 | } % % [ 2 . . .                                                         ",
"                                                        . . 3 4 % % % % % 5 . . .                                             . .                                             . . . 5 % % % % % 4 6 . .                                                         ",
"                                                        . . 7 % % % % % % 8 9 . .                                             . .                                             . . 9 8 % % % % % % 7 . .                                                         ",
"                                                        . . 0 % % % % % % % a . .                                             . .                                             . . a % % % % % % % b . .                                                         ",
"                                                        . . c % % % % % % d e . .                                             . .                                             . . e d % % % % % % f . .                                                         ",
"                                                        . . g h % % % % % i . . .                                             . .                                             . . . j % % % % % h k . .                                                         ",
"                                                        . . . l m % % % n o . .                                               . .                                               . . o p % % % m l . . .                                                         ",
"                                                          . . . q # r s t . . .                                               . .                                               . . . u v r # q . . .                                                           ",
"                                                        . . . . . . . . . . . . .                                             . .                                             . . . . . . . . . . . . .                                                         ",
"                                                      . . .   . . . . . .   . . . .                                           . .                                           . . . .   . . . . . .   . . .                                                       ",
"                                                    . . .                       . . .                                         . .                                         . . .                       . . .                                                     ",
"                                                  . . .                           . . .                                       . .                                       . . .                           . . .                                                   ",
"                                                . . . .                             . . .                                     . .                                     . . .                             . . . .                                                 ",
"                                              . . . .                                 . . .                                   . .                                   . . .                                 . . . .                                               ",
"                                            . . . .                                     . . .                                 . .                                 . . .                                     . . . .                                             ",
"                                          . . . .                                         . . .                               . .                               . . .                                         . . . .                                           ",
"                                        . . . .                                             . . . .                           . .                           . . . .                                             . . . .                                         ",
"                                      . . . .                                                 . . . .                         . .                         . . . .                                                 . . . .                                       ",
"                                    . . . .                                                     . . . .                       . .                       . . . .                                                     . . . .                                     ",
"                                  . . . .                                                         . . . .                     . .                     . . . .                                                         . . . .                                   ",
"                                . . . .                                                             . . . .                   . .                   . . . .                                                             . . . .                                 ",
"                              . . . .                                                                 . . . .                 . .                 . . . .                                                                 . . . .                               ",
"                            . . . .                                                                     . . . .               . .               . . . .                                                                     . . . .                             ",
"                          . . . .                                                                         . . . .             . .             . . . .                                                                         . . . .                           ",
"                        . . . .                                                                             . . . .           . .           . . . .                                                                             . . . .                         ",
"                      . . . .                                                                                 . . . .         . .         . . . .                                                                                 . . . .                       ",
"        . . . . . . . . . .                                                                                     . . . .   . . . . . .   . . . .                                                                                     . . . . . . . . . .         ",
"    . . . . . . . . . . .                                                                                         . . . . . . . . . . . . . .                                                                                         . . . . . . . . . . .     ",
"  . . . w / x y z . . .                                                                                             . . . . A { { A . . . .                                                                                             . . . B y x / C . . .   ",
"  . . D E % % % F G . . .                                                                                           . . H ! % % % % ! ) . .                                                                                           . . . G I % % % E D . .   ",
". . J K % % % % % L M . .                                                                                           . . N % % % % % % ' . .                                                                                           . . e L % % % % % K O . . ",
". . A % % % % % % % / . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . , % % % % % % , . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . / % % % % % % % A . . ",
". . P % % % % % % % { . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . - ; % % % % % % ; > . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . Q % % % % % % % R . . ",
". . S % % % % % % % T . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . = % % % % % % = . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . U % % % % % % % V . . ",
". . . W % % % % % K X . .                                                                                           . . @ % % % % % % @ . .                                                                                           . . Y K % % % % % Z . . . ",
"  . . ` Z % % % ,  .. .                                                                                             . . . & $ % % $ & . . .                                                                                             . .  ., % % % Z ... .   ",
"  . . . . D +.@.H . . .                                                                                               . . . o ^ ^ o . . .                                                                                               . . . #.$.+.%.. . . .   ",
"    . . . . . . . . .                                                                                                   . . . . . . . .                                                                                                   . . . . . . . . .     ",
"        . . . . .                                                                                                         . . . . . .                                                                                                         . . . . .         "};
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


FreeCADGui.addCommand('QueenPost',QueenPost_Command() ) 
