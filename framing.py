import math
import FreeCAD
import FreeCADGui
import Draft
import plate

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


################################
## Utility methods           ###
################################
def isItemSelected():
    selection = FreeCADGui.Selection.getSelectionEx()
    if selection:
        return True
    return False


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
