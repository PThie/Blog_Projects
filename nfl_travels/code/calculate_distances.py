# for references: 
# https://www.nbcsports.com/chicago/bears/which-nfl-teams-will-travel-most-least-2022
# https://www.cbssports.com/nfl/news/heres-how-far-each-nfl-team-will-travel-in-2022-steelers-get-huge-advantage-buccaneers-face-brutal-slate/

#--------------------------------------------------
# import libraries

import pandas as pd
import os
from os.path import join
import haversine as hs
import numpy as np
from haversine import Unit

#--------------------------------------------------
# paths

main_path = r"D:\Blog_Projects\nfl_travels"
data_path = main_path + r"\data"

# set directory
os.chdir(main_path)

#--------------------------------------------------
# load data

schedule = pd.read_csv(
    join(data_path, "schedule_locations.csv"),
    sep = ";"
)

#--------------------------------------------------
# calculating the distance rowwise

# define function for calculation
def calc_dist(
    lat_away_team, lon_away_team, lat_home_team, lon_home_team
):
    dist = hs.haversine(
        (lat_away_team, lon_away_team),
        (lat_home_team, lon_home_team)
    )
    return dist

# apply function
schedule["travel_dist_km"] = schedule.apply(
    lambda row: calc_dist(
        row["lat_away_team"], row["lon_away_team"], row["lat_home_team"], row["lon_home_team"]
    ),
    axis = 1
)

#--------------------------------------------------
# summarise distance by away team
# NOTE: Does not account for the circumstance that some teams combine trips
# and do not travel home once on the road

sum_distance = schedule.groupby("away_team")["travel_dist_km"].sum()
sum_distance = sum_distance.to_frame()
sum_distance["travel_dist_mi"] = sum_distance["travel_dist_km"] * 0.621371

# account for the fact that each travel is a round trip
sum_distance["travel_dist_km"] = sum_distance["travel_dist_km"] * 2
sum_distance["travel_dist_mi"] = sum_distance["travel_dist_mi"] * 2

#--------------------------------------------------
# add distances outside US also for home teams
# because even though they are considered to play at home they have to travel 
# as well

# CONTINUE here

outside_us = schedule[
    schedule["loc_home_team"].str.contains("London|Munich|Mexico")
]

# print(loc1)
# print(schedule[schedule["away_team"] == "Seahawks"])
print(outside_us)
# loc1 = (37.2333253, -121.6846349)
# loc2 = (33.9562003, -118.353132)

# x = pd.DataFrame(, columns = ["lat", "lon"])
# print(schedule["coords_away_team"].tolist())
# for (loc1, loc2) in zip(locs1, locs2):
#     dist = hs.haversine(loc1, loc2)
#     print(dist)
