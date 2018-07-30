# ADCIRC
<img style="float:right;" src="https://github.com/tmiesse/adcirc_prod/blob/master/extra/figures/DewberryLogo_RGB.png" width=150px>


## Contents:
- Notebooks
    1. [Model QC tool](https://github.com/tmiesse/adcirc_prod/blob/master/notebooks/ModelQC__v2.ipynb)
    2. [NOAA Tide Gauge](https://github.com/tmiesse/adcirc_prod/blob/master/notebooks/noaa_tide.ipynb)
    3. [Subdomains](https://github.com/tmiesse/adcirc_prod/blob/master/notebooks/subdomain.ipynb)
    4. [Create Fort.15](https://github.com/tmiesse/adcirc_prod/blob/master/notebooks/create_fort15.ipynb)
- py_scripts:
    1. Dewberry's custom python library for adcirc applications
- Data:
    1. Example NETCDF data for model QC notebook

## Description:
Perform astronomic tide simulations and a series of storm surge runs to calibrate and validate 
the UnSWAN+ADCIRC model. The study mesh to be used is that which was developed as part of the 
sensitivity work which added increased mesh resolution in the study areas and updated the topography
and bathymetry. Simulated astronomic tides and hurricane storm surge will be compared against verified
tidal constituents maintained by NOAA, tidal elevation hydrographs, and historic storm surge high water
marks (HWMs) to ensure the model is reasonably reproducing the hydrodynamic behavior within the study area.












