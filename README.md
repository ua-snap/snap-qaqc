# Quality Assurance and Quality Control resources for SNAP datasets

This codebase has three purposes:

1. Describe the official [SNAP Data Quality Standard](quality_standard.md) for geospatial data products
2. Provide the official [SNAP QA/QC Protocol](qaqc.ipynb) and requisite [metadata protocol](metadata.ipynb)
3. Provide a python package with useful tools for executing the SNAP QA/QC protocol (the `snap_qaqc` packge herein - forthcoming)

## Quality Data Standard

The [`quality_standard.md`](quality_standard.md) contains SNAP's Quality Data Standard. It is a set of rules that collectively define the ideal for what SNAP considers to be quality data.

## QA/QC Protocol

The Standard is the ideal, and the protocol is what we use to evaluate how close a particular data product is to that ideal. The SNAP QA/QC protocol is manifest as a [Jupyter notebook](qaqc.ipynb) with template python code, but all of the steps are in english and so it is language agnostic.
