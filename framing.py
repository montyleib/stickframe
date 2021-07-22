import math
import FreeCAD
import FreeCADGui
import Draft
import Part
import plate
import os

import stud

# def makeStud(name):
#	newstud = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name )
#	Stud(newstud)
#	ViewProviderStud(newstud.ViewObject)
#	return newstud

mod_name = "stickframe"

def makePlate(name):
    newplate = plate.Plate_Command()
    return newplate


def makeFloorJoist(name):
    pass


def makeCeilingJoist(name):
    pass


def makeRafter(name):
    pass


def makeFloorPanel(name):
    pass


################################
## Intermediate Constructions ##
################################

def bottomWallPlates(selectedline):

    starterplate = self.makePlate("BottomPlate")

#	totalplates = math.ceil ( selectedline.length/starterplate.length )
#	lastplatelength = selectedline.length % starterplate.length

    starterplate.Placement.Base = selectedLine.Start
    starterplate.Placement.Rotation = getLineAngle(selectedLine)

    pass


def topWallPlates(selectedLine):
    pass


def startingStudCorner(selectedLine):
    pass


def endingStudCorner(selectedLine):
    pass


def nailers():
    pass


def fillerStuds():
    pass
    
    
def populateStuds( sketchinstance, studtype ):

	print ( sketchinstance.Name )
	print ( studtype )

	

	sketch_name = FreeCAD.ActiveDocument.getObject( sketchinstance.Name )
	edges = sketchinstance.Shape.Edges 
	
	print ( edges )
	
	points = []
	studs = []
	
	for vertex in sketchinstance.Shape.Vertexes:
		points.append(vertex.Point)		
	
	for  edge in edges:
	
		newstud = stud.makeStud( studtype )	
		newstud.Length =  edge.Length
		idx = edges.index(edge) + 1

		if ( edge.Vertexes[0].Point in points ):
#			print ( edge.Vertexes[0].Point )
#			print (points.index( edge.Vertexes[0].Point ) )
			vert1 = "Vertex" + str  ( points.index( edge.Vertexes[0].Point ) + 1 )
			vert2 = "Vertex" + str  ( points.index( edge.Vertexes[1].Point ) + 1 )
			
			#print ("========")
			#print ( edge.Vertexes[0].Point )
			#print ( edge.Vertexes[1].Point )
			#print ( "-------" )
			fvert = edge.firstVertex().Point
			lvert = edge.lastVertex().Point

#			if ( (fvert.x > lvert.x) or (fvert.y > lvert.y) ):
#			
#				print ("Inverted mapping")
#				newstud.Support = [(sketch_instance,vert2),(sketch_instance,vert1)]
#			else:

			newstud.Support = [(sketchinstance,vert1),(sketchinstance,vert2)]
			
			expression = sketchinstance.Name + ".Shape.Edge" + str(idx) + ".Length"
			
			newstud.setExpression( 'Length', expression)
			

# reversed line fix ???			

			if ( idx == 0 ):
			
				cut_truss = FreeCAD.ActiveDocument.addObject("Part::Chamfer","cut_truss")
				cut_truss.Base = newstud
			
				ridge_angle = newstud.Shape.Face1.Placement.Rotation.toEuler()[2]
				
				#
				edgeAngle = degrees ( vert1.Point.getAngle ( vert2.Point ) )
				
				a = 3.5
				A = 180 - ridge_angle
				B = 90
				C = 180 - A - B
				b = a·sin(B)/sin(A)
				c = a·sin(C)/sin(A)
				
				__fillets__ = []
				__fillets__.append((3,b,c))
				
				cut_truss.Edges = __fillets__
				newcollar.Shape = collar

			
#			if ( idx == 1 ):
				#offset center post
#				newstud.AttachmentOffset = FreeCAD.Placement(FreeCAD.Vector(0,44.45,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))	
								
#			if( idx == 2 ) :
#				pass				
								
		newstud.MapMode = 'OZX'   
		
		studs.append( newstud ) 
		
	return studs		


################################
## Utility methods           ###
################################
def isItemSelected():
    selection = FreeCADGui.Selection.getSelectionEx()
    if selection:
        return True
    return False

def getIconImage( toolname ):

#	image_path = "/" + framing.mod_name + '/icons/stud.png'
	image_path = '/stickframe/icons/' + toolname + ".png"

	global_path = FreeCAD.getHomePath()+"Mod"
	user_path = FreeCAD.getUserAppDataDir()+"Mod"
	icon_path = ""

	if os.path.exists(user_path + image_path):
		icon_path = user_path + image_path

	elif os.path.exists(global_path + image_path):
		icon_path = global_path + image_path

	return icon_path	

def defaultAttachment( framing_member ):
	if isItemSelected():
		selection = FreeCADGui.Selection.getSelectionEx()

		obj = selection[0].SubElementNames
		edge_name = obj[0]

		edge_obj = FreeCADGui.Selection.getSelection()[0]
		edge_shp = FreeCADGui.Selection.getSelection()[0].Shape
		edge_elt = FreeCADGui.Selection.getSelection ()[0].Shape.Edge1

		if isinstance( edge_shp, Part.Wire ):
		#Check if a single edge
			print ( "number of edges = "  + str(edge_shp.Edges.__len__() ) )
		
			if edge_shp.Edges.__len__() == 1:	
				print( "Adding single item to single edge")	
				
				framing_member.Length = edge_elt.Length
				
				FreeCAD.ActiveDocument.getObject(framing_member.Name).Support = [(edge_obj,'Vertex1'),(edge_obj,edge_name)]
				FreeCAD.ActiveDocument.getObject(framing_member.Name).MapMode = 'OXY'	
				print("item selected part.wire:", obj[0] )
			if edge_shp.Edges.__len__() > 1:
				print( "Multiple edges found")	
				return False												
	return True
	
#def multiEdgeAttachments( primary_framing_member, secondary_framing_member ):
	#need to add a generic make for each framing member, os on odd even can just call add() or make()
	# or can I construct a call using a string like - make +"Wall" + "()"
	

	print ( primary_framing_member )
	
#	pri_module_ = __import__( primary_framing_member )
	#sec_module_ = __import__( secondary_framing_member )
	
	
#	pri_instance = pri_module_
#	pri_class_ = getattr( pri_instance, "Wall_Command" )
#	pri_class_.Activated( pri_instance )
		
	
	
	
	
	print( "Adding walls to all edges" )
	if isItemSelected():
		selection = FreeCADGui.Selection.getSelectionEx()

		obj = selection[0].SubElementNames
		edge_name = obj[0]

		edge_obj = FreeCADGui.Selection.getSelection()[0]
		edge_shp = FreeCADGui.Selection.getSelection()[0].Shape
		
		edge_count = edge_shp.Edges.__len__()
		
		for edge in edge_shp.Edges:
			#edge_name = "Edge" + str(edge_shp.Edges.index(edge) + 1 )
		
			edge_name = "Edge1"
		
			#GET THIS EDGES VERTEX MAPPED TO SHAP VERTEXES.
		
			if isinstance( edge_shp, Part.Wire ):
				if edge_count > 1 and math.fmod ( edge_count,2) == 0:
					#add wall
					newwall = wall.makeWall()
					#attach wall to cirrent edge
					vert1name, vert2name = matchVertexes( edge_shp, edge )
					FreeCAD.ActiveDocument.getObject(newwall.Name).Support = [(edge,vert1name),(edge,edge_name)]
					FreeCAD.ActiveDocument.getObject(partobj.Name).MapMode = 'OXY'
					
				if edge_count > 1 and math.fmod ( edge_count,2) == 1:
					#add simple wall
					newwall = simplewall.makeSimpleWall()
					#attach wall to current edge
					vert1name, vert2name = matchVertexes( edge_shp, edge )
					FreeCAD.ActiveDocument.getObject(newwall.Name).Support = [(edge,vert1name),(edge,edge_name)]
					FreeCAD.ActiveDocument.getObject(partobj.Name).MapMode = 'OXY'

					
def matchVertexes( shape, edge  ):
	points = []
	
	for vertex in shape.Vertexes:
		points.append(vertex.Point)		

	fvert = edge.Vertexes[0].Point
	lvert = edge.Vertexes[1].Point
	
	if ( edge.Vertexes[0].Point in points ):
		point1name = "Vertex" + str( points.index(fvert) + 1 )
	if ( edge.Vertexes[1].Point in points ):
		point2name = "Vertex" + str( points.index(lvert) + 1 )					

	return point1name,point2name	


def getSelectedObject():
#    selection = FreeCADGui.Selection.getSelectionEx()
    selection = FreeCADGui.Selection.getSelection()
#    object = selection[0].Object
    object = selection[0]
    return object


def getSelectedElement():
    selection = FreeCADGui.Selection.getSelectionEx()
    element = selection[0].SubObjects[0]
    return element


def getSelectedPlacement():
    selection = FreeCADGui.Selection.getSelectionEx()
    object = selection[0]
    selectedPlacement = object.Placement
    return selectedPlacement


def getSelectedDirection():
    pass


def getFaceDirection(selectedPlane, drawpointer=False):
    """
    Given a Face make a line, return a vector with the direction.
    """
    com = selectedPlane.CenterOfMass
    # find the surface u,v parameter of a point on the surface edge
    # using the CenterOfMass of the face
    u, v = selectedPlane.Surface.parameter(com)
    normal = selectedPlane.normalAt(u, v)  # use u,v to find normal vector
    x1 = selectedPlane.CenterOfMass
    normal.multiply(100)
    x2 = x1 + normal
    if drawpointer:
        myline = Draft.makeLine(x1, x2)
        myline.ViewObject.EndArrow = True
        myline.ViewObject.ArrowType = "Arrow"
        myline.ViewObject.ArrowSize = ".5 in"

    # add a line with an arrow to indicate direction
    return normal.normalize()


def getLineAngle(selectedline):
    """
    Given a line return a rotatation.
    """
    print(selectedline.Name)
    print(selectedline.Placement)
    verts = selectedline.Shape.Vertexes

    point1 = verts[0]
    point2 = verts[1]

    Y1 = point1.Y
    Y2 = point2.Y

    X1 = point1.X
    X2 = point2.X

    slope = (Y2-Y1) / (X2-X1)
    radians = math.atan2(Y2-Y1, X2-X1)
    angle = math.degrees(radians)

#	print "\t", Y2, " - ", Y1
#	print "M =\t ----------"
#	print "\t", X2, " - ", X1
#	print "\n"

#	print "Slope: ", slope
#	print "Angle in Radians: ", radians
    print("Angle in Degrees: ", angle)

    axis = selectedline.Placement.Base

    rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), angle)
#	print rotation
    return rotation


class _ViewProviderFraming():

    def __init__(self, vobj, icon='/icons/studwallnailer.png'):
        self.iconpath = __dir__ + icon
        self.Object = vobj.Object
        vobj.Proxy = self

    def getIcon(self):
        return self.iconpath
