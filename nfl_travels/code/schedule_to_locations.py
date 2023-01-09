#--------------------------------------------------
# import libraries

import pandas as pd
import os
from os.path import join

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
schedule["away_team"] = schedule["away_team"].str.rstrip()

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
# merge both data sets based on team name (short)

# define function for merge
# depending on whether you want to merge based on away or home
def merge_data(away_home):
    # implement a check whether its the correct value entry
    valid_values = ["away_team", "home_team"]
    if away_home not in valid_values:
        raise ValueError("Wrong entry for away_home!")
    
    # merge based on entry
    schedule_locations = pd.merge(
        schedule,
        locations,
        left_on = away_home,
        right_on = "team_name_short"
    )
    
    # make sure number of rows did not change
    if len(schedule_locations.index) != len(schedule.index):
        print("CAUTION: Number of rows changed after merge!") 
    
    # rename arena location
    col_name = "loc_" + away_home
    schedule_locations.rename(
        columns = {
            "arena_location" : col_name
        },
        inplace = True
    )
    
    # drop short name
    schedule_locations.drop(
        columns = "team_name_short",
        inplace = True
    )
    
    return schedule_locations

# apply function depending on whether to look at away or home team
away_data = merge_data(away_home = "away_team")
home_data = merge_data(away_home = "home_team")

# bring both together