#!bin/bash
module unload python3 python2
export PATH=$HOME/anaconda3/bin:$PATH
#conda install -c anaconda nodejs 
conda install jupyterlab
conda install -c conda-forge ipyleaflet 
conda install -c conda-forge jupyterlab_launcher
conda install -c conda-forge jupyter_core
conda install -c conda-forge jupyter_contrib_nbextensions
conda install -c conda-forge jupyter_nbextensions_configurator
conda install -c conda-forge jupyter_dashboards
#conda install -c conda-forge plotly
conda install -c plotly plotly
conda install -c anaconda basemap
conda install -c anaconda netcdf4
conda install -c anaconda ipython
export PATH=$HOME:$PATH
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install @jupyterlab/plotly-extension
jupyter labextension install jupyter-leaflet
jupyter lab build
#
#
# problems with libraries in conda
# geoviews
# shapely
# more gis type libraries
# 
# these libraries give the error can't exceed disk quota
# this will end up causing anything python related to give errors
# 
# currently I either can get away with:
# conda clean --all
# or I have to uninstall anaconda then reinstall everything
#
# further problems may be errors trying to open or create a new notebook
# you need to delete hidden dir .jupyter, .ipython, and .local 
# then re generate them