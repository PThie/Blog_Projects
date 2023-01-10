#--------------------------------------------------
# import libraries

import pandas as pd
import os
from os.path import join
from geopy.geocoders import Nominatim
import numpy as np

#--------------------------------------------------
# paths

main_path = r"G:\Blog_Projects\nfl_travels"
data_path = main_path + r"\data"

# set directory
os.chdir(main_path)

#--------------------------------------------------
# read data
schedule = pd.read_csv(
    filepath_or_buffer = join(data_path, "game_schedule.csv"),
    sep = ";"
)

locations = pd.read_csv(
    filepath_or_buffer = join(data_path, "team_locations.csv"),
    sep = ";"
)

#--------------------------------------------------
# adjust name of the Commanders which changed their team name

locations["team_name"] = locations["team_name"].replace(
    "Washington Redskins", "Washington Commanders"
)

#--------------------------------------------------
# add short name of teams to location data
# split long name into parts and keep the last element

locations["team_name_short"] = locations["team_name"].str.split(" ").str[-1]

# remove white spaces
schedule["away_team"] = schedule["away_team"].str.strip()
schedule["home_team"] = schedule["home_team"].str.strip()

# check if all names match between both data sets
unique_loc_names = sorted(locations["team_name_short"].unique())
unique_sched_names = sorted(schedule["away_team"].unique())

if unique_loc_names == unique_sched_names:
    pass
else:
    print("Team names differ")
    
#--------------------------------------------------
# do some cleaning by deleting unneeded columns

locations.drop(
    columns = ["team_name", "arena_name", "seat_cap", "opening"],
    inplace = True
)

#--------------------------------------------------
# find coordinates for each location

# calling Nominatim tool
loct = Nominatim(user_agent = "GetLoc")

# get each location as value
arena_locs = locations["arena_location"].values

# list for storage
coords = []

# loop through all locations
for arena_loc in arena_locs:
    # complete location name
    loc_name = loct.geocode(arena_loc)
    # get longitude and latitude
    lon = loc_name.longitude
    lat = loc_name.latitude
    coord = [lat, lon]
    # store coords
    coords.append(coord)
    
# assing to location data
locations["coords"] = coords

#--------------------------------------------------
# merge location data to schedule based on away team

away_location = pd.merge(
    schedule,
    locations,
    left_on = "away_team",
    right_on = "team_name_short"
)

# rename columns
away_location.rename(
    columns = {
        "arena_location" : "loc_away_team",
        "coords" : "coords_away_team"
    },
    inplace = True
)

# drop columns
away_location.drop(
    columns = "team_name_short",
    inplace = True
)

#--------------------------------------------------
# merge location data based on home team

schedule_locations = pd.merge(
    away_location,
    locations,
    left_on = "home_team",
    right_on = "team_name_short"
)

# do renaming and cleaning
schedule_locations.rename(
    columns = {
        "arena_location" : "loc_home_team",
        "coords" : "coords_home_team"
    },
    inplace = True
)

schedule_locations.drop(
    columns = "team_name_short",
    inplace = True
)

#--------------------------------------------------
# sometime matches are played outside the US
# find the location for those

outside_us = away_location[
    away_location["home_team"].str.contains("London|Munich|Mexico")
]

# get clean location names
outside_us["loc_home_team"] = outside_us["home_team"].str.extract(".*\((.*)\).*")

# get coords for those locations
arena_locs = outside_us["loc_home_team"].values
coords = []

# loop through all locations
for arena_loc in arena_locs:
    # complete location name
    loc_name = loct.geocode(arena_loc)
    # get longitude and latitude
    lon = loc_name.longitude
    lat = loc_name.latitude
    coord = [lat, lon]
    # store coords
    coords.append(coord)
    
# assing to location data
outside_us["coords_home_team"] = coords

# bring together with the rest of the data
schedule_locations = pd.concat(
    [schedule_locations, outside_us],
    ignore_index = True
)

#--------------------------------------------------
# do some restructuring to make it nicer

# get column names for away and home variables
cols = schedule_locations.columns.values
away_cols = [x for x in cols if "away" in x]
home_cols = [x for x in cols if "home" in x]

# assign new column order
schedule_locations = schedule_locations[away_cols + home_cols]

#--------------------------------------------------
# export

schedule_locations.to_csv(
    join(data_path, "schedule_locations.csv"),
    sep = ";",
    na_rep = np.nan
)