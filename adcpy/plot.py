
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import netCDF4 as nc4
import matplotlib as mpl
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import FancyArrowPatch
from PIL import *




def attr_plot(grp,title,ax,lat1,lat2,lon1,lon2,data='data',pixels='600'):
    x = grp.variables['Longitude'][:]
    y = grp.variables['Latitude'][:]
    #z = grp.variables['Elevation'][:]
    data = grp.variables[data][:]
    m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,urcrnrlon=lon2,resolution='h', epsg = 4269)
    m.drawcoastlines(color='k')
    m.arcgisimage(service='World_Street_Map', xpixels=int(pixels), verbose= False)
    plt.title(title+'\n')
    cmap = mpl.cm.get_cmap('viridis')  
    normalize = mpl.colors.Normalize(vmin=min(data), vmax=max(data))
    colors = [cmap(normalize(value)) for value in data]
    ax.scatter(x,y,marker = '.', color=colors, zorder=.25)
    cax, _ = mpl.colorbar.make_axes(ax)
    cbar = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=normalize)
    
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

def global_water(global_path,netcdf_file,title,hours,levels,lon1,lon2,lat1,lat2):
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
        m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 900, verbose= False)
        m.drawcoastlines(color='k')
        if data1.mask.any():
            point_mask_indices = np.where(data1.mask)
            tri_mask = np.any(np.in1d(elems, point_mask_indices).reshape(-1, 3), axis=1)
            triang.set_mask(tri_mask)
        plt.xlim([lon1, lon2])
        plt.ylim([lat1, lat2])    
        plt.tricontourf(triang, data1, levels=levels,alpha=0.75,vmin=-1.1, vmax=6, aspect='auto',cmap='jet')
        wl.append('WL{}.png'.format(file_number))
        plt.colorbar(cmap='jet',format = "%.1f") 
        plt.title(title + '\n')
        plt.savefig('WL{}.png'.format(file_number),dpi=300, bbox_inches = 'tight', pad_inches = 0.1)
        plt.close()
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
    for f in glob.glob('WL*'):
        os.remove(f)    
    return

def global_velocity(global_path,netcdf_file,title,hours,levels,lon1,lon2,lat1,lat2):
    wl=[]
    xx = netcdf_file.variables['x'][:]
    yy = netcdf_file.variables['y'][:]
    gridvars = netcdf_file.variables      
    var_element = 'element'
    elems = gridvars[var_element][:,:]-1
    m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,urcrnrlon=lon2,resolution='h', epsg = 4269)
    for i in range(0,hours):
        i=i+1
        u = netcdf_file.variables['u-vel'][i,:]
        v = netcdf_file.variables['v-vel'][i,:]
        file_number = '%02d'%i
        m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 900, verbose= False)
        m.drawcoastlines(color='k')
        plt.quiver(xx,yy,u,v)
        plt.xlim([lon1, lon2])
        plt.ylim([lat1, lat2])    
        wl.append('WL{}.png'.format(file_number))
        plt.title(title + '\n')
        plt.savefig('WL{}.png'.format(file_number),dpi=300, bbox_inches = 'tight', pad_inches = 0.1)
        plt.close()
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
    for f in glob.glob('WL*'):
        os.remove(f)
    return

def global_pressure(global_path,netcdf_file,title,hours,levels,lon1,lon2,lat1,lat2):
    wl=[]
    xx = netcdf_file.variables['x'][:]
    yy = netcdf_file.variables['y'][:]
    gridvars = netcdf_file.variables      
    var_element = 'element'
    elems = gridvars[var_element][:,:]-1
    m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,urcrnrlon=lon2,resolution='h', epsg = 4269)
    for i in range(0,hours):
        i=i+1
        data1 = netcdf_file.variables['pressure'][i,:]
        file_number = '%02d'%i
        triang = tri.Triangulation(xx,yy, triangles=elems)
        m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 900, verbose= False)
        m.drawcoastlines(color='k')
        if data1.mask.any():
            point_mask_indices = np.where(data1.mask)
            tri_mask = np.any(np.in1d(elems, point_mask_indices).reshape(-1, 3), axis=1)
            triang.set_mask(tri_mask)
        plt.xlim([lon1, lon2])
        plt.ylim([lat1, lat2])    
        plt.tricontourf(triang, data1, levels=levels,alpha=0.9,vmin=-1.1, vmax=3, aspect='auto',cmap='jet')
        wl.append('WL{}.png'.format(file_number))
        plt.colorbar(cmap='jet',format = "%.1f") 
        plt.title(title + '\n')
        plt.savefig('WL{}.png'.format(file_number),dpi=300, bbox_inches = 'tight', pad_inches = 0.1)
        plt.close()
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
    for f in glob.glob('WL*'):
        os.remove(f)    
    return

def global_wind(global_path,netcdf_file,title,hours,levels,lon1,lon2,lat1,lat2):
    wl=[]
    xx = netcdf_file.variables['x'][:]
    yy = netcdf_file.variables['y'][:]
    gridvars = netcdf_file.variables      
    var_element = 'element'
    elems = gridvars[var_element][:,:]-1
    m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,urcrnrlon=lon2,resolution='h', epsg = 4269)
    for i in range(0,hours):
        i=i+1
        u = netcdf_file.variables['windx'][i,:]
        v = netcdf_file.variables['windy'][i,:]
        file_number = '%02d'%i
        m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 900, verbose= False)
        m.drawcoastlines(color='k')
        plt.quiver(xx,yy,u,v)
        plt.xlim([lon1, lon2])
        plt.ylim([lat1, lat2])    
        wl.append('WL{}.png'.format(file_number))
        plt.title(title + '\n')
        plt.savefig('WL{}.png'.format(file_number),dpi=300, bbox_inches = 'tight', pad_inches = 0.1)
        plt.close()
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
    for f in glob.glob('WL*'):
        os.remove(f)
    return

def water_velocity(global_path,nc4_f1,nc4_f2,title,hours,levels,lon1,lon2,lat1,lat2):
    wl=[]
    xx = nc4_f1.variables['x'][:]
    yy = nc4_f1.variables['y'][:]
    gridvars = nc4_f1.variables      
    var_element = 'element'
    elems = gridvars[var_element][:,:]-1
    m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,urcrnrlon=lon2,resolution='h', epsg = 4269)
    for i in range(0,hours):
        i=i+1
        data1 = nc4_f1.variables['zeta'][i,:]
        u = nc4_f2.variables['u-vel'][i,:]
        v = nc4_f2.variables['v-vel'][i,:]
        file_number = '%02d'%i
        triang = tri.Triangulation(xx,yy, triangles=elems)
        m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 900, verbose= False)
        m.drawcoastlines(color='k')
        if data1.mask.any():
            point_mask_indices = np.where(data1.mask)
            tri_mask = np.any(np.in1d(elems, point_mask_indices).reshape(-1, 3), axis=1)
            triang.set_mask(tri_mask)
        plt.xlim([lon1, lon2])
        plt.ylim([lat1, lat2])    
        plt.tricontourf(triang, data1, levels=levels,alpha=0.9,vmin=-1.1, vmax=6, aspect='auto',cmap='jet')
        plt.quiver(xx,yy,u,v)
        wl.append('WL{}.png'.format(file_number))
        #plt.colorbar(cmap='jet',format = "%.1f") 
        plt.title(title + '\n')
        plt.savefig('WL{}.png'.format(file_number),dpi=300, bbox_inches = 'tight', pad_inches = 0.1)
        plt.close()
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
    for f in glob.glob('WL*'):
        os.remove(f)    
    return  