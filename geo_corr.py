#!/usr/bin/env python
# coding: utf-8

# # Geographic Correlation to POI: air temperature (reanalysis) and precipitation (GPCC)

# Calculate correlation between geographic points surrounding St. Louis, MO for chosen environmental variables. 

# #### import packages

# In[1]:


import env_methods as em 
import vis_methods as vm 
import time 
import numpy as np
import copy
import matplotlib.pyplot as plt 
import cartopy 
import cartopy.crs as ccrs
import os
import geopandas

# #### initial parameters 

# In[2]:


st_lou = [38.611389, -90.203154] #lat/lon coords of a taco joint in st. lou
#standard longitude system = -degrees east of prime meridian, +degrees west of prime meridian (GPCC stores data this way 

#bounding box - North America
lat_start = 60
lat_end = 0
lon_start = -180
lon_end =  -20

#whold world bouding box 
#lat_start = 90
#lat_end = -90
#lon_start = -180
#lon_end =  180

#files containing data 
gpcc_dir = r'D:\GPCC'
air_dir = r'D:\NOAA - just air'
mois_dir = r'D:\NOAA Reanalysis Data\Soil'


# #### import data
start_time = time.time()
pre_dic = em.get_data_gpcc(gpcc_dir, 1) #1 degree resolution, can't handle 0.25 deg res 
print("--- %s seconds for GPCC ---" % (time.time() - start_time))


# __NOTE__: All NCEP reanalysis datasets are stored in 0 to 360 deg longitude sets, representing degrees west of the dateline
start_time = time.time()
air_dic = em.get_data(air_dir, True, [0]) #1 degree resolution, can't handle 0.25 deg res 
air = air_dic['nc_vars']['air']
air_dic['air'] = air_dic.pop('nc_vars') #get rid of stacked structure 
air_dic['air'] = air
print("--- %s seconds for air temp ---" % (time.time() - start_time))


start_time = time.time()
mois_dic = em.get_data(mois_dir, True, [0])
soilm = mois_dic['nc_vars']['soilm']
mois_dic['soilm'] = mois_dic.pop('nc_vars')
soilm[soilm == 9.96921E36] = np.nan
soilm[soilm == -9.96921E36] = np.nan
mois_dic['soilm'] = soilm
print("--- %s seconds for soil moisture ---" % (time.time() - start_time))

def compress2annual(dp, var):
    num_years = dp['time'][-1].year - dp['time'][0].year + 1 
    new_data = np.empty((num_years, dp[var].shape[1], dp[var].shape[2]))
    time_new = np.arange(dp['time'][0].year, dp['time'][-1].year + 1).tolist()

    for y in time_new: 
        inds = em.get_year_indices(dp['time'], y)
        arr = np.mean(dp[var][inds, :, : ], axis = 0)
        
        new_data[time_new.index(y), :, :] = arr
    
    dp['time'] = time_new
    print('---time bnds---')
    print([time_new[0], time_new[-1]])
    dp[var] = new_data
    
    return dp 

air_dic = compress2annual(copy.deepcopy(air_dic), 'air')
pre_dic = compress2annual(copy.deepcopy(pre_dic), 'precip')
mois_dic = compress2annual(copy.deepcopy(mois_dic), 'soilm')


# #### geospatial correlation method
#method to generate a correlation grid 
#assume grid = time x lat x lon 
def corr_grid(array, poi): #poi refers to indices 
    corr = np.empty([array.shape[1], array.shape[2]])
    comp = array[:, poi[0], poi[1]] #time series at poi 
    for i in range(array.shape[1]):
        for j in range(array.shape[2]):
            comp0 = array[:, i, j]
            corr[i, j] = np.corrcoef(comp, comp0)[0,1]
    return corr


# #### run correlation on each dictionary 

start_time = time.time()
dics = [pre_dic, air_dic, mois_dic]
name = ['precip', 'air', 'soilm']
c = []

for i in range(len(dics)):
    d = dics[i]

    poi = [em.find_closest_val(st_lou[0], d['lat']), em.find_closest_val(st_lou[1], d['lon'])]
    
    #conversion
    if i > 0: 
        if st_lou[1] < 0: 
            poi = [em.find_closest_val(st_lou[0], d['lat']), em.find_closest_val(360 + st_lou[1], d['lon'])] 
        if st_lou[1] > 0:
            poi = [em.find_closest_val(st_lou[0], d['lat']), em.find_closest_val(st_lou[1], d['lon'])] 
    print(poi)
    c.append(corr_grid(d[name[i]], poi))
    

print("--- %s seconds for correlation  ---" % (time.time() - start_time))


def plot_corr(dic, array, title, lat_start, lat_end, lon_start, lon_end, poi, flipped_axis):
    lat = dic['lat']
    lon = dic['lon']
    
    old_lon = lon 
    if flipped_axis:
        lon = [180 - x for x in lon]
        temp = lon_start
        lon_start = lon_end
        lon_end = temp
        
        #print(lon)
        print([lon_start, lon_end])
        
    fig = plt.figure(figsize = (12, 5))
    fig.patch.set_facecolor('white')

    ax = plt.subplot(projection = ccrs.PlateCarree(central_longitude = 0))
    lat1 = em.find_closest_val(lat_start, lat)
    lat2 = em.find_closest_val(lat_end, lat)
    lon1 = em.find_closest_val(lon_start, lon)
    lon2 = em.find_closest_val(lon_end, lon)
    
    print([lon1, lon2])
    ax.coastlines()
    plt.title(title)
    plt.xlabel('lon')
    plt.ylabel('lat')

    int_lon = int(len(old_lon[lon1:lon2])/10)
    int_lat = int(len(lat[lat1:lat2])/10)

    ax.set_xticks(np.round(np.asarray(old_lon[lon1:lon2][::int_lon])), crs = ccrs.PlateCarree())
    ax.set_yticks(np.round(np.asarray(lat[lat1:lat2][::int_lat])), crs = ccrs.PlateCarree())
        
    mesh = plt.pcolormesh(old_lon[lon1:lon2], lat[lat1:lat2], array[lat1:lat2,lon1:lon2], cmap = 'coolwarm', vmax = 1, vmin = -1)
    cbar = plt.colorbar(mesh)

    path1 = r'D:\Shapefiles\msrivs\msrivs.shp'
    shp1 = geopandas.read_file(path1)
    shp1.plot(ax=ax, edgecolor='gray', linewidth = 1.3)

    path2 = r'D:\Shapefiles\Miss_RiverBasin\Miss_RiverBasin.shp'
    shp2 = geopandas.read_file(path2)
    shp2 = shp2.to_crs("EPSG:4326")
    shp2.plot(ax = ax, edgecolor = 'black', linewidth = 1.3, facecolor = 'none')


    ax.scatter(poi[1], poi[0], color = 'yellow', s = 30, transform=ccrs.PlateCarree())
    cbar.set_label('correlation coefficient to St. Louis')
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')

    savepath = os.path.join(r'C:\Users\bydd1\OneDrive\Documents\Research\miss-atmo correlation images', title + '.png')
    plt.savefig(savepath)


plot_corr(pre_dic, c[0], 'Precipitation Annual Average Correlation (GPCC)', lat_start, lat_end, lon_start, lon_end, copy.copy(st_lou), False)
plot_corr(air_dic, c[1], 'Air Temperature Annual Average Correlation', lat_start, lat_end,lon_start, lon_end, copy.copy(st_lou), True)
plot_corr(mois_dic, c[2], 'Soil Moisture Annual Average Correlation', lat_start, lat_end, lon_start, lon_end, copy.copy(st_lou), True)

