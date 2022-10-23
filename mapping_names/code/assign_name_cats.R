assign_name_cats <- function(munic_shapes){

    #--------------------------------------------------
    # add naming category
    munic_shapes <- munic_shapes |>
        mutate(name_cats = case_when(
            grepl(name, pattern = "burg") == TRUE ~ "burg",
            grepl(name, pattern = "bach") == TRUE ~ "bach",
            #grepl(name, pattern = "berg") == TRUE ~ "berg",
            grepl(name, pattern = "hausen") == TRUE ~ "hausen",
            grepl(name, pattern = "stadt") == TRUE ~ "stadt",
            grepl(name, pattern = "stedt") == TRUE ~ "stedt/ staedt",
            grepl(name, pattern = "städt") == TRUE ~ "stedt/ staedt"
            ),
            name_cats = case_when(
                is.na(name_cats) ~ "other",
                !is.na(name_cats) ~ name_cats
            )
        )

    #--------------------------------------------------
    # number of observations by name category

    num_obs_overall <- munic_shapes |>
        st_drop_geometry() |>
        group_by(name_cats) |>
        summarise(n = n())

    #--------------------------------------------------
    # number of observations by name category and state

    num_obs_state <- munic_shapes |>
        st_drop_geometry() |>
        group_by(name_cats, state) |>
        summarise(n = n())

    #--------------------------------------------------
    # save
    write.xlsx(
        num_obs_overall,
        file.path(
            output_path, "descriptives/obs_overall.xlsx"
        ),
        rownames = FALSE
    )

    write.xlsx(
        num_obs_state,
        file.path(
            output_path, "descriptives/obs_states.xlsx"
        ),
        rownames = FALSE
    )

    #--------------------------------------------------
    # return
    return(munic_shapes)
}