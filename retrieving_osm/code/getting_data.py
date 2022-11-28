#########################################################
# import libraries

import os
from os.path import join
import osmnx
import pandas as pd

#########################################################
# paths

main_path = "G:/Blog_Projects/retrieving_osm/"
data_path = join(main_path, "data")
output_path = join(main_path, "output")

#########################################################
# set directory

os.chdir(main_path)

#########################################################
# set up parameters

# define geographical locations
cities = ["Berlin, Germany", "Hamburg, Germany"]

# define places
places = ["restaurant", "bar"]

# setting up folder structure
for p in places:
    isExist = os.path.exists(join(data_path, p))
    if not isExist:
        os.makedirs(join(data_path, p))

# set timestamp
settings = '[out:json][timeout:180][date:"{year}-12-31T00:00:00Z"]'

# define time strange
years = ["2020", "2021"]

# list to store the data
extracted_data = []

#########################################################
# data extraction process

# loop through years and get snapshot at the time
for place in places:
    for city in cities:
        for year in years:
            # define tag
            # Note: I defined amenities (like restaurants and bars) here. You can also
            # define other types (like leisure) depending on the OSM tag. You can find
            # out about different types by consulting Google.
            tag = {"amenity" : place}

            # set extraction year
            osmnx.settings.overpass_settings = settings.format(year = year)

            # extract data for tags and year
            tagged_data = osmnx.geometries_from_place(city, tags = tag)

            # add snapshot year
            tagged_data["snap_year"] = year

            # export data
            filename = str(place) + "_" + "extracted_data_" + str(year) + "_" + str(city) + ".csv"
            path = join(data_path, place)
            tagged_data.to_csv(join(path, filename))

            # append list to store data
            extracted_data.append(tagged_data)

            # print to see where the code is at
            print(f"Extraction of {year} and {city} for {tag} completed")
