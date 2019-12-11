import arcpy
import pythonaddins
import math
from arcpy.sa import *

subdivideSquareSideLength = 100
userDefinedExtent = None

raster1 = None
raster2 = None

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

        if raster1 == None or raster2 == None:
            pythonaddins.MessageBox('Raster1 and Raster2 to compare not set.', 'Error')
            return

        rasters = [raster1, raster2]
        ndviRasters = [None, None]


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

        for i in range(len(rasters)):
            # If a raster is shown with 5,4,3 bands displayed as bands 1,2,3
            nir = arcpy.MakeRasterLayer_management(rasters[i], "nir", "#", arcpy.env.extent, "1")
            red = arcpy.MakeRasterLayer_management(rasters[i], "red", "#", arcpy.env.extent, "2")

            if nir.outputCount == 0 or red.outputCount == 0:
                pythonaddins.MessageBox('Creating raster layer from bands produced no output.', 'Error')
                return
            else:
                nirRaster = Raster(nir[0].name)
                redRaster = Raster(red[0].name)
            # Add 0.16 to denominator for OSAVI https://www.tandfonline.com/doi/pdf/10.1080/22797254.2019.1625075?needAccess=true
            ndviRasters[i] = arcpy.MakeRasterLayer_management(Float(nirRaster - redRaster) / (nirRaster + redRaster + 0.16), 'ndvi{0}'.format(i))
            arcpy.Delete_management(nir)
            arcpy.Delete_management(red)
            arcpy.Delete_management(nirRaster)
            arcpy.Delete_management(redRaster)

        vi_rdc = arcpy.MakeRasterLayer_management((ndviRasters[1]-ndviRasters[0])/ndviRaster[0]*100, 'vi_rdc') # Calculate VI value for relative difference in contrast


        # Get count and display to user.
        #cnt = arcpy.GetCount_management(lyr)
        #msg = 'There are {0} features in the rectangle'.format(cnt)
        #pythonaddins.MessageBox(msg, 'Feature Count')
        # Restore the geoprocessing extent.
        arcpy.env.extent = old_extent

class SelectRaster1Button(object):
    """Implementation for change_finder_addin.select_raster_1_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        lyr = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        if isinstance(lyr, arcpy.mapping.Layer) and lyr.isRasterLayer:
            raster1 = lyr
        else:
            pythonaddins.MessageBox('Please select a raster layer.', 'Error')

class SelectRaster2Button(object):
    """Implementation for change_finder_addin.select_raster_2_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        lyr = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        if isinstance(lyr, arcpy.mapping.Layer) and lyr.isRasterLayer:
            raster2 = lyr
        else:
            pythonaddins.MessageBox('Please select a raster layer.', 'Error')