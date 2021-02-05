Add a vertical line

>>>App.getDocument('Unnamed').getObject('StringerSketch').addGeometry(Part.LineSegment(App.Vector(-1251.836594,1383.472692,0),App.Vector(-1032.453966,1342.676957,0)),False)
>>> App.getDocument('Unnamed').getObject('StringerSketch').addConstraint(Sketcher.Constraint('Vertical',24)) 

App.getDocument('Unnamed').getObject('StringerSketch').addConstraint(Sketcher.Constraint('Equal',1,23)) 

Select Vertexz for Constraint

# Gui.Selection.addSelection('Unnamed','StringerSketch','Vertex48',3653.11,-38.0882,1548.7,False)
>>> # Gui.Selection.addSelection('Unnamed','StringerSketch','Vertex1',3454.4,-38.0882,1422.4,False)
>>> 

Add Contstraint

>>> App.getDocument('Unnamed').getObject('StringerSketch').addConstraint(Sketcher.Constraint('Coincident',23,2,0,1)) 


App.getDocument('Unnamed').getObject('StringerSketch').addGeometry(Part.LineSegment(App.Vector(-2235.200391,1964.292725,0),App.Vector(-2984.306348,1972.171631,0)),False)
>>> App.getDocument('Unnamed').getObject('StringerSketch').addConstraint(Sketcher.Constraint('Coincident',24,1,23,1)) 
>>> App.getDocument('Unnamed').getObject('StringerSketch').addConstraint(Sketcher.Constraint('Horizontal',24)) 
>>> App.getDocument('Unnamed').getObject('StringerSketch').addConstraint(Sketcher.Constraint('Equal',24,0)) 


Delete Contratints on Laddt vertical

>>> App.getDocument('Unnamed').getObject('StringerSketch').delConstraint(51)

Re-Constrain to new step
>>> App.getDocument('Unnamed').getObject('StringerSketch').addConstraint(Sketcher.Constraint('Coincident',2,1,24,2)) 

Delete the center line point on object constraint
>>> App.getDocument('Unnamed').getObject('StringerSketch').delConstraint(62)

Reattache to tangenet construciton
>>> App.getDocument('Unnamed').getObject('StringerSketch').addConstraint(Sketcher.Constraint('PointOnObject',20,1,21)) 

Attach to top step
App.getDocument('Unnamed').getObject('StringerSketch').addConstraint(Sketcher.Constraint('Coincident',20,1,2,1))

