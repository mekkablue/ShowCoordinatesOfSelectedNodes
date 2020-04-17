# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

from GlyphsApp import *
from GlyphsApp.plugins import *
from math import degrees, atan2

@objc.python_method
def angle( firstPoint, secondPoint ):
	"""
	Returns the angle (in degrees) of the straight line between firstPoint and secondPoint,
	0 degrees being the second point to the right of first point.
	firstPoint, secondPoint: must be NSPoint or GSNode
	"""
	xDiff = secondPoint.x - firstPoint.x
	yDiff = secondPoint.y - firstPoint.y
	return degrees(atan2(yDiff,xDiff))

class ShowCoordinatesOfSelectedNodes(ReporterPlugin):
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Coordinates of Selected Nodes',
			'de': 'Koordinaten ausgewählter Punkte',
			'nl': 'coördinaten van geselecteerde punten',
			'fr': 'les coordonnées des nœuds sélectionnés',
			'es': 'las coordenadas de nodos seleccionados',
			'pt': 'coordenadas dos nós selecionados',
		})
	
	@objc.python_method
	def foreground(self, Layer):
		currentSelection = set(Layer.selection)
		if len(currentSelection) < 13:
			green = NSColor.colorWithRed_green_blue_alpha_( 0.1, 0.7, 0.2, 1.0 )
			brown = NSColor.brownColor()
			
			offset = 5.0 + self.getHandleSize() / self.getScale()
		
			if currentSelection:
				# coordinates of on-curves
				for thisItem in currentSelection:
					if type(thisItem) is GSNode:
						nodeType = thisItem.type
						if nodeType == LINE or nodeType == CURVE:
							xCoordinate = thisItem.x
							yCoordinate = thisItem.y
							self.drawTextAtPoint(
								("%.1f, %.1f" % ( xCoordinate, yCoordinate )).replace(".0",""),
								NSPoint( xCoordinate + offset, yCoordinate ),
								fontColor=brown
							)
			
				# length and angles of adjacent nodes
				for thisPath in Layer.paths:
					theseNodes = thisPath.nodes
					thisNumberOfNodes = len( theseNodes )
					for i in range( thisNumberOfNodes ):
						previousNode = theseNodes[ (i-1) % thisNumberOfNodes ]
						currentNode = theseNodes[ i ]
						if (previousNode in currentSelection or currentNode in currentSelection) and not (previousNode.type == OFFCURVE and currentNode.type == OFFCURVE):
							previousPoint = previousNode.position
							currentPoint = currentNode.position
							currentAngle = angle( previousPoint, currentPoint )
							currentDistance = distance( previousPoint, currentPoint )
							pointSum = addPoints( previousPoint, currentPoint )
							pointInTheMiddle = NSPoint( pointSum.x * 0.5 + offset, pointSum.y * 0.5 )
							self.drawTextAtPoint(
								(u"%.1f @%.1f°" % ( currentDistance, currentAngle )).replace(".0",""),
								pointInTheMiddle,
								fontColor=green
							)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
