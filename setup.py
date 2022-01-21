from setuptools import setup

setup(
    name="snap_qaqc",
    version="0.1.0",
    author="Scenarios Network for Alaska and Arctic Planning",
    author_email="uaf-snap-data-tools@alaska.edu",
    packages=["snap_qaqc"],
    url="https://github.com/ua-snap/snap-qaqc",
    license="LICENSE.txt",
    description="A package providing functions and notebooks for conducting QA/QC on geospatial data products",
    long_description=open("README.md").read(),
    install_requires=[
        "gdal", "xarray", "rasterio", "numpy", "pandas", "matplotlib"
    ],
    scripts=["bin/startqaqc.py"],
)
