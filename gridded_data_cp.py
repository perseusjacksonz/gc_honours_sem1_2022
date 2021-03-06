import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from scipy import spatial
#%matplotlib inline
import sys


def find_index(pointlat,pointlon):
    xi=np.searchsorted(lat,pointlat)
    yi=np.searchsorted(lon,pointlon)
    return xi,yi

#read in the barra precip
precip,lat,lon=read_barra_data()
print(np.shape(precip))

#lon_grid, lat_grid = np.meshgrid(lon,lat)

#print('lon_grid',np.shape(lon_grid))
#data = (np.linspace(30, 0, num_sl*num_gp).reshape(num_sl, num_gp) + 
#        6*np.random.rand(num_sl, num_gp))

#precip = xr.DataArray(variable, dims=['lat', 'lon'])

print('test1',np.shape(lat))
print('test2',np.shape(lon))
print('test3',np.shape(precip))


#find closest point to whatever you inout in a regualr lat lon array.

#read in the ignition data set


#loop over ignition data



pointlon= 135
pointlat= -30


#find the closest index in the precip array
thisLat, thisLong = find_index(pointlat,pointlon)

closest_point_in_array=precip[thisLat,thisLong]
print('rainfall',closest_point_in_array)

lightning_dtf_match['collocated_lat'],lightning_dtf_match['collocated_lon']=find_index(lightning_dtf_match['Lat_IG'],lightning_dtf_match['Lon_IG'])
lightning_dtf_match['precip']=precip[lightning_dtf_match['collocated_lat'],lightning_dtf_match['collocated_lon']]

#add the matched point to your data frame

sys.exit()


#use this when you have an irregular array

class KDTreeIndex():
    
    """ A KD-tree implementation for fast point lookup on a 2D grid
    
    Keyword arguments: 
    dataset -- a xarray DataArray containing lat/lon coordinates
               (named 'lat' and 'lon' respectively)
               
    """
    
    def transform_coordinates(self, coords):
        """ Transform coordinates from geodetic to cartesian
        
        Keyword arguments:
        coords - a set of lan/lon coordinates (e.g. a tuple or 
                 an array of tuples)
        """
        # WGS 84 reference coordinate system parameters
        A = 6378.137 # major axis [km]   
        E2 = 6.69437999014e-3 # eccentricity squared    
        
        coords = np.asarray(coords).astype(np.float64)
        
        # is coords a tuple? Convert it to an one-element array of tuples
        if coords.ndim == 1:
            coords = np.array([coords])
        
        # convert to radiants
        lat_rad = np.radians(coords[:,0])
        lon_rad = np.radians(coords[:,1]) 
        
        # convert to cartesian coordinates
        r_n = A / (np.sqrt(1 - E2 * (np.sin(lat_rad) ** 2)))
        x = r_n * np.cos(lat_rad) * np.cos(lon_rad)
        y = r_n * np.cos(lat_rad) * np.sin(lon_rad)
        z = r_n * (1 - E2) * np.sin(lat_rad)
        
        return np.column_stack((x, y, z))
    
    def __init__(self, dataset):
        # store original dataset shape
        self.shape = dataset.shape
        
        # reshape and stack coordinates
        coords = np.column_stack((dataset.lat.values.ravel(),
                                  dataset.lon.values.ravel()))
        
        # construct KD-tree
        self.tree = spatial.cKDTree(self.transform_coordinates(coords))
        
    def query(self, point):
        """ Query the kd-tree for nearest neighbour.

        Keyword arguments:
        point -- a (lat, lon) tuple or array of tuples
        """
        _, index = self.tree.query(self.transform_coordinates(point))
        
        # regrid to 2D grid
        index = np.unravel_index(index, self.shape)
        
        # return DataArray indexers
        return xr.DataArray(index[0], dims='pixel'), \
               xr.DataArray(index[1], dims='pixel')
    
    def query_ball_point(self, point, radius):
        """ Query the kd-tree for all point within distance 
        radius of point(s) x
        
        Keyword arguments:
        point -- a (lat, lon) tuple or array of tuples
        radius -- the search radius (km)
        """
        
        index = self.tree.query_ball_point(self.transform_coordinates(point),
                                           radius)

        # regrid to 2D grid 
        index = np.unravel_index(index[0], self.shape)
        
        # return DataArray indexers
        return xr.DataArray(index[0], dims='pixel'), \
               xr.DataArray(index[1], dims='pixel')

ground_pixel_tree = KDTreeIndex(precip)

melbourne = (-37.8136, 144.9631)
melbourne_index = ground_pixel_tree.query(melbourne)
print(variable[melbourne_index])

coords = np.column_stack((da.lat.values.ravel(),
                          da.lon.values.ravel()))
