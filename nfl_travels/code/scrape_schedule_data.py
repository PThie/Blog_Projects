# for references: https://www.nbcsports.com/chicago/bears/which-nfl-teams-will-travel-most-least-2022

#--------------------------------------------------
# import libraries

import os
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = "https://fbschedules.com/nfl-schedule/"

page = requests.get(URL)

soup = bs(page.content, "html.parser")

print(page)