# encoding: utf-8
from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from math import degrees, atan2

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
		Glyphs.registerDefault( "com.mekkablue.ShowCoordinatesOfSelectedNodes.showNodes", 1 )
		Glyphs.registerDefault( "com.mekkablue.ShowCoordinatesOfSelectedNodes.showHandles", 1 )
	
	@objc.python_method
	def angle( self, firstPoint, secondPoint ):
		"""
		Returns the angle (in degrees) of the straight line between firstPoint and secondPoint,
		0 degrees being the second point to the right of first point.
		firstPoint, secondPoint: must be NSPoint or GSNode
		"""
		xDiff = secondPoint.x - firstPoint.x
		yDiff = secondPoint.y - firstPoint.y
		return degrees(atan2(yDiff,xDiff))
	
	@objc.python_method
	def foreground(self, layer):
		showNodes = Glyphs.defaults["com.mekkablue.ShowCoordinatesOfSelectedNodes.showNodes"]
		showHandles = Glyphs.defaults["com.mekkablue.ShowCoordinatesOfSelectedNodes.showHandles"]
		
		currentSelection = layer.selection
		if len(currentSelection) < 13:
			alpha = 0.7
			if Glyphs.versionNumber >= 3:
				# GLYPHS 3
				green = Glyphs.colorDefaults["GSColorNodeSmooth"].colorWithAlphaComponent_(alpha)
				brown = Glyphs.colorDefaults["GSColorBackgroundStroke"].colorWithAlphaComponent_(alpha)
			else:
				# GLYPHS 2
				green = NSColor.greenColor().colorWithAlphaComponent_(alpha)
				brown = NSColor.brownColor().colorWithAlphaComponent_(alpha)
			
			offset = 5.0 + self.getHandleSize() / self.getScale()
		
			if currentSelection:

				# coordinates of on-curves
				if showNodes:
					for thisItem in currentSelection:
						if type(thisItem) is GSNode:
							nodeType = thisItem.type
							if nodeType == LINE or nodeType == CURVE:
								xCoordinate = thisItem.x
								yCoordinate = thisItem.y
								self.drawTextAtPoint(
									f"{xCoordinate:.1f}, {yCoordinate:.1f} ".replace(".0,",",").replace(".0 ","").strip(),
									NSPoint( xCoordinate + offset, yCoordinate ),
									fontColor=brown,
									fontSize=10+2*Glyphs.handleSize,
								)
			
				# length and angles of adjacent nodes
				if showHandles:
					for thisPath in layer.paths:
						theseNodes = thisPath.nodes
						thisNumberOfNodes = len( theseNodes )
						for i in range( thisNumberOfNodes ):
							previousNode = theseNodes[ (i-1) % thisNumberOfNodes ]
							currentNode = theseNodes[ i ]
							if (previousNode in currentSelection or currentNode in currentSelection) and not (previousNode.type == OFFCURVE and currentNode.type == OFFCURVE):
								previousPoint = previousNode.position
								currentPoint = currentNode.position
								currentAngle = self.angle( previousPoint, currentPoint )
								currentDistance = distance( previousPoint, currentPoint )
								pointSum = addPoints( previousPoint, currentPoint )
								pointInTheMiddle = NSPoint( pointSum.x * 0.5 + offset, pointSum.y * 0.5 )
								self.drawTextAtPoint(
									f"{currentDistance:.1f} @{currentAngle:.1f}°".replace(".0 "," ").replace(".0°","°"),
									pointInTheMiddle,
									fontColor=green,
									fontSize=10+2*Glyphs.handleSize,
								)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
