"""Utility functions for working with this package"""

import os
import shutil
import site
from pathlib import Path


def copy_protocols():
    """Copy the QAQ/QC and Metadata Collection 
    protocol notebooks into the calling directory
    
    Not working yet!
    """
    pkgdir = Path(site.getsitepackages()[0]).joinpath("snap_qaqc")
    shutil.copy(pkgdir.joinpath("qaqc.ipynb"), os.getcwd())
    shutil.copy(pkgdir.joinpath("metadata.ipynb"), os.getcwd())
    