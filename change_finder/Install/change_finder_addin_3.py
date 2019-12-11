import arcpy
import pythonaddins
import math
from arcpy.sa import *

subdivideSquareSideLength = 100
userDefinedExtent = None

class ComputeChangeInAreaTool(object):
    """Implementation for change_finder_addin.compute_change_in_area_tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
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
        pass

class SelectAreaTool(object):
    """Implementation for change_finder_addin.select_area_tool (Tool)"""
    

    def __init__(self):
        self.enabled = True
        self.shape = "Rectangle" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
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
        # Import separate TIF bands from Landsat 7,5,4,3,2
        # Use composite bands tool to create 5,4,3 layers, etc


        # Get selected layer.
        lyr = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        # Make sure it's a feature layer.
        if isinstance(lyr, arcpy.mapping.Layer) and lyr.isRasterLayer:
            # Save the current geoprocessing extent.
            old_extent = arcpy.env.extent
            # Set extent to passed geometry. Save passed geometry in global variable.
            arcpy.env.extent = userDefinedExtent = rectangle_geometry

            extentUpperRight = arcpy.env.extent.upperRight
            extentWidth = arcpy.env.extent.width
            extentHeight = arcpy.env.extent.height

            amountOfImagelets = math.ceil(extentHeight / subdivideSquareSideLength) * math.ceil(extentWidth / subdivideSquareSideLength)
            if pythonaddins.MessageBox('{0} imagelets will be computed'.format(amountOfImagelets), 'Message', 1) != "OK":
                return

            # If a raster is shown with 5,4,3 bands displayed as bands 1,2,3
            nir = arcpy.MakeRasterLayer_management(lyr, "nir", "#", arcpy.env.extent, "1")
            red = arcpy.MakeRasterLayer_management(lyr, "red", "#", arcpy.env.extent, "2")

            if nir.outputCount == 0 or red.outputCount == 0:
                pythonaddins.MessageBox('Creating raster layer from bands produced no output.', 'Error')
                return
            else:
                nirRaster = Raster(nir[0].name)
                redRaster = Raster(red[0].name)

            ndvi = arcpy.MakeRasterLayer_management(Float(nirRaster - redRaster) / (nirRaster + redRaster), "ndvi")
            arcpy.Delete_management(nir)
            arcpy.Delete_management(red)
            arcpy.Delete_management(nirRaster)
            arcpy.Delete_management(redRaster)


            # Get count and display to user.
            #cnt = arcpy.GetCount_management(lyr)
            #msg = 'There are {0} features in the rectangle'.format(cnt)
            #pythonaddins.MessageBox(msg, 'Feature Count')
            # Restore the geoprocessing extent.
            arcpy.env.extent = old_extent
        else:
            # Show a message if a feature layer wasn't selected.
            pythonaddins.MessageBox('Please select a raster layer.', 'Error')