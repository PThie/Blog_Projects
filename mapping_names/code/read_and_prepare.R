read_and_prepare <- function(){
    #' Read and prepare municipality shapes
    #' 
    #' @description Reads in the municipality shape file
    #' and cleans it
    #' 
    #' @return Returns shape of clean municipalities
    #' @author Patrick Thiel
    
    #--------------------------------------------------
    # load data

    munic_shapes <- st_read(
        file.path(
            data_path, "municipalities/shapes/vg250_ebenen_1231/VG250_GEM.shp"
        )
    )

    #--------------------------------------------------
    # clean

    # transform
    munic_shapes <- munic_shapes |>
        st_transform(crs = 4326)

    # remove unnecessary columns
    munic_shapes <- munic_shapes |>
        select(AGS_0, GEN, geometry)

    # rename
    colnames(munic_shapes) <- c("ags", "name", "geometry")

    # add state variable and rename
    munic_shapes <- munic_shapes |>
        mutate(
            state = substr(ags, start = 1, stop = 2),
            state = case_when(
                state == "01" ~ "SH",
                state == "02" ~ "HH",
                state == "03" ~ "NI",
                state == "04" ~ "HB",
                state == "05" ~ "NW",
                state == "06" ~ "HE",
                state == "07" ~ "RP",
                state == "08" ~ "BW",
                state == "09" ~ "BY",
                state == "10" ~ "SL",
                state == "11" ~ "BE",
                state == "12" ~ "BB",
                state == "13" ~ "MV",
                state == "14" ~ "SN",
                state == "15" ~ "ST",
                state == "16" ~ "TH",
            )
        )

    #--------------------------------------------------
    # save
    qsave(
        munic_shapes,
        file.path(
            data_path, "municipalities/clean_munic.shp"
        )   
    )
    
    #--------------------------------------------------
    # return
    return(munic_shapes)
}