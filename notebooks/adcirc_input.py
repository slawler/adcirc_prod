import pandas as pd
import numpy as np
import netCDF4 as nc4
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.tri as tri
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import FancyArrowPatch
from matplotlib.animation import FuncAnimation




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

def read_fort13(self, attribute):
    x = 0
    table_v2 = pd.DataFrame()
    with open(self.fp, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if attribute['Parameter'].iloc[-1] in line:
                start_read_line = i+4
                break
    for x in range(len(attribute['Parameter'])):
        with open(self.fp, 'r') as f:
            idx=0
            get_count = False
            lines = f.readlines()
            table13 = []
            for i, line in enumerate(lines):
                if i < start_read_line:
                    continue

                elif attribute['Parameter'][x] in line:
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
            table_v2.columns=[attribute['Parameter'][x].split('_')[0]+'_'+attribute['Parameter'][x].split('_')[1]]
        else:
            table_v3 = pd.DataFrame(data)
            table_v3.columns=[attribute['Parameter'][x].split('_')[0]+'_'+attribute['Parameter'][x].split('_')[1]]
            table_v2 = pd.concat([table_v2,table_v3],axis=1,sort=False)
    return table_v2

    
def read_fort14(self):
    nodesx, nodesy, value, node_id, node_name, loc = [], [], [], [], [], []
    with open(self.fp, 'r') as f:
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
    
    
def tide_data(begin_d, end_d, station):
    website = r'https://tidesandcurrents.noaa.gov/api/'
    datum = 'datum=NAVD'
    units = 'units=metric'
    timez = 'time_zone=LST'
    form = 'format=csv'
    app = 'datagetter?product=hourly_height&application=NOS.COOPS.TAC.WL'
    domain = website + app + '&' + station + '&' + begin_d + '&' + end_d + '&' + datum + '&' + units + '&' + timez + '&' + form
    return domain    
    
def noaa_plot(datasets, obs, dtm, title):
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    