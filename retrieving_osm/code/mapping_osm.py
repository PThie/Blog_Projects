#########################################################
# import libraries

import os
import pandas as pd
from os.path import join
import geopandas as gpd
import geoplot as gplt
import matplotlib.pyplot as plt
import geoplot.crs as gcrs 

#########################################################
# paths

main_path = "G:/Blog_Projects/retrieving_osm/"
data_path = join(main_path, "data")
output_path = join(main_path, "output")

#########################################################
# set directory

os.chdir(main_path)

#########################################################
# prepare data

# global for GPS CRS
gps = 4326

# read Berlin borders
berlin_borders = gpd.read_file(
    join(
        data_path, "borders", "berlin_borders.shp"
    )
)

# transform to GPS
berlin_borders = berlin_borders.to_crs(gps)

# read Berlin restaurants
berlin_restaurants = pd.read_csv(
    join(data_path, "restaurant", "restaurant_extracted_data_2020_Berlin, Germany.csv"),
    index_col = None,
    header = 0,
    low_memory = False
)

# remove relations
berlin_restaurants = berlin_restaurants.loc[(berlin_restaurants["element_type"]) != "relation"]

# define as spatial data
berlin_restaurants["geometry"] = gpd.GeoSeries.from_wkt(berlin_restaurants["geometry"])
berlin_restaurants_spatial = gpd.GeoDataFrame(berlin_restaurants, geometry = "geometry", crs = "EPSG:4326")
berlin_restaurants_spatial = berlin_restaurants_spatial.to_crs(32632)

# replace ways (i.e. those that have the building as geo info) with centroid of building
berlin_restaurants_spatial.loc[(berlin_restaurants_spatial.element_type == "way"), "geometry"] = berlin_restaurants_spatial["geometry"].centroid

# set to GPS
berlin_restaurants_spatial = berlin_restaurants_spatial.to_crs(gps)

# plot and save
ax = gplt.pointplot(
    berlin_restaurants_spatial,
    color = "darkorange",
    linewidth = 0.1,
    figsize = (12, 10),
    projection = gcrs.WebMercator()
)
gplt.polyplot(berlin_borders, ax = ax)

plt.savefig(join(output_path, "map_berlin_restaurants.png"))