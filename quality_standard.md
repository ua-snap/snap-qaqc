# SNAP Quality Data Standard

## Abstract

This standard describes a formalized ideal of what high quality data means for SNAP. It applies to the **dataset**, or **data product**, a high-level grouping of one or more data files (assets) that were usually (always?) produced by the same data generating process. In practice, it will likely not always be guaranteed because it is not realistic to perform the human-in-the-loop checks (e.g., "does this seem right?") on all files for datasets consisting of many files or large, multidimensional files. However, this ideal is useful nonetheless because it serves as a benchmark that can be reasonably approximated in most cases. In fact, this standard serves as the basis for what the [SNAP QA/QC protocol](qaqc.ipynb) is designed to approximate with the datasets it is used for.

## 1. All data files load and work as expected in typical software

This depends on both the file type and software. 

### 1.1.  NetCDF

#### `ncdump`  

1.1.1. Opening the files with the `ncdump` command line tool returns header info, coordinate data, and data variable data

#### `GDAL`

1.1.2. Opening the files with the `gdalinfo` command line tool returns header info with expected coordinate system

#### Python `xarray` / `rioxarray`  

1.1.3.  Opening the files with `xarray.open_dataset` function creates an xarray.DataSet object  
1.1.4.  Data variable values successfully read into memory with the `xarray.DataArray.sel` method for all data variables  
1.1.5.  Calling the `rioxarray` accessor functions of `set_spatial_dims` and `set_crs` on an open `xarray` dataset is creates a new dataset that is correctly georeferenced, which is validated via plotting in the context of a vetted geospatial dataset opened with `geopandas` or `rasterio`  

#### QGIS

1.1.6. Opening the files in QGIS displays them as expected in relationship to another vetted geospatial dataset

**Note** - QGIS shall serve as a proxy for the ESRI suite of “typical software”, given it is FOSS and cross-platform.

#### NCL

1.1.7. Opening the files into NCL correctly georeferences the data files..TBC

#### Panoply

1.1.8. Opening the files into NCL correctly georeferences the data files..TBC

### 1.2. GeoTIFF

#### GDAL

1.2.1. Opening the files with the gdalinfo command line tool returns header info with expected coordinate system

#### Python `rasterio`

1.2.2. The files open as a `rasterio.io.DatasetReader` class via `rasterio.open`
1.2.3. The `rasterio.io.DatasetReader` class has a valid `.meta` property with header info  
1.2.4. The `rasterio.io.DatasetReader` class has a valid `.crs` property  

#### QGIS

1.2.5. Opening the files in QGIS displays them as expected in relationship to another vetted geospatial dataset

### 1.3. CSV

#### Python `pandas`

1.3.1. The files open and display data using the `pandas.read_csv` function

### 1.4. All file types

1.4.1. All files have at least *some* valid data

## 2. Data are within a valid range and have been statistically screened

2.1. Data are within a valid range based on common sense (e.g., no negative values for a precipitation dataset unless a specific scaling / transformation is defined in the metadata)
2.2. A statistical screening* has occurred to identify potentially problematic data files that may be indicative of corruption, human error, etc. All results of this shall be readily available for reference.

*This screening will be highly context-dependent so it is difficult to make general remarks here, but the following things will have been evaluated and results discussed with domain experts where feasible.
* intrafile summary stats (mean/min/max/range/variance/quartiles)
* interfile summary stats (mean/min/max/range/variance/quartiles)
* histogram analysis
* spatial and temporal variance
* spatial and temporal autocorrelation
* PSNR, etc. measures of image quality

## 3. Consistent data types, nodata values, and precision **within and between** datasets

#### Within datasets, there is only one:

3.1. data type used in the dataset unless required otherwise  
3.2. nodata value used in the dataset  
3.3. compression type and level 

#### Between datasets

3.4. Data types and nodata values should conform to [SNAP's data type & nodata conventions](#Appendix-1:-SNAP-data-type-&-nodata-conventions)

## 4. External and file metadata are valid and match metadata collection notebook

4.1. External (e.g. XML) metadata is valid according to GeoNetwork (currently only use case for this is ISO-19115 metadata)  
4.2. File metadata is valid according to some vetted source 
    4.2.1. NetCDF file metadata is validated as CF-compliant by [CEDA's CF Checker utility](https://github.com/cedadev/cf-checker)
4.3. External metadata includes thorough descriptions of variables / fields / etc
4.4. Missing data files, such as a seemingly missing year in a dataset containing files grouped and named by year, are noted in the external metadata
4.5. File naming scheme is explained in the external metadata and is accurate

## 5. File and variable naming scheme is consistent

This section applies to datasets consisting of multiple files.

5.1. File names shall be structured in a consistent format, preferring the use of underscores for separating logical descriptors
5.2. Variable names used in files shall be consistent

## Appendix 1: SNAP data type & nodata conventions

#### Data types

The data type for a given dataset should be chosen to strike a balance between usability and memory efficiency. A dataset is less usable if every file needs to be transformed to a different type prior to processing. A dataset is less memory efficient if its datatype accommodates a much greater range of values than are realistic for the information being stored.

The preference for all numeric datasets is 32- and 64-bit integer and floating point types. The smaller type should be preferred, so 64-bit data types should be used only as the amount of necessary significant digits increases enough to warrant it. However, this is a soft standard for now (i.e. no quality red flag) as we recognize that system defaults are usually 64-bit.

In special cases of large datasets, the usability-efficiency balance may be tipped in favor of smaller integer types along with a scaling factor to represent floating point information. Fro example, if the information being stored only ranges from -5 to 5, with a precision of 1 decimal places, and utilizes > 50GB when stored as a 32-bit float, these could be represented as 16-bit integers with a scaling factor of 100.

#### Nodata values

Datasets should prefer -9999-based values if valid values are always greater than -9999. This is because it is a common, practical convention in many scientific fields. Otherwise, we suggest values based on the [netCDF default fill values](https://www.unidata.ucar.edu/software/netcdf/documentation/4.7.4-pre/file_format_specifications.html):

| data type | nodata value | preference rank |
| - | - | - |
| 16, 32-, 64-bit integer | -9999 | 1 |
| 32-, 64-bit float | -9999.0 | 1 |
| 32-bit integer | -32767 | 2 |
| 64-bit integer | -2147483647 | 2 |
| 32-, 64-bit float | 9.9692099683868690e+36| 2 |
