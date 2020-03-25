
# miss-atmo
Atmospheric trends related to heavy flooding events in the Mississippi Basin (same purpose as miss-climate, I was just too nauseated at the prospect of sifting through that mess and decided to start from scratch)

## Data Dependencies
- NOAA-CIRES 20th Century Reanalysis V2c (https://www.esrl.noaa.gov/psd/data/gridded/data.20thC_ReanV2c.html)
	- uwnd
	- vwnd
	- gph 
- NOAA ERSST (https://www.esrl.noaa.gov/psd/data/gridded/data.noaa.ersst.v5.html)
    - sst 
- USGS Gage Data for Hermann, Louisville, and Vicksburg 
	- top ten dates at each location 

## Packages
- env_methods: package with methods for handling data 
- vis_methods: package with methods for visualizing data 

## Scripts

## Notebooks
- gph_wind_anomaly.ipynb: Jupyter Notebook that generates anomaly and mean maps for GPH and wind vectors 
- sst_anomaly.ipynb: Jupyter Notebook that generates anomaly maps for SST around heavy flooding events 
- ind_event.ipynb: Jupyter Notebook that generates anomaly and composite maps for single flood events 

## Python Dependencies
- matplotlib 
- netCDF4
- cartopy 
- datetime 
- numpy 
- pandas 
- copy