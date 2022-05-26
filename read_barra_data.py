#
#
#read in the barray data and sum over the different forecast perions
#
#

from netCDF4 import Dataset as NetCDFFile
import numpy as np

def read_barra_data():
    
    nc = NetCDFFile('/g/data/cj37/BARRA/BARRA_R/v1/forecast/spec/accum_prcp/2008/01/accum_prcp-fc-spec-PT1H-BARRA_R-v1-20080101T0000Z.sub.nc')
    var=nc.variables['accum_prcp']
    lon=nc.variables['longitude']
    lat=nc.variables['latitude']

    print('shape lat',np.shape(lat))
    print('shape lon',np.shape(lon))
    print('xx',np.shape(var))
    #variable[4]
    variable=np.sum(var,axis=0)
    print('yy',np.shape(variable))
    return variable, lat,lon


#read_barra_data()
