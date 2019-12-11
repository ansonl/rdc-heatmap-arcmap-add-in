import arcpy
import pythonaddins

import math

class ComputeChangeInAreaButton(object):
    """Implementation for demo_addin.statistics_tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "Line" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift):
        pass
    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        pass
    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        # Get selected layer.
        lyr = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        # Make sure it's a raster layer.
        if isinstance(lyr, arcpy.mapping.Layer) and lyr.isRasterLayer:
            # Get raster object.
            raster = arcpy.Raster(lyr.dataSource)
            # Clip the raster.
            clipped = arcpy.sa.ExtractByPolygon(raster, list(line_geometry.getPart(0)))
            #Create msg with statistics from clipped raster
            msg = 'Minimum: {0}\nMaximum: {1}\nMean: {2}\nStandard deviation: {3}'.format(clipped.minimum, clipped.maximum, clipped.mean, clipped.standardDeviation)
            pythonaddins.MessageBox(msg, 'Statistics')
        else:
            # Show a message if a raster layer wasn't selected.
            pythonaddins.MessageBox('Please select a raster layer.', 'Error')
    def onRectangle(self, rectangle_geometry):
        pass
class SelectAreaButton(object):
    """Implementation for change_finder_addin.select_area_button (Button)"""
    subdivideSquareSideLength = 100

    def __init__(self):
        self.enabled = True
        self.shape = "Rectangle"
    def onClick(self):
        pass
    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift):
        pass
    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        pass
    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        pass
    def onRectangle(self, rectangle_geometry):
        # Get selected layer.
        lyr = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        # Make sure it's a feature layer.
        if isinstance(lyr, arcpy.mapping.Layer) and lyr.isRasterLayer:
            # Save the current geoprocessing extent.
            old_extent = arcpy.env.extent
            # Set extent to passed geometry.
            arcpy.env.extent = rectangle_geometry


            extentUpperRight = arcpy.env.extent.upperRight
            extentWidth = arcpy.env.extent.width
            extentHeight = arcpy.env.extent.height

            amountOfImagelets = math.ceil(extentHeight / subdivideSquareSideLength) * math.ceil(extentWidth / subdivideSquareSideLength)
            arcpy.AddMessage('{0} imagelets will be computed'.format(amountOfImagelets))


            # Get count and display to user.
            #cnt = arcpy.GetCount_management(lyr)
            #msg = 'There are {0} features in the rectangle'.format(cnt)
            #pythonaddins.MessageBox(msg, 'Feature Count')
            # Restore the geoprocessing extent.
            arcpy.env.extent = old_extent
        else:
            # Show a message if a feature layer wasn't selected.
            pythonaddins.MessageBox('Please select a raster layer.', 'Error')