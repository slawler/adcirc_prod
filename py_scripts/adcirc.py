# ADCIRC python library
# Author: Tyler Miesse

'''
    ADCIRC Functions
    attributes_fort13
    read_fort13
'''

import pandas as pd
import numpy as np
from importlib import reload
import adcirc_input_lib ; reload(adcirc_input_lib)
from adcirc_input_lib import *

class adcirc:
    
    def __init__(self,path, file):
        self.path = path
        self.file = file
        self.fp   = os.path.join(self.path,self.file)
        
        
    def attributes(self, name='none'):
        attributes =['primitive_weighting_in_continuity_equation',
                     'surface_submergence_state','quadratic_friction_coefficient_at_sea_floor',
                     'surface_directional_effective_roughness_length',
                     'surface_canopy_coefficient','bridge_pilings_friction_paramenters',
                     'mannings_n_at_sea_floor','chezy_friction_coefficient_at_sea_floor',
                     'sea_surface_height_above_geoid','wave_refraction_in_swan','bottom_roughness_length',
                     'average_horizontal_eddy_viscosity_in_sea_water_wrt_depth','elemental_slope_limiter',
                     'advection_state','initial_river_elevation']
        attribute = []
        with open(self.fp, 'r') as f:
            lines = f.readlines()
            for line in lines:
                for i in range(0,len(attributes)):
                    if line.find(attributes[i])>-1 and attributes[i] not in attribute:
                        attribute.append(attributes[i])      
        t_attrib = pd.DataFrame(attribute)
        t_attrib.columns = ['Parameter']
        if name != 'none':
            t_attrib = t_attrib[t_attrib['Parameter'].str.contains(name)]
        return t_attrib

        
    def read_fort13(self, attribute):
        a = dt.now()
        print("\n Started finding nodes in attributes at \n") 
        print(a)
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
        b = dt.now()
        c = b-a
        print("===========END========== \n")
        print("Processing Time : ")
        print(c)  
        return table_v2 
        
        
        
    # Create a table for Fort.14
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

    def seperate_13(table):
        xx = list(table.columns.values)
        for i in range(0,len(xx)):
            if table[xx[i]][0] == 'NaN':
                i+=1
            else:
                if 'surface_directional' in xx[i]:
                    table[xx[i].split('_')[0]+'dir_nodes'],table['e'],table['ese'],table['se'],table['s'], table['sw'], table['wsw'], table['w'], table['wnw'],table['nw'], table['n'], table['ne'], table['ene'] = table[xx[i]].str.split(' ', 0).str
                    table = table.drop(xx[i],1)
                else:
                    table[xx[i].split('_')[0]+'nodes'], table[xx[i].split('_')[0]+'data'] = table[xx[i]].str.split(' ', 1).str
                    table = table.drop(xx[i],1)
        return table
        