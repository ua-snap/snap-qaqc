"""Utility functions for working with this package"""

import os
import shutil
import site
from pathlib import Path
from osgeo import gdal


def gdalinfo_equal(check_fp, ref_fp, crs_varname=None):
    """Compare the gdalinfo output for two files to see if they match.
    
    Args:
        check_fp (path_like): path to file to check gdalinfo for
        ref_fp (path_like): path to file to check gdalinfo against
        crs_varname (str): name of the variable that contains the CRS attributes. 
            This variable should be equal across assets in a dataset. 

    Returns:
        info_equal (bool): True if the file attributes and metadata match, False if not
    """
    assert Path(check_fp).suffix == Path(ref_fp).suffix
    # get gdalinfo for both
    check_info = gdal.Info(check_fp, format="json")
    ref_info = gdal.Info(ref_fp, format="json")

    # append results of equality tests to a tracker list
    results = {}
    # check metadata separately because it is a dict itself
    # mysterious '' key contains the global attributes and attributes
    #  of the coordinate variables - values are not expected to be equal,
    #  but keys should be.
    results["meta_keys_match"] = list(check_info["metadata"][""].keys()) == list(
        ref_info["metadata"][""].keys()
    )
    # There should be one variable with equal values: whatever variable contains the CRS attributes
    if results["meta_keys_match"] & (crs_varname is not None):
        # only do this test if the metadata key names are even the same between files
        crs_keys = [key for key in ref_info["metadata"].keys() if crs_varname in key]
        try:
            results["crs_var_attrs_match"] = [
                check_info["metadata"][key] == ref_info["metadata"][key]
                for key in crs_keys
            ]
        except KeyError:
            results["crs_var_attrs_match"] = False
    else:
        # omit crs_var_attrs_match if keys don't match or crs_varname is not specified
        pass

    # files should have the same driverShortName, size, coordinateSystem,
    #  geoTransform, metadata should be mostly equal except for list of
    #  specified field names
    # this should be a super-set of the possible keys that could be
    #  present that should be equal across files in a dataset. E.g. "extent"
    #  might be present, but not "wgs84Extent", and vice versa.
    base_keys = [
        "driverShortName",
        "size",
        "coordinateSystem",
        "geoTransform",
        "cornerCoordinates",
        "wgs84Extent",
        "extent",
    ]
    ref_keys = [key for key in base_keys if key in list(ref_info.keys())]
    for key in ref_keys:
        result_key = f"{key}_match"
        try:
            results[result_key] = check_info[key] == ref_info[key]
        except KeyError:
            # set False if key not in check_info
            results[result_key] = False

    info_equal = all(list(results.values()))

    return info_equal


def copy_protocols():
    """Copy the QAQ/QC and Metadata Collection 
    protocol notebooks into the calling directory
    
    Not working yet!
    """
    pkgdir = Path(site.getsitepackages()[0]).joinpath("snap_qaqc")
    shutil.copy(pkgdir.joinpath("qaqc.ipynb"), os.getcwd())
    shutil.copy(pkgdir.joinpath("metadata.ipynb"), os.getcwd())
    
