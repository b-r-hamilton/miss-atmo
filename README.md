
# miss-atmo
Atmospheric trends related to heavy flooding events in the Mississippi

## Data Dependencies
- NOAA-CIRES 20th Century Reanalysis V2c and V3 (https://www.esrl.noaa.gov/psd/data/gridded/data.20thC_ReanV2c.html)
    - air 
    - hgt
    - prate
    - pres
    - runoff 
    - snod
    - soilw 
    - uwnd 
    - vwnd 
- NOAA ERSST (https://www.esrl.noaa.gov/psd/data/gridded/data.noaa.ersst.v5.html)
    - sst 
- USGS Gage Data for Hermann, Louisville, and Vicksburg 
	- top ten dates at each location 

## Packages
- env_methods: package with methods for handling data 
- vis_methods: package with methods for visualizing data 

## Scripts

## Notebooks
- allvariable_analysis.ipynb: pulls reanalysis data prior to each flood for all variables, plots anomaly composites and exports to csv 
- bootstrap.ipynb: completes a bootstrap analysis for significance of atmospheric patterns 
- geo_corr.ipynb: computes Pearson correlation in env. variables to single specified point 
- gph_wind_anomaly.ipynb: generates anomaly and mean maps for GPH and wind vectors 
- ind_event.ipynb: Jupyter Notebook that generates anomaly and composite maps for single flood events 
- sst_anomaly.ipynb: generates anomaly maps for SST around heavy flooding events 

## Python Dependencies
- matplotlib 
- netCDF4
- cartopy 
- datetime 
- numpy 
- pandas 
- copy