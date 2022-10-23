assign_name_cats <- function(munic_shapes){
    #--------------------------------------------------
    # for mapping load state shapes
    state_shapes <- st_read(
        file.path(
            data_path, "municipalities/shapes/vg250_ebenen_1231/VG250_LAN.shp"
        )
    )
    
    # transform
    state_shapes <- state_shapes |>
        st_transform(crs = st_crs(munic_shapes))
    
    #--------------------------------------------------
    # add naming category
    munic_shapes <- munic_shapes |>
        mutate(name_cats = case_when(
            grepl(name, pattern = "burg") == TRUE ~ "burg",
            grepl(name, pattern = "bach") == TRUE ~ "bach",
            grepl(name, pattern = "berg") == TRUE ~ "berg",
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

    num_obs <- munic_shapes |>
        st_drop_geometry() |>
        group_by(name_cats) |>
        summarise(n = n())


    ggplot()+
        geom_sf(
            data = munic_shapes,
            mapping = aes(geometry = geometry, fill = name_cats),
            col = NA
        )+
        geom_sf(
            data = state_shapes,
            mapping = aes(geometry = geometry),
            fill = NA
        )+
        scale_fill_manual(
            values = c(
                "burg" = "darkorange3",
                "bach" = "navyblue",
                "berg" = "darkgreen",
                "hausen" = "yellow",
                "stadt" = "pink",
                "stedt/ staedt" = "red",
                "other" = "white"
            ),
            labels = c(
                "burg" = "-burg",
                "bach" = "-bach",
                "berg" = "-berg",
                "hausen" = "-hausen",
                "stadt" = "-stadt",
                "stedt/ staedt" = "-stedt",
                "other" = "Other"
            ),
            name = "Name ending"
        )+
        theme(
            panel.background = element_blank(),
            axis.line = element_rect()
        )

    #tar_load(munic_shapes)

    
}