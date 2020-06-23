import matplotlib.pyplot as plt 
import cartopy 
import cartopy.crs as ccrs 
import env_methods as em 
import numpy as np 
import geopandas as gpd

def height_anomaly_plot(lat_start, lat_end, lon_start, lon_end,lat, lon, pres_levels, lev_x, data_package, title_str):
   
    lat1 = em.find_closest_val(lat_start, lat)
    lat2 = em.find_closest_val(lat_end, lat)
    lon1 = em.find_closest_val(lon_start, lon)
    lon2 = em.find_closest_val(lon_end, lon)

    lev_x = em.find_closest_val(lev_x, pres_levels)
    
    fig = plt.figure(figsize = (12,4))
    ax = plt.subplot(projection = ccrs.PlateCarree())

    ax.coastlines()

    ax.set_xticks(np.asarray(lon[::4]) - 180)
    ax.set_yticks(np.asarray(lat[::3]))
    ax.set_xlabel('lon')
    ax.set_ylabel('lat')
    mesh = plt.pcolormesh(lon[lon1:lon2], lat[lat1:lat2], data_package['hgt'][lev_x, lat1:lat2, lon1:lon2],
                    cmap = 'coolwarm', vmin = -1, vmax = 1)
    #plt.contour(lon[lon1:lon2], lat[lat1:lat2], data_package['hgt'][lev_x, lat1:lat2, lon1:lon2],
    #            cmap = 'coolwarm')
    
    cb = plt.colorbar(mesh)
    # ax.clabel(cont, inline=1, fontsize=5, colors = 'black')
    cb.set_label('stdev from mean')
    
    ax.set_title(title_str)
    
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    ax.add_feature(cartopy.feature.LAKES, alpha=0.5)
    ax.add_feature(cartopy.feature.RIVERS)
    
    return fig 
def average_plot(lat_start, lat_end, lon_start, lon_end, lat, lon, pres_levels, lev_x, data_package, title_str):
   
    lat1 = em.find_closest_val(lat_start, lat)
    lat2 = em.find_closest_val(lat_end, lat)
    lon1 = em.find_closest_val(lon_start, lon)
    lon2 = em.find_closest_val(lon_end, lon)

    lev_x = em.find_closest_val(lev_x, pres_levels)
    
    fig = plt.figure(figsize = (12,4))
    ax = plt.subplot(projection = ccrs.PlateCarree())

    ax.coastlines()

    ax.set_xticks(np.asarray(lon[::5]) - 180)
    ax.set_yticks(np.asarray(lat[::4]))
    ax.set_xlabel('lon')
    ax.set_ylabel('lat')
    mesh = plt.pcolormesh(lon[lon1:lon2], lat[lat1:lat2], data_package['hgt'][lev_x, lat1:lat2, lon1:lon2],
                    cmap = 'coolwarm')
    #plt.contour(lon[lon1:lon2], lat[lat1:lat2], data_package['hgt'][lev_x, lat1:lat2, lon1:lon2],
    #            cmap = 'coolwarm')
    
    cb = plt.colorbar(mesh)
    # ax.clabel(cont, inline=1, fontsize=5, colors = 'black')
    cb.set_label('GPH at ' + str(pres_levels[lev_x]) +'mb level [m]')
    quiv = plt.quiver(lon[lon1:lon2], lat[lat1:lat2], data_package['uwnd'][lev_x, lat1:lat2, lon1:lon2], 
                      data_package['vwnd'][lev_x, lat1:lat2, lon1:lon2])
    ax.quiverkey(quiv, X=0.3, Y=-0.1, U=10,
                 label='Quiver key, length = 10 m/s', labelpos='E')
    ax.set_title(title_str)

    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    ax.add_feature(cartopy.feature.LAKES, alpha=0.5)
    ax.add_feature(cartopy.feature.RIVERS)
    
    return fig

def sst_anomaly_plot(lat_start, lat_end, lon_start, lon_end, lat, lon, data_package, title_str, max_at_one):
   
    lat1 = em.find_closest_val(lat_start, lat)
    lat2 = em.find_closest_val(lat_end, lat)
    lon1 = em.find_closest_val(lon_start, lon)
    lon2 = em.find_closest_val(lon_end, lon)
    
    fig = plt.figure(figsize = (12,4))
    ax = plt.subplot(projection = ccrs.PlateCarree())

    ax.coastlines()

    ax.add_feature(cartopy.feature.RIVERS)
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')


    ax.set_xticks(np.asarray(lon[::5]) - 180)
    ax.set_yticks(np.asarray(lat[::4]))
    ax.set_xlabel('lon')
    ax.set_ylabel('lat')
    if max_at_one: 
        mesh = plt.pcolormesh(lon[lon1:lon2], lat[lat1:lat2], data_package['sst'][lat1:lat2, lon1:lon2],
                        cmap = 'coolwarm', vmin = -1, vmax = 1)
    else: 
        mesh = plt.pcolormesh(lon[lon1:lon2], lat[lat1:lat2], data_package['sst'][lat1:lat2, lon1:lon2],
                        cmap = 'coolwarm')  
    cb = plt.colorbar(mesh)
    # ax.clabel(cont, inline=1, fontsize=5, colors = 'black')
    cb.set_label('stdev from mean')
    
    ax.set_title(title_str)
    
    return fig 

def plot_poi():
    plt.figure()
    ax = plt.subplot(projection = ccrs.PlateCarree())
    ax.coastlines()
    path1 = r'D:\Shapefiles\msrivs\msrivs.shp'
    shp1 = gpd.read_file(path1)
    shp1.plot(ax=ax, edgecolor='cornflowerblue', linewidth = 2)
    plt.scatter(-91.438585, 38.708687, c = 'black')
    plt.scatter(-85.741164, 38.262327, c = 'black')
    plt.text(-94, 39.5, 'Hermann')
    plt.text(-87, 39, 'Louisville')
    gl = ax.gridlines(draw_labels = True)
    gl.xlabels_top = False
    gl.ylabels_right = False
    ax.add_feature(cartopy.feature.OCEAN)
    ax.add_feature(cartopy.feature.LAKES)
    ax.add_feature(cartopy.feature.BORDERS)
    plt.title('Locations of Flood Gauges')