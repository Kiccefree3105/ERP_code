from pyclmuapp import get_urban_params
urban = get_urban_params(urban_ds='/Users/user/Documents/GitHub/pyclmuapp/docs/notebooks/own/data/mksrf_urban_0.05x0.05_simyr2000.c170724.nc', # can be a xarray dataset or a path to a netcdf file
                 soil_ds='/Users/user/Documents/GitHub/pyclmuapp/docs/notebooks/own/data/mksrf_soitex.10level.c010119.nc', # can be a xarray dataset or a path to a netcdf file
                 lat = 53.417,
                 lon = -2.25,
                 outputname='surfdata_mcr.nc')