import pandas as pd
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
import plotly.plotly as py
import plotly.offline as offline
import plotly.graph_objs as go
import numpy as np
from pathlib import Path
from scipy.integrate import trapz, cumtrapz, simps
import numpy as np
import os
from glob import glob
import requests
import json
from datetime import datetime
from collections import OrderedDict, defaultdict
from importlib import reload
import string
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import random
import fileinput
from datetime import datetime as dt
from  ipyleaflet  import *
import netCDF4



# read the fort.221 file to get the start and end dates of the simulations
def start_date(path):
    with open(path,'r') as f:
        for i in range(0,1):
            line = f.readline().strip().split()
            timestamp = line[3]
            start_date = datetime.strptime(timestamp,'%Y%m%d%H')
    return start_date

# read the netcdf fort file
def fort_nc(fort_nc):
    file1 = netCDF4.Dataset(fort_nc)
    lat  = file1.variables['y'][:]
    lon  = file1.variables['x'][:]
    gridfile=fort_nc
    gridvars = netCDF4.Dataset(gridfile).variables
    return file1, lat, lon, gridvars

# Find the parameters used in the fort.13 
def attributes_fort13(path):
    attributes =['primitive_weighting_in_continuity_equation','surface_submergence_state',
             'quadratic_friction_coefficient_at_sea_floor','surface_directional_effective_roughness_length',
             'surface_canopy_coefficient','bridge_pilings_friction_paramenters','mannings_n_at_sea_floor',
             'chezy_friction_coefficient_at_sea_floor','sea_surface_height_above_geoid',
             'wave_refraction_in_swan','bottom_roughness_length',
             'average_horizontal_eddy_viscosity_in_sea_water_wrt_depth','elemental_slope_limiter',
             'advection_state','initial_river_elevation']
    attribute = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            for i in range(0,len(attributes)):
                if line.find(attributes[i])>-1 and attributes[i] not in attribute:
                    attribute.append(attributes[i])      
    return attribute






# Read the values of the parameters in the fort.13
def read_fort13(path13, attribute):
    table_v2 = pd.DataFrame()  
    with open(path13, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if attribute[-1] in line:
                start_read_line = i+4
                break
    print("\n Started finding nodes at \n")
    a = dt.now()
    print(a)             
    for x in range(0,len(attribute)):
        with open(path13, 'r') as f:
            idx=0
            get_count = False
            lines = f.readlines()
            table13 = []
            for i, line in enumerate(lines):
                if i < start_read_line:
                    continue
                elif attribute[x] in line:
                    attr = line
                    get_count = True
                elif get_count:
                    nodes = int(line)
                    i+=1
                    if i > nodes:
                        nodes = i + nodes 
                    ii=0
                    for ii in range(i,nodes):
                        line = lines[ii]                    
                        table13.append(line.split('\n')[0])                    
                    get_count = False
                    idx+=1
        node, data = [],[]
        surface = []
        if len(table13) == 0:
            data.append('NaN')
            table_v3 = pd.DataFrame(data)
            table_v3.columns = [attribute[x].split('_')[0]]
            table_v2 = pd.concat([table_v2,table_v3],axis=1,sort=False)
        else:
            for y in range(len(table13)):
                data.append(table13[y])
            if len(table_v2) == 0:
                table_v2 = pd.DataFrame(data)
                table_v2.columns = [attribute[x].split('_')[0]]
            else:
                table_v3 = pd.DataFrame(data)
                table_v3.columns = [attribute[x].split('_')[0]+'_'+attribute[x].split('_')[1]]
                table_v2 = pd.concat([table_v2,table_v3],axis=1,sort=False)
    b = dt.now()
    c = b-a
    print("===========END========== \n")
    print("Processing Time : ")
    print(c)          
    return table_v2




# Find the columns in a different size table
def find_columns(data):
    data2 = []
    for f in data.split(' '):
        if f != '':
            data2.append(f)   
    return data2


# Generate a table of the nodes from the fort.14
def read_fort14(path):
    nodesx, nodesy, value, node_id, node_name, loc = [], [], [], [], [], []
    with open(path, 'r') as f:
        lines = f.readlines()
    for i in range(0,len(lines)):
        nodes= int(find_columns(lines[1])[1])
        line = lines[i]
        if i>1 and i<nodes+2:
            loc.append(line.strip().split('\n')[0])
    for i in range(len(loc)):
        node_id.append(find_columns(loc[i])[0])
        nodesx.append(find_columns(loc[i])[1])
        nodesy.append(find_columns(loc[i])[2])
        value.append(find_columns(loc[i])[3])
    node_name = {'node_id':node_id}
    table = pd.DataFrame(node_name)
    table.insert(1,'node_x',nodesx)
    table.insert(2,'node_y',nodesy)
    table.insert(3,'value',value)
    return table

# Find which nodes were used in the fort.13 file by comparing it with the fort.14
def compare_fort_nodes(node_num, table):
    nodesx2, nodesy2, value2, node_id2 = [], [], [], []
    a = dt.now()
    print("\n Started comparing nodes at \n") 
    print(a)
    
    for i in range(0,len(table)):
        if table['node_id'][i] in node_num:
            node_id2.append(table['node_id'][i])
            nodesx2.append(table['node_x'][i])
            nodesy2.append(table['node_y'][i])
            value2.append(table['value'][i])
    
    b = dt.now()
    c = b-a
    print("===========END========== \n")
    print("Processing Time : ")
    print(c)  

    return node_id2, nodesx2, nodesy2, value2



