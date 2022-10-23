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
    # load overall stats

    obs_overall <- read.xlsx(
        file.path(
            output_path, "descriptives/obs_overall.xlsx"
        )
    )

    #--------------------------------------------------
    # define globals

    own_dpi <- 800

    #--------------------------------------------------
    # define own theme

    own_theme <- theme(
        panel.background = element_blank(),
        panel.border = element_rect(
            size = 1,
            fill = NA
        )
    )

    #--------------------------------------------------
    # define colors

    pal <- MetBrewer::met.brewer(name = "Archambault")
    pal2 <- MetBrewer::met.brewer(name = "Java")

    #--------------------------------------------------
    # berg and burg plotting

    berg_burg_plot <- ggplot(
        data = assigning_names |> filter(name_cats == "berg" | name_cats == "burg")
    )+
    geom_sf(
        aes(geometry = geometry, fill = name_cats),
        col = NA
    )+
    geom_sf(
        data = state_shapes,
        mapping = aes(geometry = geometry),
        fill = NA
    )+
    scale_fill_manual(
        name = "Naming endings (Obs.)",
        labels = c(
            "berg" = paste0(
                "-berg ", "(", obs_overall$n[obs_overall$name_cats == "berg"], ")"
            ),
            "burg" = paste0(
                "-burg ", "(", obs_overall$n[obs_overall$name_cats == "burg"], ")"
            )
        ),
        values = c(
            "berg" = pal[3],
            "burg" = pal[6]
        )
    )+
    own_theme

    # export
    ggsave(
        plot = berg_burg_plot,
        file.path(
            output_path, "maps/berg_burg_map.png"
        ),
        dpi = own_dpi
    )

    #--------------------------------------------------
    # bach plotting

    bach_plot <- ggplot(
        data = assigning_names |> filter(name_cats == "bach")
    )+
    geom_sf(
        aes(geometry = geometry, fill = name_cats),
        col = NA
    )+
    geom_sf(
        data = state_shapes,
        mapping = aes(geometry = geometry),
        fill = NA
    )+
    scale_fill_manual(
        name = "Naming endings (Obs.)",
        labels = c(
            "bach" = paste0(
                "-bach ", "(", obs_overall$n[obs_overall$name_cats == "bach"], ")"
            )
        ),
        values = c(
            "bach" = pal2[2]
        )
    )+
    own_theme

    # export
    ggsave(
        plot = bach_plot,
        file.path(
            output_path, "maps/bach_map.png"
        ),
        dpi = own_dpi
    )

    #--------------------------------------------------
    # stadt and stedt/ staedt plotting

    stadt_stedt_plot <- ggplot(
        data = assigning_names |> filter(name_cats == "stadt" | name_cats == "stedt/ staedt")
    )+
    geom_sf(
        aes(geometry = geometry, fill = name_cats),
        col = NA
    )+
    geom_sf(
        data = state_shapes,
        mapping = aes(geometry = geometry),
        fill = NA
    )+
    scale_fill_manual(
        name = "Naming endings (Obs.)",
        labels = c(
            "stadt" = paste0(
                "-stadt ", "(", obs_overall$n[obs_overall$name_cats == "stadt"], ")"
            ),
            "stedt/ staedt" = paste0(
                "-stedt/ -städt ", "(", obs_overall$n[obs_overall$name_cats == "stedt/ staedt"], ")"
            )
        ),
        values = c(
            "stadt" = pal[2],
            "stedt/ staedt" = pal[5]
        )
    )+
    own_theme

    # export
    ggsave(
        plot = stadt_stedt_plot,
        file.path(
            output_path, "maps/stadt_stedt_map.png"
        ),
        dpi = own_dpi
    )
}