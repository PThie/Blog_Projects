#--------------------------------------------------
# import libraries

import pandas as pd
import os
from os.path import join
import haversine as hs
import numpy as np

#--------------------------------------------------
# paths

main_path = r"G:\Blog_Projects\nfl_travels"
data_path = main_path + r"\data"

# set directory
os.chdir(main_path)

#--------------------------------------------------
# load data

schedule = pd.read_csv(
    join(data_path, "schedule_locations.csv"),
    sep = ";"
)

# loc1 = (37.2333253, -121.6846349)
# loc2 = (33.9562003, -118.353132)

locs1 = schedule["coords_away_team"]
locs2 = schedule["coords_home_team"].values

# for (loc1, loc2) in zip(locs1, locs2):
#     dist = hs.haversine(loc1, loc2)
#     print(dist)
