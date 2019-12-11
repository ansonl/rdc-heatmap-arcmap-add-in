## Significant Relative Difference Highlighter

### An ESRI ArcMap Add-In for highlighting significant changes between two raster datasets

This add-in for ArcGIS allows a user to quickly preview significant changes between two raster datasets based on relative difference in contrast (r.d.c.). NDVI, OSAVI, and MSAVI2 index methods are selectable as processing options before calculating r.d.c. Cells with significant changes are classified in an output raster based on how many standard deviations away from mean r.d.c. each cell's r.d.c. is between the two overlapping input rasters. A single raster may also be highlighted based on its band 1 values' standard deviation distance away from band 1 mean with a special index option. 

Additionally, there is a tool in this add-in to strip backgrounds from rasters and replace the 0 value backgrounds with NODATA values to assist with accurate calculations.

![raster-highlighter-demo-screenshot](https://gitlab.com/ansonl/significant-change-preview/raw/master/demo_screenshot.PNG)

### Backstory

> On May 6, 2018, about 1338 mountain standard time, a Grumman TBM-3E airplane, N337VT, is presumed to have impacted terrain following the bailout of the pilot and passenger due to a partial loss of engine power about 8 miles southwest of Mount Baldy, on the Fort Apache Reservation, Arizona. 
--[NSTB event ANC18LA034](https://www.ntsb.gov/_layouts/ntsb.aviation/brief.aspx?ev_id=20180507X34747)

The airplane is assumed to still be intact and somewhere in the mountains of Fort Apache Reservation, Arizona. The [owner has asked for public help](http://tbmavenger.blogspot.com/2018/06/tbm-avenger-lost-in-white-mountains-of.html) in locating the plane. Multi-spectral imaging using modern satellites may be able to assist with this search as the potential crash area upwards of 30,000 acres is much too great to manually search at low cost. 

The `sample_data` folder contains day and night Landsat 8 Band 11 (TIRS 2) [thermal] data in Apache County, AZ clipped to the probable crash site of N337VT.

### Installation

1. Clone this repository.

2. Double cick the `change_finder.esriaddin` file inside the `change-finder` folder. 

3. Restart ArcMap.

4. Enable the **Relative Difference Highlighter** add-in under Customize > Add-In Manager.

5. Enable the **Change Finder** toolbar under Customize > Toolbars.

*This add-in requires a Spatial Analyst license due to raster calculations.*

### Usage

![raster-highlighter-add-in-screenshot](https://gitlab.com/ansonl/significant-change-preview/raw/master/add-in_screenshot.PNG)

The only required data are two overlapping raster images for the same geographic area. 

1. Select two raster layers to compare one at a time and click the appropriate "Select raster" button to save your selection.

2. Select an index method to use and define the size of the rectangle area to apply the index method to. If you only want to highlight significant band 1 values of a single raster and not calculate r.d.c., select "Band 1 (raster 1)" index method. 

3. Highlight significant relative difference in contrast (r.d.c.). 

The output dataset will be a raster containing the area cells' relative difference in contrasts and a raster classifying cells in the area based on how many standard deviations away from mean r.d.c. each cell's r.d.c. is. 

To strip backgrounds from rasters with 0 value backgrounds, select the raster and click the remove background tool. The new raster will be saved to the same directory as the original raster with `-noBG` appended to the filename.