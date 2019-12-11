import arcpy
import pythonaddins
from arcpy import env
from arcpy.sa import *

import math
import os
import numpy as np
import matplotlib.pyplot as plt

subdivideSquareSideLength = 100
userDefinedExtent = None

raster1 = None
raster2 = None

vi_rdc = None

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

class ClipRasterRectangleTool(object):
    """Implementation for change_finder_addin.compute_change_in_area_tool (Tool)"""
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
        # Get selected layer.
        lyr = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        # Make sure it's a raster layer.
        if isinstance(lyr, arcpy.mapping.Layer) and lyr.isRasterLayer:
            # Get raster object.
            raster = arcpy.Raster(lyr.dataSource)
            # Clip the raster.
            clipped = arcpy.sa.ExtractByPolygon(raster, list(line_geometry.getPart(0)))
            result = arcpy.MakeRasterLayer_management(clipped, '{0}-clipped'.format(lyr.name))
        else:
            # Show a message if a raster layer wasn't selected.
            pythonaddins.MessageBox('Please select a raster layer.', 'Error')
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

        global subdivideSquareSideLength
        global userDefinedExtent

        if raster1 is None or raster2 is None:
            pythonaddins.MessageBox('Raster1 and Raster2 to compare not set.', 'Error')
            return

        rasters = [raster1, raster2]
        viRasters = [None, None]
        viRastersCasted = [None, None]

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
            
            if (index_method_combobox.value == "Band 1"):
                viRasters[i] = arcpy.MakeRasterLayer_management(Float(nirRaster), 'band-1_{0}'.format(i))
            elif (index_method_combobox.value == "NDVI"):
                viRasters[i] = arcpy.MakeRasterLayer_management(Float(nirRaster - redRaster) / (nirRaster + redRaster), 'ndvi_{0}'.format(i))
            elif (index_method_combobox.value == "OSAVI"):
                # Add 0.16 to denominator for OSAVI https://www.tandfonline.com/doi/pdf/10.1080/22797254.2019.1625075?needAccess=true
                viRasters[i] = arcpy.MakeRasterLayer_management(Float(nirRaster - redRaster) / (nirRaster + redRaster + 0.16), 'osavi_{0}'.format(i))
            elif (index_method_combobox.value == "MSAVI2"):
                # http://www.remote-sensing.info/wp-content/uploads/2012/07/A_FAQ_on_Vegetation_in_Remote_Sensing.pdf
                viRasters[i] = arcpy.MakeRasterLayer_management(0.5 * (2.0 * Float(nirRaster + 1) - SquareRoot(Power(2.0 * Float(nirRaster + 1.0), 2) - 8.0 * Float(nirRaster - redRaster))), 'msavi2_{0}'.format(i))
            else:
                pythonaddins.MessageBox('No supported index method selected.', 'Error')     
                return           

            arcpy.Delete_management(nir)
            arcpy.Delete_management(red)

        for i in range(len(viRasters)):
            if viRasters[i].outputCount == 0:
                pythonaddins.MessageBox('VI raster produced no output.', 'Error')
                return
            viRastersCasted[i] = Raster(viRasters[i][0].name)

        global vi_rdc
        vi_rdc = arcpy.MakeRasterLayer_management((viRastersCasted[1]-viRastersCasted[0])/viRastersCasted[0]*100, '{0}_rdc'.format(index_method_combobox.value)) # Calculate VI value for relative difference in contrast

        for i in range(len(viRasters)):
            arcpy.Delete_management(viRasters[i])

        rdcNumpyArray = arcpy.RasterToNumPyArray(vi_rdc[0].name)
        plt.hist(rdcNumpyArray.flatten(), bins = 50) 
        print(rdcNumpyArray.flatten())
        plt.ylabel('Pixel Count')
        plt.xlabel('Pixel Values')
        plt.savefig('vi_rdc_hist.png')  
        plt.close()  
        os.system('vi_rdc_hist.png')

        # Compute difference of each pixel VI r.d.c to the average in the rdc raster
        vi_rdc_diff = arcpy.MakeRasterLayer_management(Abs(vi_rdc - vi_rdc.average))

        vi_rdc_highlight = Reclassify(vi_rdc_diff[0].name, "Value", RemapRange([[0,vi_rdc.standardDeviation,"NODATA"],[vi_rdc.standardDeviation,vi_rdc.standardDeviation*2,1],[vi_rdc.standardDeviation*2,vi_rdc.standardDeviation*3,2],[vi_rdc.standardDeviation*3,vi_rdc.maximum,3]]))

        # Restore the geoprocessing extent.
        arcpy.env.extent = old_extent

class SelectRaster1Button(object):
    """Implementation for change_finder_addin.select_raster_1_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        global raster1
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
        global raster2
        lyr = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        if isinstance(lyr, arcpy.mapping.Layer) and lyr.isRasterLayer:
            raster2 = lyr
        else:
            pythonaddins.MessageBox('Please select a raster layer.', 'Error')

class Reclassify0BackgroundAsNODATAButton(object):
    """Implementation for change_finder_addin.select_raster_1_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        env.overwriteOutput = True
        lyr = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        if isinstance(lyr, arcpy.mapping.Layer) and lyr.isRasterLayer:
            noDataBackground = Con(Raster(lyr.name) != 0, lyr.name)
            fileParts = os.path.splitext(lyr.name)
            savePath = '{0}/{1}-noBG{2}'.format(lyr.workspacePath, fileParts[0], fileParts[1])
            noDataBackground.save(savePath)
            result = arcpy.MakeRasterLayer_management(savePath, '{0}-noBG'.format(fileParts[0]))
        elif isinstance(lyr, list):
            for i in range(len(lyr)): 
                if lyr[i].isRasterLayer:
                    noDataBackground = Con(Raster(lyr[i].name) != 0, lyr[i].name)
                    fileParts = os.path.splitext(lyr[i].name)
                    savePath = '{0}/{1}-noBG{2}'.format(lyr[i].workspacePath, fileParts[0], fileParts[1])
                    noDataBackground.save(savePath)
                    result = arcpy.MakeRasterLayer_management(savePath, '{0}-noBG'.format(fileParts[0]))
                else:
                    pythonaddins.MessageBox('Please select a raster layer.', 'Error')
        else:
            pythonaddins.MessageBox('Please select a raster layer.', 'Error')

class IndexMethodComboBox(object):
    """Implementation for change_finder_addin.index_method_combobox (ComboBox)"""
    def __init__(self):
        self.items = ["Band 1", "NDVI", "OSAVI", "MSAVI2"]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
    def onSelChange(self, selection):
        pass
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass