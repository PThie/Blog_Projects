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