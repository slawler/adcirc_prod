
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





def MakeDomain(begin_d, end_d, station):
    website = r'https://tidesandcurrents.noaa.gov/api/'
    datum = 'datum=NAVD'
    units = 'units=metric'
    timez = 'time_zone=LST'
    form = 'format=csv'
    app = 'datagetter?product=hourly_height&application=NOS.COOPS.TAC.WL'
    domain = website + app + '&' + station + '&' + begin_d + '&' + end_d + '&' + datum + '&' + units + '&' + timez + '&' + form
    return domain





def MakePlot(datasets, obs, dtm, title):
    
    data = list()
    for dataset in datasets:
        water_level = dataset.loc[:,obs]
        date = dataset.loc[:,dtm]
        c_list = ['rgb(51, 204, 51)','rgb(0, 255, 204)',
                      'rgb(0, 204, 255)','rgb(102, 255, 255)',
                      'rgb(0, 102, 153)','rgb(0, 0, 255)',
                      'rgb(51, 51, 255)','rgb(102, 0, 255)',
                      'rgb(153, 153, 255)','rgb(204, 0, 255)',
                      'rgb(255, 51, 204)','rgb(204, 0, 0)',
                      'rgb(255, 153, 0)','rgb(204, 255, 51)',
                      'rgb(0, 153, 0)']
        for x in range(1):
                y=random.randint(1,14)

#                print(y)
                color = c_list[y]
                
        trace = go.Scatter(
                x = date,
                y = water_level,
                name = dataset.name,
                        line = dict(
                        color = color,
                    ))
        data.append(trace)

    layout = go.Layout(dict(title = title),
                  xaxis = dict(title = 'Time'),
                  yaxis = dict(title = 'Water level (m) above NavD88'),                     
                  legend= dict(orientation = "h"),
                  font = dict(color = 'rgb(255,255,255)'),
                  paper_bgcolor = 'rgb(0,0,0)',
                  plot_bgcolor = 'rgb(0,0,0)',
                      )
    
    return data, layout





def read_fort63(path, nodes):
    ''''---Enter Nodes of Interest in the nodes dictionary---'''

    #------------------------------BEGIN SCRIPT----------------------------------#
    a = dt.now()
    print("\n Started reading Global File at \n") 
    print(a)
    table = []
    f = fileinput.input(path)
    
    for line in f:
        n = line.strip().split(' ')[0] 
        if n in nodes:
            nodes[n].append(line)
    
    for n in nodes:    
        output = open('extracted_%s.txt' %(n),'w')
        header = "      NODE                  SWEL\n"
        output.write(header)
        for i in range(len(nodes[n])):
            output.write(nodes[n][i])
               
    table = nodes   
    output.close(); fileinput.close()
    
        
    b = dt.now()
    c = b-a
    print("===========END========== \n")
    print("Processing Time : ")
    print(c)
    
    return table




def clean_fort(dt, table):
    duke,duke2 = [], []
    wright, wright2 = [], []
    hatt, hatt2 = [], []
    table1,table2,table3 =[], [], []
    table1 = table['324363']
    table2 = table['116637']
    table3 = table['72148']

    for i in range(len(dt)):
        duke.append(table['324363'][i].strip().split('\n')[0])
        duke2.append(float(duke[i].split('324363  ')[1]))
    adc_duke = pd.DataFrame(duke2)
    adc_duke.name = "Beaufort ADCIRC"
    adc_duke.columns = [' Water Level']
    adc_duke.insert(0,'Date Time',dt)    
    for i in range(len(dt)):
        wright.append(table2[i].strip().split('\n')[0])
        wright2.append(float(wright[i].split('116637  ')[1]))
    adc_wright = pd.DataFrame(wright2)
    adc_wright.name = 'Wrightsville ADCIRC'
    adc_wright.columns = [' Water Level']
    adc_wright.insert(0,'Date Time',dt)   
    for i in range(len(dt)):
        hatt.append(table3[i].strip().split('\n')[0])
        hatt2.append(float(hatt[i].split('72148  ')[1]))
    adc_hatt = pd.DataFrame(hatt2)
    adc_hatt.name = 'Hatteras ADCIRC'
    adc_hatt.columns = [' Water Level']
    adc_hatt.insert(0,'Date Time',dt)
    return adc_duke,adc_wright,adc_hatt




def find_hurricanes(root_adc,hurricanes):
    adcirc1, adcirc0, fort_loc = [],[],[]
    for i in range(len(hurricanes)):
        fort_loc.append(glob(os.path.join(root_adc, "**", hurricanes[i],"**","fort.63"), recursive=True))

        for fort in fort_loc[i]:
            if 'adcirc.1' in fort:
                adcirc1.append(fort)
            else:
                adcirc0.append(fort)
    return adcirc0,adcirc1





def create_map(center, zoom, markers):
    
    m = Map(center=center, zoom=zoom)
    m.add_layer(basemaps.Esri.WorldStreetMap)
    for i in range(len(markers)):    
        m+=Marker(location=markers[i])
    return m





def find_columns(data):
    data2 = []
    for f in data.split(' '):
        if f != '':
            data2.append(f)   
    return data2




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



def read_fort13(path13, attribute, attribute1):
    a = dt.now()
    print("\n Started finding nodes in attributes at \n") 
    print(a)
    x = 0
    node = []
    data = np.array([])
    table13 = []
    with open(path13, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if attribute[-1] in line:
                start_read_line = i+4
                break
            
    with open(path13, 'r') as f:
        idx=0
        get_count = False
        lines = f.readlines()
    
        for i, line in enumerate(lines):
            if i < start_read_line:
                continue
            
            elif attribute1 in line:
                attr = line
                get_count = True
            
            elif get_count:
                nodes = int(line)
                i+=1
                for ii in range(i,nodes):
                    line = lines[ii]
                    table13.append(line.split('\n')[0])
                get_count = False
                idx+=1

    data = np.empty((nodes))
    for i in range(len(table13)):
        node.append(table13[i].split(' ')[0])    
        data[i] = table13[i].split(' ')[1]   
    b = dt.now()
    c = b-a
    print("===========END========== \n")
    print("Processing Time : ")
    print(c)              
    return node, data





def read_fort14(path):
    nodesx, nodesy, value, node_id, node_name, loc = [], [], [], [], [], []
    with open(path, 'r') as f:
        lines = f.readlines()
    for i in range(0,len(lines)):
        nodes= int(lines[2].split(' ')[1])
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











