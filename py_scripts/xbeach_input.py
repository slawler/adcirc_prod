import math
import pandas as pd
import numpy as np
import os
import datetime as dt
from oceanwaves import OceanWaves
from scipy.interpolate import interp1d
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from wave_utils import waves
root = r'D:\FHRL_work\Projects\Brazil\xbeach\raw_data'
cross= 'cross_v1.csv'

grid = pd.read_csv(os.path.join(root,cross))

x = grid['X'][:]
z = grid['Graphic Profile 1'][:]

#%%
#class xbeach:
#    def __init__(self):
#        
#
#def generate_xgrid(xin,zin,var):
xin = x
zin = z
xgrid   = {'xgrid':[]}
Tm      = {'Tm':5.0}
dxmin   = {'dxmin':2.0}
dxmax   = {'dxmax':'Inf'}
vardx   = {'vardx':1.0}
g       = {'g':9.81}
CFL     = {'CFL':0.9}
dtref   = {'dtref':4.0}
maxfac  = {'maxfac':1.15}
wl      = {'wl':0}
depthfac= {'depthfac':2}
ppwl    = {'ppwl':12}
OPT = [xgrid,Tm,dxmin,dxmax,vardx,g,CFL,dtref,maxfac,wl,depthfac,ppwl]
dx = []
depthfac= 2
ppwel   = 12

  # make grid
xend    = xin.iloc[-1]
xstart  = xin.iloc[0]
xlast   = xstart
  
if vardx == 0:
  xgr = np.linspace(xin.iloc[0],xin.iloc[-1],int(len(xin))/OPT[2]['dxmin'])
  zgr = np.interp(xgr,xin,zin)
      #    xb_verbose(1,'Create equidistant cross-shore grid');

elif vardx == 1 and not xgrid:
  xgr = OPT[0]['xgrid']
  zgr = np.interp(xgr,xin,zin)

elif vardx == 1:
  hin = max(OPT[9]['wl']-zin)
  k = waves.dispersion(2*math.pi/OPT[1]['Tm'],hin,OPT[5]['g'])
  Llong = 4*2*math.pi/k
  x = xin
  
  xgr, zgr,hgr = [],[],[]
  ii = 0;
  xgr.append(xstart)
  zgr.append(zin(0))
  hgr.append(hin(0)) 

  while xlast < xend:
    dxmax = Llong/OPT[11]['ppwl']
    dxmax = min(dxmax,float(OPT[3]['dxmax']))
    dx = math.sqrt(OPT[5]['g']*hgr)
    dx = min(xgr[ii],xend)
    dx = max(dx[ii],OPT[2]['dxmin'])
#%%      
trace = go.Scatter(
    x = xgr,
    y = zgr)
data = [trace]

plot(data, 'cross.html')
      
      
#    xb_verbose(2,'Grid size',dxmin);
    


      
#%%










