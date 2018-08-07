import pandas as pd
import numpy as np
import netCDF4 as nc4
from datetime import datetime
import os

def attributes(self, name=None):
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

def seperate_13(table):
    xx = list(table.columns.values)
    for i in range(0,len(xx)):
        if table[xx[i]][0] == 'NaN':
            i+=1
        else:
            if 'surface_directional' in xx[i]:
                table[xx[i].split('_')[0]+'dir_nodes'],table['e'],table['ene'],table['ne'],table['n'], table['nw'], table['wnw'], table['w'], table['wsw'],table['sw'], table['s'], table['se'], table['ese'] = table[xx[i]].str.split(' ', 0).str
                table = table.drop(xx[i],1)
            else:
                table[xx[i].split('_')[0]+'nodes'], table[xx[i].split('_')[0]+'data'] = table[xx[i]].str.split(' ', 1).str
                table = table.drop(xx[i],1)
    return table


def read_fort15(self):
    content,descr,var = [], [],[]
    with open(self.fp, 'r') as fin:
        lines = fin.readlines()
        for line in lines:
            if '!' in line:
                data = line.split('!')
                var.append(data[0].strip())
                param= data[1].split('-')[0].replace('\n','')
                descr.append(param)
    content = np.reshape(var,(1,len(var)))
    table = pd.DataFrame(content,columns=descr) 
    
    return table

def initnc4(netcdf_path, fort14, lon='lon',lat='lat'):
    f = nc4.Dataset(os.path.join(netcdf_path,'input_fort.nc'),'w',format='NETCDF4')
    temp = f.createGroup('fort14')
    variable1 = ['lat','lon','value']
    header1   = ['Latitude','Longitude','Elevation']   
    for y in range(0,len(variable1)):
        temp.createDimension(variable1[y],len(fort14[variable1[y]]))
        variab1 = temp.createVariable(header1[y],'f4',variable1[y],zlib=True)
        variab1[:]= fort14[variable1[y]].values
    temp.createDimension('nodes', len(fort14['node_id']))
    temp.createDimension('time', None)
    nodes = temp.createVariable('nodes','i4','nodes', zlib=True)
    time = temp.createVariable('Time', 'i4', 'time', zlib=True)
    nodes[:]     = fort14['node_id'].values
    time.units      = 'days since July 24'
    nodes.units   = 'none'
    today = datetime.today()
    time_n= today.toordinal()
    time[0]= time_n
    f.history     = 'Created ' + today.strftime('%d/%m/%y')
    f.close()
    return

def add_attribute2nc4(netcdf_path, table, attr, lon='lon',lat='lat',surf='0'):
    head = list(table)
    variable = ['lat','lon','value','e','ene','ne','n','nw',
                'wnw','w','wsw','sw','s','se','ese']
    header   = ['Latitude','Longitude','Elevation','E','ENE',
                'NE','N','NW','WNW','W','WSW','SW','S','SE','ESE']
    variable1 = ['lat','lon','value',head[-1]]
    header1   = ['Latitude','Longitude','Elevation','data']
    f=nc4.Dataset(os.path.join(netcdf_path,'input_fort.nc'),'r+')
    for i in range(0,len(attr['Parameter'])):
        if int(surf) !=0:
            temp = f.createGroup('surface_directional_effective_roughness_length')
            for x in range(0,len(variable)):
                temp.createDimension(variable[x],len(table[variable[x]]))
                variab = temp.createVariable(header[x],'f4',variable[x],zlib=True)
                variab[:]= table[variable[x]].values
            temp.createDimension('nodes',len(table['node_id']))
            nodes= temp.createVariable('nodes','S1','nodes',zlib=True)
            nodes[:]      = table['node_id'].values
            f.close()
            break
        else:
            for ii in range(0,len(head)):
                if attr['Parameter'][i].split('_')[0]==head[ii].split('nodes')[0]:
                    if attr['Parameter'][i]=='surface_directional_effective_roughness_length' and head[ii]!='surfacedir_nodes':
                        i+=1

                    else:                         
                        temp = f.createGroup(attr['Parameter'][i])
                        for y in range(0,len(variable1)):
                            temp.createDimension(variable1[y],len(table[variable1[y]]))
                            variab1 = temp.createVariable(header1[y],'f4',variable1[y],zlib=True)
                            variab1[:]= table[variable1[y]].values    
                        temp.createDimension('nodes',len(table['node_id']))
                        nodes= temp.createVariable('nodes','S1','nodes',zlib=True)
                        nodes[:]      = table['node_id'].values
                        f.close()
                        break
    return










