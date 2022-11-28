#########################################################
# import libraries

import os
import pandas as pd
from os.path import join
# from os import listdir
# import glob
# import geopandas as gpd
import numpy as np

#########################################################
# paths

main_path = "G:/Blog_Projects/retrieving_osm/"
data_path = join(main_path, "data")
output_path = join(main_path, "output")

#########################################################
# set directory

os.chdir(main_path)
