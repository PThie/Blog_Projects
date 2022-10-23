#--------------------------------------------------
# load libraries

suppressPackageStartupMessages(
  {
    library(targets)
    library(tarchetypes)
    library(future)
    library(future.callr)
    library(here)
    library(sf)
    library(dplyr)
    library(docstring)
    library(roxygen2)
    library(qs)
    library(ggplot2)
  }
)

#--------------------------------------------------
# set working directory

setwd(here())

#--------------------------------------------------
# define paths

data_path <- here("data")
output_path <- here("output")
code_path <- here("code")

#--------------------------------------------------
# targets settings
plan(callr)

#--------------------------------------------------
# read in functions

lapply(
  list.files(
    code_path,
    pattern = "\\.R$",
    full.names = TRUE
  ),
  source
)

#--------------------------------------------------
# target elements

rlang::list2(
  tar_qs(
    munic_shapes,
    read_and_prepare()
  ),
  tar_target(
    assigning_names,
    assign_name_cats(munic_shapes)
  )
)

#--------------------------------------------------
# execute

# tar_make_future()
