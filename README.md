# CORDEX domain tables

[![ci](https://github.com/WCRP-CORDEX/domain-tables/actions/workflows/ci.yaml/badge.svg)](https://github.com/WCRP-CORDEX/domain-tables/actions/workflows/ci.yaml)

Grid information of CORDEX domains in machine readable format. 

> [!IMPORTANT]
> Note that the domain identifier changes from CMIP5 to CMIP6 (from `CORDEX_domain` to `domain_id`): The global attribute that defines the domain in CMIP5 is named `CORDEX_domain` where the domain resolution is indicated in degrees, e.g., `EUR-11` means Europe on a 0.11° resolution. The global attribute in CMIP6 is named more precisely as `domain_id` which indicates the domain resolution roughly in km, which means that `EUR-11` becomes `EUR-12`! See also https://github.com/WCRP-CORDEX/cordex-cmip6-cv/issues/2.

## Adding new domains

For establishing a new CORDEX domain one needs to apply to the CORDEX SAT [according to this document](https://cordex.org/wp-content/uploads/2020/09/Domain-Criteria-Document-FINAL.pdf).

## Tables

These tables define CORDEX domains in different coordinate reference systems (CRS) to allow all kinds of downscaling models to participate in CORDEX activities. Please note that the coordinates in the `rotated_grids` and `regular_grids` tables denote the *cell centers* while the coordinates in the `domain_boundaries` table define actual *boundaries* and no cell centers.

* `CORDEX-CMIP6_rotated_grids.csv`: Domain definitions in the rotated pole CRS for the CMIP6 era (`rotated_latitude_longitude`). There might be some updates or additions for certain regions in CORDEX-CMIP6. 
* `CORDEX-CMIP5_rotated_grids.csv`: Domain definitions in the rotated pole CRS in the CMIP5 era (`rotated_latitude_longitude`).
* `CORDEX-CMIP5_regular_grids.csv`: Domain definitions in a regular latitude longitude CRS (`EPSG:4326`).
* `CORDEX-CMIP6_domain_boundaries.csv`: Domain boundaries in a regular latitude longitude CRS (`EPSG:4326`).
