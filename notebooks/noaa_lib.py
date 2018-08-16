import pandas as pd
import numpy as np
import netCDF4 as nc4
from datetime import datetime
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import random





def tide_data(begin_d, end_d, station):
    website = r'https://tidesandcurrents.noaa.gov/api/'
    datum = 'datum=MSL'
    units = 'units=metric'
    timez = 'time_zone=GMT'
    form = 'format=csv'
    app = 'datagetter?product=water_level&application=NOS.COOPS.TAC.WL'
    domain = website + app + '&' + station + '&' + begin_d + '&' + end_d + '&' + datum + '&' + units + '&' + timez + '&' + form
    return domain

def tide_gauges():
    Hatteras = {'Hatteras':'station=8654467'}
    Beaufort = {'Beaufort':'station=8656483'}
    Wrightsville = {'Wrightsville':'station=8658163'}
    Duck = {'Duck': 'station=8651370'}
    Wilmington = {'Wilmington':'station=8658120'}
    Oregon = {'Oregon':'station=8652587'}
    stations = [Hatteras, Beaufort, Wrightsville, Duck, Wilmington, Oregon]
    return stations

def noaa_map(ax,lat1,lat2,lon1,lon2):
    x = [-75.704178,-76.670471,-77.786322]
    y = [35.20885,34.719802,34.213210]
    m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,urcrnrlon=lon2,resolution='h', epsg = 4269)
    m.drawcoastlines(color='k')
    m.arcgisimage(service='World_Street_Map', xpixels=int(500), verbose= False)
    ax.scatter(x,y,marker = '.', color='fuchsia',s=750, zorder=5)

    return plt.show()

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
                color = c_list[y]
        trace = go.Scatter(
                x = date,
                y = water_level,
                name = dataset.name,
                        line = dict(
                        color = color))
        data.append(trace)
    layout = go.Layout(dict(title = title),
                  xaxis = dict(title = 'Time'),
                  yaxis = dict(title = 'Water level (m) above NavD88'),                     
                  legend= dict(orientation = "h"),
                  font = dict(color = 'rgb(255,255,255)'),
                  paper_bgcolor = 'rgb(0,0,0)',
                  plot_bgcolor = 'rgb(0,0,0)')
    return data, layout





