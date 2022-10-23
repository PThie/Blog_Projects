plot_munic_names <- function(assigning_names) {
    #--------------------------------------------------
    # for mapping load state shapes
    state_shapes <- st_read(
        file.path(
            data_path, "municipalities/shapes/vg250_ebenen_1231/VG250_LAN.shp"
        )
    )

    # transform
    state_shapes <- state_shapes |>
        st_transform(crs = st_crs(assigning_names))

    #--------------------------------------------------
    # define colors

    pal <- RColorBrewer::brewer.pal(name = "Dark2", n = 6)
    
    #--------------------------------------------------
    # plotting

    munic_plot <- ggplot()+
        geom_sf(
            data = assigning_names,
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
                "burg" = pal[1],
                "bach" = pal[2],
                #"berg" = pal[3],
                "hausen" = pal[4],
                "stadt" = pal[5],
                "stedt/ staedt" = pal[6],
                "other" = "white"
            ),
            labels = c(
                "burg" = "-burg",
                "bach" = "-bach",
                #"berg" = "-berg",
                "hausen" = "-hausen",
                "stadt" = "-stadt",
                "stedt/ staedt" = "-stedt/ -staedt",
                "other" = "Other"
            ),
            name = "Name ending"
        )+
        theme(
            panel.background = element_blank(),
            panel.border = element_rect(
                size = 1,
                fill = NA
            )
        )
        munic_plot
}