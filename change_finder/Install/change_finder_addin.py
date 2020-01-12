# Created by Anson Liu

import arcpy
import pythonaddins
from arcpy import env
from arcpy.sa import *

import math
import os
import time

class AboutButton(object):
    """Implementation for change_finder_addin.about_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # Calling webbrowser on "Yes" button crashes arcmap but on No" button does not...
        if pythonaddins.MessageBox('Relative Difference in Contrast Heatmap\n\nDeveloped by Anson Liu (ansonliu.com)\nProject repository at github.com/ansonl/rdc-heatmap-arcmap-add-in\n\nPress No to open project website. Yes - I meant press No and not Yes.', 'About', 4) != "Yes":
            import webbrowser
            url = 'github.com/ansonl/rdc-heatmap-arcmap-add-in'
            webbrowser.open(url,new=2)

class ImageletSizeComboBox(object):
    """Implementation for change_finder_addin.imaglet_size_combobox (ComboBox)"""
    def __init__(self):
        self.items = ["N/A", "10", "100", "1000", "10,000", "100,000", "1,000,000"]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWW'
        self.width = 'WWWWWWWWW'
        self.value = "N/A"
    def onSelChange(self, selection):
        pass
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        if self.value != "N/A":
            self.value = self.value.replace(',','')
            try:
                int(self.value)
            except ValueError as e:
                pythonaddins.MessageBox(str(e) + "\n\n To analyze whole user defined extent at once and not split up into imagelets for localized analysis, use imagelet size of 0.", 'Error')
                self.value = "0"
    def onEnter(self):
        pass
    def refresh(self):
        pass

class IndexMethodComboBox(object):
    """Implementation for change_finder_addin.index_method_combobox (ComboBox)"""
    def __init__(self):
        self.items = ["Band 1", "NDVI", "OSAVI", "MSAVI2"]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.value = "Band 1"
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
        #check out spatial analyst extension
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")

        # Import separate TIF bands from Landsat 7,5,4,3,2
        # Use composite bands tool to create 5,4,3 layers, etc
        env.overwriteOutput = True

        global userDefinedExtent
        global raster1
        global raster2

        if raster1 is None or raster2 is None:
            pythonaddins.MessageBox('Raster1 and Raster2 to compare not set.', 'Error')
            return
            #DEV
            #1/0

        rasters = [raster1, raster2]
        viRasters = [None, None]
        viRastersCasted = [None, None]
        reclassified = []

        # Save the current geoprocessing extent.
        old_extent = arcpy.env.extent
        # Set extent to passed geometry. Save passed geometry in global variable.
        arcpy.env.extent = userDefinedExtent = rectangle_geometry
        #DEV
        #arizona example extent
        #arcpy.env.extent = userDefinedExtent = arcpy.Extent(-12190000, 4005000, -12188000, 4006000)

        #Confirm operation
        extentUpperRight = arcpy.env.extent.upperRight
        extentWidth = arcpy.env.extent.width
        extentHeight = arcpy.env.extent.height
        totalArea = extentHeight * extentWidth
        cellSizeX = int(arcpy.GetRasterProperties_management(raster1, "CELLSIZEX")[0])
        cellSizeY = int(arcpy.GetRasterProperties_management(raster1, "CELLSIZEY")[0])
        totalCells = totalArea / (cellSizeX * cellSizeY)
        amountOfImagelets = 1
        cellsPerImagelet = totalCells
        if imaglet_size_combobox.value != "N/A" and int(imaglet_size_combobox.value) != 0:
            amountOfImagelets = math.ceil(extentHeight / int(imaglet_size_combobox.value)) * math.ceil(extentWidth / int(imaglet_size_combobox.value))
            cellsPerImagelet = int(imaglet_size_combobox.value)**2 / (cellSizeX * cellSizeY)

        if pythonaddins.MessageBox('{0} total area to analyze\n{1} total cells to analyze (approximate based on raster1 cell size)\n\n{2} imagelets will be analyzed separately at {3} cells per imagelet\n\nNote: Pause drawing (F9) to get ~10%% faster performance.'.format(totalArea, totalCells, amountOfImagelets, cellsPerImagelet), 'Confirm Operation?', 1) != "OK":
            return
            #DEV
            #1/0

        # Log start time
        start = time.time()

        imageletExtents = []
        fishnetFeatureClassName = "fishnet.shp"
        #output coordinate system MUST be set to the dataframe spatial reference or the coordinates for the fishnet will be wrong
        mxd = arcpy.mapping.MapDocument("CURRENT")
        env.outputCoordinateSystem = arcpy.mapping.ListDataFrames(mxd)[0].spatialReference
        # Set the origin of the fishnet
        originCoordinate = "{0} {1}".format(arcpy.env.extent.lowerLeft.X, arcpy.env.extent.lowerLeft.Y)
        # Set the orientation
        yAxisCoordinate = "{0} {1}".format(arcpy.env.extent.lowerLeft.X, arcpy.env.extent.lowerLeft.Y+10)
        if imaglet_size_combobox.value != "N/A" and int(imaglet_size_combobox.value) != 0:
            cellSizeWidth = int(imaglet_size_combobox.value)
            cellSizeHeight = int(imaglet_size_combobox.value)
            numRows =  '0'
            numColumns = '0'
        else:
            cellSizeWidth = '0'
            cellSizeHeight = '0'
            numRows =  1
            numColumns = 1

        oppositeCorner = "{0} {1}".format(arcpy.env.extent.upperRight.X, arcpy.env.extent.upperRight.Y)
        # Create a point label feature class 
        labels = 'NO_LABELS'
        # Extent is set by origin and opposite corner - no need to use a template fc
        templateExtent = '#'
        # Each output cell will be a polygon
        geometryType = 'POLYGON'
        #do fishnet
        arcpy.CreateFishnet_management(fishnetFeatureClassName, originCoordinate, yAxisCoordinate, cellSizeWidth, cellSizeHeight, numRows, numColumns, oppositeCorner, labels, templateExtent, geometryType)

        # put imagelet extents into list
        with arcpy.da.SearchCursor(fishnetFeatureClassName[:-4], ["OID@", "SHAPE@"]) as cursor:
            for row in cursor:
                imageletExtents.append(row[1].extent)
        arcpy.Delete_management(fishnetFeatureClassName[:-4])

        #else: # If not spliting into imagelet, supply the whole extent as one big imagelet extent
         #   imageletExtents.append(arcpy.env.extent)


        for idx, iExtent in enumerate(imageletExtents):
            #disable adding outputs to map for performance
            arcpy.env.addOutputsToMap = False

            if (single_raster_combobox.value != "YES"):
                for i in range(len(rasters)):
                    # If a raster is shown with 5,4,3 bands displayed as bands 1,2,3
                    nir = arcpy.MakeRasterLayer_management(rasters[i], "nir{0}".format(idx), "#", iExtent, "1")
                    red = arcpy.MakeRasterLayer_management(rasters[i], "red{0}".format(idx), "#", iExtent, "2")

                    if nir.outputCount == 0 or red.outputCount == 0:
                        pythonaddins.MessageBox('Creating raster layer from bands produced no output.', 'Error')
                        #return
                        1/0
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
                        #return  
                        1/0         

                    arcpy.Delete_management(nir)
                    arcpy.Delete_management(red)

                for i in range(len(viRasters)):
                    if viRasters[i].outputCount == 0:
                        pythonaddins.MessageBox('VI raster produced no output.', 'Error')
                        #return
                        1/0

                    viRastersCasted[i] = Raster(viRasters[i][0].name)

                global vi_rdc
                # Calculate VI value for relative difference in contrast
                vi_rdc = arcpy.MakeRasterLayer_management((viRastersCasted[1]-viRastersCasted[0])/viRastersCasted[0]*100, '{0}_rdc'.format(index_method_combobox.value)) 

                for i in range(len(viRasters)):
                    arcpy.Delete_management(viRasters[i])

                #rdcNumpyArray = arcpy.RasterToNumPyArray(vi_rdc[0].name)
                #plt.hist(rdcNumpyArray.flatten(), bins = 50) 
                #print(rdcNumpyArray.flatten())
                #plt.ylabel('Pixel Count')
                #plt.xlabel('Pixel Values')
                #plt.savefig('vi_rdc_hist.png')  
                #plt.close()  
                #os.system('vi_rdc_hist.png')
                
            # Special case for Single Raster analysis (Raster 1 only)
            if (single_raster_combobox.value == "YES"): 

                # If a raster is shown with 5,4,3 bands displayed as bands 1,2,3
                nir = arcpy.MakeRasterLayer_management(rasters[0], "nir{0}".format(idx), "#", iExtent, "1")
                red = arcpy.MakeRasterLayer_management(rasters[0], "red{0}".format(idx), "#", iExtent, "2")

                if nir.outputCount == 0 or red.outputCount == 0:
                    pythonaddins.MessageBox('Creating raster layer from bands produced no output.', 'Error')
                    #return
                    1/0
                else:
                    nirRaster = Raster(nir[0].name)
                    redRaster = Raster(red[0].name)
                
                if (index_method_combobox.value == "Band 1"):
                    vi_rdc = arcpy.MakeRasterLayer_management(Float(nirRaster), 'band-1_{0}'.format(i))
                elif (index_method_combobox.value == "NDVI"):
                    vi_rdc = arcpy.MakeRasterLayer_management(Float(nirRaster - redRaster) / (nirRaster + redRaster), 'ndvi_{0}'.format(i))
                elif (index_method_combobox.value == "OSAVI"):
                    # Add 0.16 to denominator for OSAVI https://www.tandfonline.com/doi/pdf/10.1080/22797254.2019.1625075?needAccess=true
                    vi_rdc = arcpy.MakeRasterLayer_management(Float(nirRaster - redRaster) / (nirRaster + redRaster + 0.16), 'osavi_{0}'.format(i))
                elif (index_method_combobox.value == "MSAVI2"):
                    # http://www.remote-sensing.info/wp-content/uploads/2012/07/A_FAQ_on_Vegetation_in_Remote_Sensing.pdf
                    vi_rdc = arcpy.MakeRasterLayer_management(0.5 * (2.0 * Float(nirRaster + 1) - SquareRoot(Power(2.0 * Float(nirRaster + 1.0), 2) - 8.0 * Float(nirRaster - redRaster))), 'msavi2_{0}'.format(i))
                else:
                    pythonaddins.MessageBox('No supported index method selected.', 'Error')     
                    #return  
                    1/0         

                arcpy.Delete_management(nir)
                arcpy.Delete_management(red)

            vi_rdc[0].visible = False


            # Compute difference of each pixel VI r.d.c to the average in the rdc raster
            vi_rdcRaster = Raster(vi_rdc[0].name)
            vi_rdcRaster.save('{0}/../{1}_{2}.tif'.format(raster1.workspacePath, vi_rdc[0].name, idx))
            vi_rdc_diff = arcpy.MakeRasterLayer_management(Abs(vi_rdcRaster - vi_rdcRaster.mean), '{0}_diff'.format(vi_rdc[0].name))
            vi_rdc_diffRaster = Raster(vi_rdc_diff[0].name)
            vi_rdc_diffRaster.save('{0}/../{1}_{2}.tif'.format(raster1.workspacePath, vi_rdc_diff[0].name, idx))

            absStdDev = abs(vi_rdcRaster.standardDeviation)
            #print(absStdDev)
            #print(vi_rdc_diffRaster.maximum)

            reclassified.append(Reclassify(vi_rdc_diff[0].name, "Value", RemapRange([[0,absStdDev,"NODATA"],[absStdDev,absStdDev*2,1],[absStdDev*2,absStdDev*3,2],[absStdDev*3,vi_rdc_diffRaster.maximum if vi_rdc_diffRaster.maximum>absStdDev*3 else absStdDev*3+1,3]])))
            reclassified[idx].save('{0}/../{1}-highlight_{2}.tif'.format(raster1.workspacePath, vi_rdc_diff[0].name, idx))
            #Re-enable adding outputs to map to show the classified heatmap
            arcpy.env.addOutputsToMap = True
            output = arcpy.MakeRasterLayer_management('{0}/../{1}-highlight_{2}.tif'.format(raster1.workspacePath, vi_rdc_diff[0].name, idx), '{0}-highlight_{1}'.format(vi_rdc_diff[0].name, idx))

            # Apply symbology from a manually colored layer exported layer (right click > Save As Layer File) that we premade
            # http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//00170000006n000000
            arcpy.ApplySymbologyFromLayer_management(output[0], os.path.dirname( arcpy.mapping.MapDocument('CURRENT').filePath )+"\\highlight_heatmap.lyr")

            arcpy.Delete_management(vi_rdc)
            vi_rdc_diff[0].visible = False

        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()

        print("Creating heatmap took {0} seconds.".format(time.time()-start))

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

class SingleRasterComboBox(object):
    """Implementation for change_finder_addin.single_raster_combobox (ComboBox)"""
    def __init__(self):
        self.items = ["NO", "YES"]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWW'
        self.width = 'WWW'
        self.value = "NO"
    def onSelChange(self, selection):
        select_raster_2_button.enabled = selection != "YES"
        pass
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass