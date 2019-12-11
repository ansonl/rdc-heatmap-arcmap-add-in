## Project Proposal

### An ArcGIS Python tool for previewing significant changes between two raster datasets

This Python tool for ArcGIS allows a user to quickly preview significant changes between two raster datasets. 

### Background

> On May 6, 2018, about 1338 mountain standard time, a Grumman TBM-3E airplane, N337VT, is presumed to have impacted terrain following the bailout of the pilot and passenger due to a partial loss of engine power about 8 miles southwest of Mount Baldy, on the Fort Apache Reservation, Arizona. 
--[NSTB event ANC18LA034](https://www.ntsb.gov/_layouts/ntsb.aviation/brief.aspx?ev_id=20180507X34747)

The airplane is assumed to still be intact and somewhere in the mountains of Fort Apache Reservation, Arizona. The [owner has asked for public help](http://tbmavenger.blogspot.com/2018/06/tbm-avenger-lost-in-white-mountains-of.html) in locating the plane. Multi-spectral imaging using modern satellites may be able to assist with this search as the potential crash area upwards of 30,000 acres is much too great to manually search at low cost. 

Using multi-spectral imagery taken before and after the crash, the plane may be found by comparing multiple small square areas of each raster. 

Significant changes will be measured by the difference in standard deviation between user defined square size nxn of both rasters. The user will then specify the standard deviation difference cutoff and all squares with a greater standard deviation will be displayed in a custom Python GUI browser navigable by buttons or keyboard. The GUI will be faster than scrolling in ArcGIS because images will be presented one at a time to the user. This frees the user from needing to keep track of where they are inspecting in the massive search area and focus on analyzing the images with significant changes. 

### Data and parameters

The only required data are two raster images for the same geographic area. The user will define the size of the square area to calculate standard deviation for as well as the standard deviation difference cutoff to preview areas in the GUI. 

The output datasets will be raster images of areas with significant change between the two raster images. Rasters containing standard deviation calculations 


### Limitations

1. Calculating standard deviation for a large area may take a large amount of memory and time. 

2. Editing the raster may require use of an external Python library such as GDAL. 

3. Python GUI may need an external Python library such as tkinter or qt. 

3. Launching the Python GUI as part of the processing workflow may not be supported by ArcPy.

## Solution

1. Smaller raster images will be used for testing and the larger raster datasets may need to be manually broken up before being fed into this tool.

2. The user will need to install a compatible version of GDAL.

3. The user will need to install a compatible GUI library. If Python GUI cannot be created, significant change areas will be marked on the map in ArcGIS so that users can still do analysis. 

4. If Python GUI cannot be launched from ArcPy, it can be bundled as a separate script to be run outside of ArcGIS. 