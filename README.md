# CORDEX domain tables

Grid information of CORDEX domains in machine readable format. Note that the domain identifier changes from CMIP5 to CMIP6: The global attribute that defines the domain
in CMIP5 is named `CORDEX_domain` where the domain resolution is indicated in degrees, e.g., `EUR-11` means Europe on a 0.11° resolution. The global attribute in CMIP6 is named
more precisely as `domain_id` which indicates the domain resolution roughly in km, which means that `EUR-11` becomes `EUR-12`! See also https://github.com/WCRP-CORDEX/cordex-cmip6-cv/issues/2 

## Tables

* `CORDEX-CMIP5_rotated_grids.csv`: Table with domain definitions in the rotated pole CRS (`rotated_latitude_longitude`).
* `CORDEX-CMIP5_regular_grids.csv`: Table with domain definitions in a regular latitude longitude CRS (`EPSG:4326`).
* `CORDEX-CMIP6_domain_boundaries.csv`: Table with domain boundaries in a regular latitude longitude CRS (`EPSG:4326`).
