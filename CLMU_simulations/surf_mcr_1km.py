import json
import xarray as xr
import numpy as np

varlist = [
    'ALB_ROOF',
    'EM_ROOF',
    'ALB_IMPROAD',
    'EM_IMPROAD',
    'ALB_PERROAD',
    'EM_PERROAD',
    'ALB_WALL',
    'EM_WALL',
    'HT_ROOF',
    'CANYON_HWR',
    'WTLUNIT_ROOF',
    'WTROAD_PERV',
    'PCT_URBAN',
    'WIND_HGT_CANYON']

var_dict = {}



def get_urban_dist(fp, var, lat, lon):
    
    urban = xr.open_dataset(fp.format(var=var))
    
    urban = urban.sel(lat=slice(lat-0.25, lat+0.25), lon=slice(lon-0.25, lon+0.25))
    
    valid_values = urban[var].values[~np.isnan(urban[var].values)]
    var_dict[var] = [valid_values.min(), valid_values.max()]

filepath = '/mnt/iusers01/fatpou01/sees01/z47137jy/scratch/urbrwt/surf/USurf_1km_netcdf/global_{var}_1km_masked_gapfilled_QC.nc'

for var in varlist:
    file = filepath.format(var=var)
    get_urban_dist(file, var, 53.417, -2.25)
    
with open('mcr_up_dist.json', 'w') as f:
    json.dump(var_dict, f)