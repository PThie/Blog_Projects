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
# define URL
url = "https://www.sportingnews.com/us/nfl/news/nfl-schedule-2022-dates-times-tv-channels/bkz3xhyr6tiu4kl2456dalro"
page = requests.get(url)

#--------------------------------------------------
# get content and parse
soup = bs(page.content, "html.parser")
tables = soup.find_all("table")

#--------------------------------------------------
# loop through tables to get the desired rows

# data frame for storage
headers = ["game", "time", "news_channel"]
game_schedule = pd.DataFrame(columns = headers)

# loop through tables
for table in tables:
    for element in table.find_all("tr"):
        unfiltered_row = element.find_all("td")
        row = [i.text for i in unfiltered_row]
        if len(row) != 3:
            pass # do nothing
        else:
            length = len(game_schedule)
            game_schedule.loc[length] = row

#--------------------------------------------------
# cleaning

# drop unwanted columns
game_schedule.drop(["time", "news_channel"], axis = 1, inplace = True)

# split game column
game_schedule[["away_team", "home_team"]] = game_schedule["game"].str.split("vs.", expand = True)

# drop game column
game_schedule.drop(["game"], axis = 1, inplace = True)

# drop rows with nonsense
game_schedule = game_schedule[~game_schedule.away_team.str.contains("\xa0")]
#game_schedule = game_schedule[~game_schedule.home_team.str.contains("None")]

#--------------------------------------------------
# export

game_schedule.to_csv(
    path_or_buf = os.path.join(data_path, "game_schedule.csv"),
    sep = ";",
    index = False,
    na_rep = np.nan
)