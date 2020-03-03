# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 10:25:25 2020
Data from https://www.esrl.noaa.gov/psd/data/gridded/data.20thC_ReanV2c.pressure.html
@author: bydd1
"""
import os 
from netCDF4 import Dataset
import cartopy 
import cartopy.crs as ccrs 
import datetime as dt 
import numpy as np 

#find the closest value to some specified value in an array 
def find_closest_val(val, arr):
    if isinstance(val, dt.datetime):
        diff = [(abs(x - val)).total_seconds() for x in arr]
    else: 
        diff = [abs(x - val) for x in arr]
    index = diff.index(min(diff))
    return index    
    
#convert from "hours since 1800-1-1" to a datetime object 
def convert_datetime(val):
    origin = dt.datetime(1800, 1, 1, 0, 0, 0)
    new = origin + dt.timedelta(hours = val)
    return new 

#acquire data between start and end data, return as dict 
def get_data(directory, all_data, time_b):
  
    files = os.listdir(directory)
    
    c_var_names = ['level', 'lat', 'lon', 'time', 'time_bnds']
    
    nc_vars = dict()
    
    x = Dataset(os.path.join(directory, files[0]), 'r', format = 'NETCDF4')
    
    lev = list(x['level'][:].data)
    lat = x['lat'][:].data
    lon = x['lon'][:].data
    time = x['time'][:].data
    pres_levels = [1000, 850, 500]
    pres_levels_i = [lev.index(i) for i in pres_levels]
    
    #sort out the time situation 
    origin = dt.datetime(1800, 1, 1, 0, 0, 0)
    
    if not all_data: 
        month_start = time_b[0]
        year_start = time_b[1]
        month_end = time_b[2]
        year_end = time_b[3]
        
        time_start = (dt.datetime(year = year_start, month = month_start, day = 1) - origin).total_seconds() / 3600

        time_end = (dt.datetime(year = year_end, month = month_end, day = 1) - origin).total_seconds() / 3600
        time_start_i = find_closest_val(time_start, time)
        time_end_i = find_closest_val(time_end, time)
        
    else:
        time_start_i = 0 
        time_end_i = len(time)
        
    time = time[time_start_i:time_end_i]
    time = [convert_datetime(i) for i in time]

    for i in files[:]:
        path = os.path.join(directory, i)
        x = Dataset(path, 'r', format = 'NETCDF4')
        var_name = [i for i in list(x.variables.keys()) if i not in c_var_names][0]
        var = x[var_name][time_start_i:time_end_i, pres_levels_i, :, :].data
        nc_vars[var_name] = var
    
    data_package = {'pres_levels':pres_levels,
                    'time':time,
                    'lat':lat,
                    'lon':lon,
                    'nc_vars': nc_vars}
    return data_package

def normalize_data(var, time):

    mean_monthly = np.empty((12, var.shape[1], var.shape[2]))
    stdev_monthly = np.empty((12, var.shape[1], var.shape[2]))
    
    for i in np.arange(1,13): #iterate through months
        monthly_subset = []
        monthly_indices = []
        for t in time:
            if t.month == i: 
                monthly_indices.append(time.index(t))
        monthly_subset = var[monthly_indices, :, :]
            
        mean_monthly[i - 1, :, :] = np.mean(monthly_subset, axis = 0)
        stdev_monthly[i - 1, :, :] = np.std(monthly_subset, axis = 0)
        
    for date in time: #for every time value, normalize
        month = date.month
    
        frame = var[time.index(date), :, :]
        
        #normalization formula = (x - mean) / stdev
        normalized_frame = np.divide(np.subtract(frame, mean_monthly[month - 1]), 
                                     stdev_monthly[month - 1])
        var[time.index(date), :, :] = normalized_frame
    
    return var
