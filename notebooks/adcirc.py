# ADCIRC python library
# Author: Tyler Miesse

'''
    ADCIRC Functions:
        attributes
        read_fort13
        read_fort14
        seperate_13
        initnc4
        add_attribute2nc4
        attr_plot
        plot_surf_dir
'''
import pandas as pd
import numpy as np
from importlib import reload
import adcirc_input_lib ; reload(adcirc_input_lib)
from adcirc_input_lib import *
import noaa_lib ; reload(noaa_lib)
from noaa_lib import *
import netCDF4 as nc4
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.tri as tri
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import FancyArrowPatch
from matplotlib.animation import FuncAnimation
from PIL import *
import glob


class adcirc:
    
    def __init__(self,path, file):
        self.path = path
        self.file = file
        self.fp   = os.path.join(self.path,self.file)
        
    
    def plot_hurricane(begin1, end1, stations, title1):
        begin = 'begin_date='+ begin1
        end   = 'end_date='+ end1
        hatt   = pd.read_csv(tide_data(begin, end, stations[0]['Hatteras']))
        duke   = pd.read_csv(tide_data(begin, end, stations[1]['Beaufort']))
        wright = pd.read_csv(tide_data(begin, end, stations[2]['Wrightsville']))
        hatt.name, duke.name, wright.name ='Hatteras','Beaufort', 'Wrightsville'
        datasets = [duke, wright, hatt]
        obs, dtm  = ' Water Level', 'Date Time'
        beg = begin.split('=')[1] + ' - ' + end.split('=')[1]
        title = title1 + ' ' + beg
        data, layout = noaa_plot(datasets, obs, dtm, title)
        
        return data, layout
    
    
    
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
                    table[xx[i].split('_')[0]+'dir_nodes'],table['e'],table['ene'],table['ne'],table['n'], table['nw'], table['wnw'], table['w'], table['wsw'],table['sw'], table['s'], table['se'], table['ese'] = table[xx[i]].str.split(' ', 0).str
                    table = table.drop(xx[i],1)
                else:
                    table[xx[i].split('_')[0]+'nodes'], table[xx[i].split('_')[0]+'data'] = table[xx[i]].str.split(' ', 1).str
                    table = table.drop(xx[i],1)
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
    
        
    def attr_plot(grp,title,ax,lat1,lat2,lon1,lon2,data='data',pixels='600'):
        x = grp.variables['Longitude'][:]
        y = grp.variables['Latitude'][:]
        #z = grp.variables['Elevation'][:]
        data = grp.variables[data][:]
        m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,urcrnrlon=lon2,resolution='h', epsg = 4269)
        m.drawcoastlines(color='k')
        m.arcgisimage(service='World_Street_Map', xpixels=int(pixels), verbose= False)
        plt.title(title+'\n')
        cmap = matplotlib.cm.get_cmap('viridis')  
        normalize = matplotlib.colors.Normalize(vmin=min(data), vmax=max(data))
        colors = [cmap(normalize(value)) for value in data]
        ax.scatter(x,y,marker = '.', color=colors, zorder=.25)
        cax, _ = matplotlib.colorbar.make_axes(ax)
        cbar = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap, norm=normalize)
        
        return plt.show()
    
        
    def plot_surf_dir(grp,lat1,lat2,lon1,lon2):
        x,y =0.225,0.225
        x2,y2,data2 = [],[],[]
        xx = grp.variables['Longitude'][:]
        yy = grp.variables['Latitude'][:]

        l1 = [(0,.75),(1,0.25)]
        l2 = [(.25,1),]
        (lx1,ly1) = zip(*l1)
        fig_title='Surface Directional Roughness Length'
        plt.text(.5, 1.40, fig_title,horizontalalignment='center',fontsize=40)

        ax1 = plt.subplot()
        ax1.grid(False)
        ax1.axis('off')
        # Arrows pointing in the 12 directions
        ax1.add_patch(FancyArrowPatch([0.5,0.8],[0.5,0.99],shrinkA=0,shrinkB=0,arrowstyle='simple',color='k',mutation_scale=40))
        ax1.add_patch(FancyArrowPatch([0.6,0.75],[0.68,0.95],shrinkA=0,shrinkB=0,arrowstyle='simple',color='k',mutation_scale=40))
        ax1.add_patch(FancyArrowPatch([0.63,0.63],[0.76,0.74],shrinkA=0,shrinkB=0,arrowstyle='simple',color='k',mutation_scale=40))
        ax1.add_patch(FancyArrowPatch([0.65,0.5],[0.8,0.5],shrinkA=0,shrinkB=0,arrowstyle='simple',color='k',mutation_scale=40))
        ax1.add_patch(FancyArrowPatch([0.63,0.37],[0.76,0.24],shrinkA=0,shrinkB=0,arrowstyle='simple',color='k',mutation_scale=40))        
        ax1.add_patch(FancyArrowPatch([0.6,0.25],[0.68,0.05],shrinkA=0,shrinkB=0,arrowstyle='simple',color='k',mutation_scale=40))
        ax1.add_patch(FancyArrowPatch([0.5,0.2],[0.5,0.01],shrinkA=0,shrinkB=0,arrowstyle='simple',color='k',mutation_scale=40))              
        ax1.add_patch(FancyArrowPatch([0.4,0.25],[0.32,0.05],shrinkA=0,shrinkB=0,arrowstyle='simple',color='k',mutation_scale=40))
        ax1.add_patch(FancyArrowPatch([0.37,0.37],[0.24,0.24],shrinkA=0,shrinkB=0,arrowstyle='simple',color='k',mutation_scale=40))
        ax1.add_patch(FancyArrowPatch([0.35,0.5],[0.20,0.5],shrinkA=0,shrinkB=0,arrowstyle='simple',color='k',mutation_scale=40))
        ax1.add_patch(FancyArrowPatch([0.37,0.63],[0.24,0.74],shrinkA=0,shrinkB=0,arrowstyle='simple',color='k',mutation_scale=40))        
        ax1.add_patch(FancyArrowPatch([0.4,0.75],[0.32,0.95],shrinkA=0,shrinkB=0,arrowstyle='simple',color='k',mutation_scale=40))       
        ax1.text(0.395,0.49,'Wind Direction',fontsize=27.5,color='k')
        ax0 = plt.axes([0,-.25, 1 , 1])
        ax0.grid(False)
        ax0.axis('off')
        
        ax2 = plt.axes([.40, .91, x , y])
        ax2.axis('off')
        data = grp.variables['N'][:]
        for i in range(0,len(xx)):
            if xx[i] > lon1 and xx[i] < lon2 and yy[i] > lat1 and yy[i] < lat2:
                x2.append(xx[i])
                y2.append(yy[i])
                data2.append(data[i])
        normalize = matplotlib.colors.Normalize(vmin=min(data2), vmax=max(data2))
        cax, _ = matplotlib.colorbar.make_axes(ax0,orientation='horizontal',anchor=(0.5,-1.25))
        cmap = matplotlib.cm.get_cmap('viridis')
        cbar = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap, norm=normalize, orientation='horizontal')
        cbar.ax.tick_params(labelsize=20) 
        colors = [cmap(normalize(value)) for value in data2]      
        ax2.scatter(x2,y2,marker = '.', color=colors, zorder=.25)
        
        ax3 = plt.axes([0.635, 0.86, x, y])
        ax3.axis('off')
        x2,y2,data2 = [],[],[]
        data = grp.variables['NE'][:]
        for i in range(0,len(xx)):
            if xx[i] > lon1 and xx[i] < lon2 and yy[i] > lat1 and yy[i] < lat2:
                x2.append(xx[i])
                y2.append(yy[i])
                data2.append(data[i])
        colors3 = [cmap(normalize(value3)) for value3 in data2]
        ax3.scatter(x2,y2,marker = '.', color=colors3, zorder=.25)
        
        ax4 = plt.axes([0.165, 0.86, x, y])
        ax4.axis('off')
        x2,y2,data2 = [],[],[]
        data = grp.variables['NW'][:]
        for i in range(0,len(xx)):
            if xx[i] > lon1 and xx[i] < lon2 and yy[i] > lat1 and yy[i] < lat2:
                x2.append(xx[i])
                y2.append(yy[i])
                data2.append(data[i])
        colors4 = [cmap(normalize(value4)) for value4 in data2]
        ax4.scatter(x2,y2,marker = '.', color=colors4, zorder=.25)
        
        ax5 = plt.axes([0.025, 0.625, x, y])
        ax5.axis('off')
        x2,y2,data2 = [],[],[]
        data = grp.variables['WNW'][:]
        for i in range(0,len(xx)):
            if xx[i] > lon1 and xx[i] < lon2 and yy[i] > lat1 and yy[i] < lat2:
                x2.append(xx[i])
                y2.append(yy[i])
                data2.append(data[i])
        colors5 = [cmap(normalize(value5)) for value5 in data2]
        ax5.scatter(x2,y2,marker = '.', color=colors5, zorder=.25)

        
        ax6 = plt.axes([-.015, 0.39, x, y])
        x2,y2,data2 = [],[],[]
        ax6.axis('off')
        data = grp.variables['W'][:]
        for i in range(0,len(xx)):
            if xx[i] > lon1 and xx[i] < lon2 and yy[i] > lat1 and yy[i] < lat2:
                x2.append(xx[i])
                y2.append(yy[i])
                data2.append(data[i])
        colors6 = [cmap(normalize(value6)) for value6 in data2]
        ax6.scatter(x2,y2,marker = '.', color=colors6, zorder=.25)

        ax7 = plt.axes([0.025, 0.155, x, y])
        x2,y2,data2 = [],[],[]
        ax7.axis('off')
        data = grp.variables['WSW'][:]
        for i in range(0,len(xx)):
            if xx[i] > lon1 and xx[i] < lon2 and yy[i] > lat1 and yy[i] < lat2:
                x2.append(xx[i])
                y2.append(yy[i])
                data2.append(data[i])
        colors7 = [cmap(normalize(value7)) for value7 in data2]
        ax7.scatter(x2,y2,marker = '.', color=colors7, zorder=.25)
        
        ax8 = plt.axes([0.165, -.08, x, y])
        x2,y2,data2 = [],[],[]
        ax8.axis('off')
        data = grp.variables['SW'][:]
        for i in range(0,len(xx)):
            if xx[i] > lon1 and xx[i] < lon2 and yy[i] > lat1 and yy[i] < lat2:
                x2.append(xx[i])
                y2.append(yy[i])
                data2.append(data[i])
        colors8 = [cmap(normalize(value8)) for value8 in data2]
        ax8.scatter(x2,y2,marker = '.', color=colors8, zorder=.25)
        
        ax9 = plt.axes([0.4, -.13, x, y])
        x2,y2,data2 = [],[],[]
        ax9.axis('off')
        data = grp.variables['S'][:]
        for i in range(0,len(xx)):
            if xx[i] > lon1 and xx[i] < lon2 and yy[i] > lat1 and yy[i] < lat2:
                x2.append(xx[i])
                y2.append(yy[i])
                data2.append(data[i])
        colors9 = [cmap(normalize(value9)) for value9 in data2]
        ax9.scatter(x2,y2,marker = '.', color=colors9, zorder=.25)
        
        ax10 = plt.axes([0.635, -.08, x, y])
        x2,y2,data2 = [],[],[]
        ax10.axis('off')
        data = grp.variables['SE'][:]
        for i in range(0,len(xx)):
            if xx[i] > lon1 and xx[i] < lon2 and yy[i] > lat1 and yy[i] < lat2:
                x2.append(xx[i])
                y2.append(yy[i])
                data2.append(data[i])
        colors10 = [cmap(normalize(value10)) for value10 in data2]
        ax10.scatter(x2,y2,marker = '.', color=colors10, zorder=.25)
        
        ax11 = plt.axes([0.775,0.155,x,y])
        x2,y2,data2 = [],[],[]
        ax11.axis('off')
        data = grp.variables['ESE'][:]
        for i in range(0,len(xx)):
            if xx[i] > lon1 and xx[i] < lon2 and yy[i] > lat1 and yy[i] < lat2:
                x2.append(xx[i])
                y2.append(yy[i])
                data2.append(data[i])
        colors11 = [cmap(normalize(value11)) for value11 in data2]
        ax11.scatter(x2,y2,marker = '.', color=colors11, zorder=.25)
        
        ax12 = plt.axes([0.815, 0.39, x, y])
        x2,y2,data2 = [],[],[]
        ax12.axis('off')
        data = grp.variables['E'][:]
        for i in range(0,len(xx)):
            if xx[i] > lon1 and xx[i] < lon2 and yy[i] > lat1 and yy[i] < lat2:
                x2.append(xx[i])
                y2.append(yy[i])
                data2.append(data[i])
        colors12= [cmap(normalize(value12)) for value12 in data2]
        ax12.scatter(x2,y2,marker = '.', color=colors12, zorder=.25)
        
        ax13 = plt.axes([0.775,0.625,x,y])
        x2,y2,data2 = [],[],[]
        ax13.axis('off')
        data = grp.variables['ENE'][:]
        for i in range(0,len(xx)):
            if xx[i] > lon1 and xx[i] < lon2 and yy[i] > lat1 and yy[i] < lat2:
                x2.append(xx[i])
                y2.append(yy[i])
                data2.append(data[i])
        colors13 = [cmap(normalize(value13)) for value13 in data2]
        ax13.scatter(x2,y2,marker = '.', color=colors13, zorder=.25)       
        
        return plt.show()
            
        
    def global_vid(global_path,netcdf_file,title,hours,levels,lon1,lon2,lat1,lat2):
        wl=[]
        xx = netcdf_file.variables['x'][:]
        yy = netcdf_file.variables['y'][:]
        gridvars = netcdf_file.variables      
        var_element = 'element'
        elems = gridvars[var_element][:,:]-1
        m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,urcrnrlon=lon2,resolution='h', epsg = 4269)
        for i in range(0,hours):
            i=i+1
            data1 = netcdf_file.variables['zeta'][i,:]
            file_number = '%02d'%i
            triang = tri.Triangulation(xx,yy, triangles=elems)
            m.arcgisimage(service='World_Street_Map', xpixels = 600, verbose= False)
            m.drawcoastlines(color='k')
            if data1.mask.any():
                point_mask_indices = np.where(data1.mask)
                tri_mask = np.any(np.in1d(elems, point_mask_indices).reshape(-1, 3), axis=1)
                triang.set_mask(tri_mask)
            plt.xlim([lon1, lon2])
            plt.ylim([lat1, lat2])    
            plt.tricontourf(triang, data1, levels=levels,alpha=0.9,vmin=-1.1, vmax=3, aspect='auto',cmap='jet')
            wl.append('WL{}.png'.format(file_number))
            plt.title(title + '\n')
            plt.savefig(os.path.join(global_path,'WL{}.png'.format(file_number)),dpi=300, bbox_inches = 'tight', pad_inches = 0.1)
            plt.close()
            os.chdir(global_path)
            images = []
        for ii in range(0,len(wl)):
            frames = Image.open(wl[ii])
            images.append(frames)
        images[0].save(title.split(' ')[0]+title.split(' ')[1]+'.gif',
           save_all=True,
           append_images=images[1:],
           delay=.1,
           duration=300,
           loop=0)
        for f in glob.glob(os.path.join(global_path,'WL*')):
            os.remove(f)
        return
        
        
        
        
        
        



        
        