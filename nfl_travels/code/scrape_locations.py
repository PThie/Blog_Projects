#--------------------------------------------------
# import libraries

import os
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

#--------------------------------------------------
# paths

main_path = r"G:\Blog_Projects\nfl_travels"
data_path = main_path + r"\data"

# set directory
os.chdir(main_path)

#--------------------------------------------------
# define url

url = "https://geojango.com/pages/list-of-nfl-teams"
page = requests.get(url)

#--------------------------------------------------
# get content and parse
soup = bs(page.content, "html.parser")
tables = soup.find(id = "s-ece35a86-0578-416c-bb6f-c7c0d3687f88") # table of interest

#--------------------------------------------------
# loop through each container row

# number of NFL teams (plus one because of Python counting)
num_cols = 5
num_teams = (5 * 32) + num_cols

# define index numbers for different columns
index_team_name = range(5, num_teams, 5)
index_arena_name = range(6, num_teams, 5)
index_arena_loc = range(7, num_teams, 5)
index_seating = range(8, num_teams, 5)
index_opening = range(9, num_teams, 5)

# create empty data frame for storage
location_data = pd.DataFrame()

# empty list for storage
# aux_list = []

# define function for extracting the relevant information
def extract_data(index, col_name, stor_list):
    """
    Extracts data depending on the index given and stores it into data frame
    
    Args:
        :param int index: Index of the value we are interested in
        :param str col_name: Name of the colum for storing
        :param list stor_list: List for storing intermediate output before
            assigning it to the data frame
        :return: Stores output into data frame
    """
    
    # extracting the data based on index
    for ind in index:
        for row in tables.find_all("td")[ind]:
            row_text = row.get_text(strip = True)
            if row_text:
                stor_list.append(row_text)

    # assign colum to data frame
    location_data[col_name] = stor_list

# loop through all indices and column names
col_names = ["team_name", "arena_name", "arena_location", "seat_cap", "opening"]
indices = [index_team_name, index_arena_name, index_arena_loc, index_seating, index_opening]

for (name, idx) in zip(col_names, indices):
    aux_list = [] # empty list for storage
    extract_data(index = idx, col_name = name, stor_list = aux_list)

#--------------------------------------------------
# export final data table

location_data.to_csv(
    path_or_buf = os.path.join(data_path, "team_locations.csv"),
    sep = ";",
    index = False,
    na_rep = np.nan
)