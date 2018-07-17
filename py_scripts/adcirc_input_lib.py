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
#import h5py
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



# Find columns in variable sized table
def find_columns(data):
    data2 = []
    for f in data.split(' '):
        if f != '':
            data2.append(f)   
    return data2


# Find the attributes within a fort.13
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


# Create a table for fort.13 with the nodes used for each attribute
def read_fort13(path13, attribute):
    a = dt.now()
    print("\n Started finding nodes in attributes at \n") 
    print(a)
    x = 0
    table_v2 = pd.DataFrame()
    with open(path13, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if attribute[-1] in line:
                start_read_line = i+4
                break
    for x in range(len(attribute)):
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
                    if i>nodes:
                        nodes=i+nodes
                    for ii in range(i,nodes):
                        line = lines[ii]
                        table13.append(line.split('\n')[0])
                    get_count = False
                    idx+=1
    
        data = []
        if len(table13) == 0:
            data.append('NaN')
            
        for i in range(len(table13)): 
            data.append(table13[i])   
        if len(table_v2) == 0:
            table_v2 = pd.DataFrame(data)
            table_v2.columns=[attribute[x].split('_')[0]+'_'+attribute[x].split('_')[1]]
        else:
            table_v3 = pd.DataFrame(data)
            table_v3.columns=[attribute[x].split('_')[0]+'_'+attribute[x].split('_')[1]]
            table_v2 = pd.concat([table_v2,table_v3],axis=1,sort=False)
    b = dt.now()
    c = b-a
    print("===========END========== \n")
    print("Processing Time : ")
    print(c)  
    return table_v2 


# Create a table for Fort.14
def read_fort14(path):
    nodesx, nodesy, value, node_id, node_name, loc = [], [], [], [], [], []
    with open(path, 'r') as f:
        lines = f.readlines()
    for i in range(0,len(lines)):
        line = lines[i]
        nodes = int(lines[1].split(' ')[2])
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





























