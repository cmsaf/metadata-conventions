# CM SAF Metadata Conventions

CM SAF Metadata Conventions, Version 3 (CDOP-4), May 2025.

## Table of Contents

- [Introduction](#introduction)
- [File Names](#file-names)
- [Format](#format)
- [Metadata](#metadata)
- [Coordinates](#coordinates)
- [Missing Records](#missing-records)
- [Compression](#compression)

## Introduction

The CM SAF metadata conventions describe the file name and format of our products as well as their 
metadata. They are mandatory for newly generated datasets.

The goal is to make our products more uniform, which will not only improve the user
experience but also facilitate our daily work with the data. We try to keep it in sync with the standards
from [C3S](https://climate.copernicus.eu/) and [obs4MIPs](https://pcmdi.github.io/obs4MIPs/) in order to
be prepared for contributing to these projects. We also follow the 
[FAIR](https://www.go-fair.org/fair-principles/) principles.

## File Names

All products must follow
the [CMSAF file naming convention](http://www.cmsaf.eu/EN/Products/NamingConvention/Naming_Convention_node.html).

## Format

CM SAF products must be distributed in [NetCDF4](https://www.unidata.ucar.edu/software/netcdf/) format with
internal compression, see also [compression](#compression).


## Metadata

Metadata make a dataset self-describing and drastically improve its usability.
The [CF Conventions](http://cfconventions.org/) are our primary metadata standard. They are widely accepted in the
climate and forecast community. In addition, we agreed to follow these conventions:

- [Attribute Convention for Data Discovery](http://wiki.esipfed.org/index.php/Attribute_Convention_for_Data_Discovery) (partly)
- [Copernicus metadata recommendations](https://confluence.ecmwf.int/display/COPSRV/Metadata+recommendations+for+encoding+NetCDF+products+based+on+CF+convention)
- [obs4MIPs data specification](https://pcmdi.github.io/obs4MIPs/dataStandards.html)

The resulting metadata conventions are summarized in the sections below.

### Global Attributes

The following global attributes must be included in each file.

| Attribute                 | Content                                                         | Example                                                                                                                                                                            | Comment                    | Changelog                           |
|---------------------------|-----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|-------------------------------------|
| title                     | Dataset Title                                                   | CM SAF FCDR of SSM/I brightness temperatures                                                                                                                                       |                            |                                     |
| summary                   | Dataset summary, including intended usage.                      | Fundamental Climate Data Record (FCDR) of Special Sensor Microwave/Imager (SSM/I) brightness temperatures. Intended usage: Input for thematic climate data records and reanalysis. |                            | Add intended usage                  |
| id                        | DOI                                                             | DOI:10.5676/EUM_SAF_CM/FCDR_SSMI/V001                                                                                                                                              |                            | DOI now includes both TCDR and ICDR |
| product_version           | Dataset version as text: Major.Minor                            | 1.0                                                                                                                                                                                |                            |                                     |
| creator_name              | Creator name                                                    | DE/DWD                                                                                                                                                                             | GCMD Providers if possible |                                     |
| creator_email             | `contact.cmsaf@dwd.de`                                          |                                                                                                                                                                                    | Fixed                      |                                     |
| creator_url               | `https://www.cmsaf.eu/`                                         |                                                                                                                                                                                    | Fixed                      |                                     |
| institution               | `EUMETSAT/CMSAF`                                                |                                                                                                                                                                                    | Fixed                      |                                     |
| project                   | `Satellite Application Facility on Climate Monitoring (CM SAF)` |                                                                                                                                                                                    | Fixed                      |                                     |
| references                | Link to DOI resolver                                            | https://doi.org/10.5676/EUM_SAF_CM/FCDR_SSMI/V001                                                                                                                                  |                            |                                     |
| keywords_vocabulary       | `GCMD Science Keywords, Version 21.0`                           |                                                                                                                                                                                    | Minimum Version            | Version update                      |
| keywords                  | comma separated list from GCMD Science Keywords                 | EARTH SCIENCE > SPECTRAL/ENGINEERING > MICROWAVE > BRIGHTNESS TEMPERATURE                                                                                                          |                            |                                     |
| Conventions               | `CF-1.12, ACDD-1.3`                                             |                                                                                                                                                                                    | Minimum Version            | Version update                      |
| standard_name_vocabulary  | `Standard Name Table (v90, 20 March 2025)`                      |                                                                                                                                                                                    | Minimum Version            | Version update                      |
| date_created              | ISO 8601:2004                                                   | YYYY-MM-DDThh:mm:ss<zone>                                                                                                                                                          |                            |                                     |
| geospatial_lat_units      | from udunits                                                    | degrees_north                                                                                                                                                                      |                            |                                     |
| geospatial_lat_min        | as double                                                       | -90.0                                                                                                                                                                              | =leftmost lat bound        |                                     |
| geospatial_lat_max        | as double                                                       | 90.0                                                                                                                                                                               | =rightmost lat bound       |                                     |
| geospatial_lat_resolution | as text                                                         | 0.5 degree                                                                                                                                                                         | if applicable              |                                     |
| geospatial_lon_units      | from udunits                                                    | degrees_east                                                                                                                                                                       |                            |                                     |
| geospatial_lon_min        | as double                                                       | -180.0                                                                                                                                                                             | =leftmost lon bound        |                                     |
| geospatial_lon_max        | as double                                                       | 180.0                                                                                                                                                                              | =rightmost lon bound       |                                     |
| geospatial_lon_resolution | as text                                                         | 0.5 degree                                                                                                                                                                         | if applicable              |                                     |
| time_coverage_start       | ISO 8601:2004                                                   | YYYY-MM-DDThh:mm:ss<zone>                                                                                                                                                          | =leftmost time bound       |                                     |
| time_coverage_end         | ISO 8601:2004                                                   | YYYY-MM-DDThh:mm:ss<zone>                                                                                                                                                          | =rightmost time bound      |                                     |
| time_coverage_duration    | ISO 8601:2004                                                   | P[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss]                                                                                                                                                   | if applicable              |                                     |
| time_coverage_resolution  | ISO 8601:2004                                                   | P[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss]                                                                                                                                                   | if applicable              |                                     |
| platform                  | comma separated list from GCMD Platform List                    | DMSP 5D-3/F16 > Defense Meteorological Satellite Program-F16                                                                                                                       | if applicable              |                                     |
| platform_vocabulary       | `GCMD Platforms, Version 21.0`                                  |                                                                                                                                                                                    | Minimum version            | Version update                      |
| instrument                | comma separated list from GCMD Instrument List                  | SSMIS > Special Sensor Microwave Imager/Sounder                                                                                                                                    | if applicable              |                                     |
| instrument_vocabulary     | `GCMD Instruments, Version 21.0`                                |                                                                                                                                                                                    | Minimum version            | Version update                      |
| history                   | as text                                                         | "Wed Jun 28 11:22:20 2017: ncatted -a myattr,global,a,c,myvalue myfile.nc"                                                                                                         | if applicable              |                                     |
| date_modified             | ISO 8601:2004                                                   | YYYY-MM-DDThh:mm:ss<zone>                                                                                                                                                          | if applicable              |                                     |
| variable_id               | Comma separated list of primary variables in the file           | ctp,cth,ctt                                                                                                                                                                        |                            |                                     |
| license                   | `https://creativecommons.org/licenses/by/4.0/`                  |                                                                                                                                                                                    |                            | New license                         |
| source                    | `satellite observation`                                         |                                                                                                                                                                                    |                            | New attribute                       |
| lineage                   | DOIs/URLs of sources this dataset was derived from              | prov:wasDerivedFrom \<https://user.eumetsat.int/catalogue/EO:EUM:DAT:MSG:HRSEVIRI\>, \<https://doi.org/10.24381/cds.bd0915c6\>;                                                    |                            | New attribute                       |


Keywords/Platforms/Instruments can be looked up in the [GCMD Keyword viewer](https://gcmd.earthdata.nasa.gov/KeywordViewer/).


#### Additional Global Attributes

Of course you can add more global attributes. We recommend adding a 'CMSAF_' prefix in order to prevent name conflicts
with the CF/ACDD Conventions. Here are some ideas to get started:

| Attribute           | Content                                              | Example                            |
|---------------------|------------------------------------------------------|------------------------------------|
| CMSAF_processor     | Overall (Re)processing framework                     | claas-v2.5.0                       |
| CMSAF_L2_processor  | Software used to generate level 2 products           | SAFNWC-MSGv2012, CPPv5.1           |
| CMSAF_L3_processor  | Software used to generate level 3 products           | CMSAFMSGL3_V2.1                    |
| CMSAF_orbits        | Number of orbits contributed by each platform        | NOAA-18=12, NOAA-19=11, METOP-A=10 |
| CMSAF_repeat_cycles | Number of repeat cycles contributed by each platform | METEOSAT-10=48, METEOSAT-11=48     |

> **Tip:** It is recommended to add time-dependent metadata not only as global attributes but also as variables. This
> facilitates concatenation along the time-dimension without losing metadata.

### Variable Attributes

Variables should be described with the following attributes:

| Attribute                              | Content                               | Example                                                         | Comment                                                                                                                                                                                                              | Changelog     |
|----------------------------------------|---------------------------------------|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| long_name                              | Variable name written out             | Cloud Fraction                                                  | Exception: Bounds variables                                                                                                                                                                                          |               |
| standard_name                          | CF Standard Name                      | cloud_area_fraction                                             | If any, see [Standard Name Table](http://cfconventions.org/standard-names.html). You may also propose new standard names.                                                                                            |               | 
| units                                  | Physical units                        | %                                                               | If applicable, [udunits](http://www.unidata.ucar.edu/software/udunits/) compatible                                                                                                                                   |               | 
| cell_methods                           | Applied statistics                    | time: area: mean (interval: 15 minutes interval: 3 km)          | Aggregated variables only ([7.3: Cell Methods](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.12/cf-conventions.html#cell-methods))                                                                  |               |
| ancillary_variables                    | Ancillary variables                   | nobs, quality                                                   | Use this to reference number of observations, quality, standard deviation etc. (if any, [3.4. Ancillary Data](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.12/cf-conventions.html#ancillary-data)) |               |
| flag_values, flag_masks, flag_meanings | Flag decoding instructions            | flag_values=[0, 1, 2], flag_meanings='good medium bad'          | Flag type variables only ([3.5. Flags](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.12/cf-conventions.html#flags))                                                                                 |               |
| bounds                                 | Reference to corresponding bounds     | lat_bounds                                                      | Coordinate variables only ([7.1. Cell Boundaries](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.12/cf-conventions.html#cell-boundaries))                                                            |               |
| add_offset, scale_factor               | Unpacking parameters                  |                                                                 | If applicable ([8.1. Packed Data](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.12/cf-conventions.html#packed-data))                                                                                |               |
| grid_mapping                           | Specifies coordinate reference system | See [Coordinate Reference System](#coordinate-reference-system) | Recommended, but not mandatory                                                                                                                                                                                       | New attribute |


## Coordinates

Rules for coordinate variables.

### Type

> **_New in version 3!_**

Coordinate variables must specify their type using the `axis` attribute, see
[4. Coordinate Types](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.12/cf-conventions.html#coordinate-types).

### Bounds

Each coordinate variable (time, lat, lon, ...) must be accompanied by cell boundaries as described
[7.1. Cell Boundaries](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.12/cf-conventions.html#cell-boundaries).
Contiguous intervals share their endpoints, for example

```
lon = [0.5, 1.5, 2.5]
lon_bounds = [
  [0, 1],
  [1, 2],
  [2, 3]
]
```

### Grid Cell Alignment

* Time coordinates represent the left boundary of the covered temporal interval.
* Geographical coordinates represent the centre of the gridbox.
* For regular grids: `(lon, lat) = (0, 0)` is the lower left corner of one grid cell.

### Coordinate Reference System

> **_New in version 3!_**

It is recommended to specify the coordinate reference system (CRS) with a
[grid mapping](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.12/cf-conventions.html#grid-mappings-and-projections)
variable. This has two advantages:

- Includes information about the figure of the earth (e.g. WGS84 ellipsoid, sphere, etc.).
- Lat/Lon coordinates can be computed from the grid mapping, which is useful for irregular
  grids (e.g. geostationary projection) where the two-dimensional coordinate arrays 
  would consume a lot of disk space if included in every file.

Examples:

1. Regular lat-lon grid based on WGS84 ellipsoid

```
dimensions:
    time = 1 ;
    lat = 180 ;
    lon = 360 ;
variables:
    double lat(lat) ;
            lat:units = "degrees_north" ;
            lat:standard_name = "latitude" ;
    double lon(lon) ;
            lon:units = "degrees_east" ;
            lon:standard_name = "longitude" ;
    float precipitation(time, lat, lon) ;
            string precipitation:grid_mapping = "latlon_grid" ;
    double latlon_grid ;
            latlon_grid:inverse_flattening = 298.257223563 ;
            latlon_grid:reference_ellipsoid_name = "WGS 84" ;
            latlon_grid:_FillValue = NaN ;
            latlon_grid:horizontal_datum_name = "World Geodetic System 1984 ensemble" ;
            latlon_grid:semi_major_axis = 6378137. ;
            latlon_grid:prime_meridian_name = "Greenwich" ;
            latlon_grid:semi_minor_axis = 6356752.31424518 ;
            latlon_grid:longitude_of_prime_meridian = 0. ;
            latlon_grid:geographic_crs_name = "WGS 84" ;
            latlon_grid:grid_mapping_name = "latitude_longitude" ;
            latlon_grid:crs_wkt = "GEOGCRS[\"WGS 84\",ENSEMBLE[\"World Geodetic System 1984 ensemble\",MEMBER[\"World Geodetic System 1984 (Transit)\"],MEMBER[\"World Geodetic System 1984 (G730)\"],MEMBER[\"World Geodetic System 1984 (G873)\"],MEMBER[\"World Geodetic System 1984 (G1150)\"],MEMBER[\"World Geodetic System 1984 (G1674)\"],MEMBER[\"World Geodetic System 1984 (G1762)\"],MEMBER[\"World Geodetic System 1984 (G2139)\"],MEMBER[\"World Geodetic System 1984 (G2296)\"],ELLIPSOID[\"WGS 84\",6378137,298.257223563,LENGTHUNIT[\"metre\",1]],ENSEMBLEACCURACY[2.0]],PRIMEM[\"Greenwich\",0,ANGLEUNIT[\"degree\",0.0174532925199433]],CS[ellipsoidal,2],AXIS[\"geodetic latitude (Lat)\",north,ORDER[1],ANGLEUNIT[\"degree\",0.0174532925199433]],AXIS[\"geodetic longitude (Lon)\",east,ORDER[2],ANGLEUNIT[\"degree\",0.0174532925199433]],USAGE[SCOPE[\"Horizontal component of 3D system.\"],AREA[\"World.\"],BBOX[-90,-180,90,180]],ID[\"EPSG\",4326]]" ;
```

2. Geostationary projection with custom ellipsoid

```
dimensions:
    time = 1 ;
    y = 3712 ;
    x = 3712 ;
variables:
    double y(y) ;
            y:units = "m" ;
            y:standard_name = "projection_y_coordinate" ;
    double x(x) ;
            x:units = "m" ;
            x:standard_name = "projection_x_coordinate" ;
    byte rain_mask(time, y, x) ;
            string rain_mask:grid_mapping = "geostationary_grid" ;
    double geostationary_grid ;
        geostationary_grid:crs_wkt = "PROJCRS[\"unknown\",BASEGEOGCRS[\"unknown\",DATUM[\"unknown\",ELLIPSOID[\"unknown\",6378169,295.488065897014,LENGTHUNIT[\"metre\",1,ID[\"EPSG\",9001]]]],PRIMEM[\"Greenwich\",0,ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8901]]],CONVERSION[\"unknown\",METHOD[\"Geostationary Satellite (Sweep Y)\"],PARAMETER[\"Longitude of natural origin\",0,ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8802]],PARAMETER[\"Satellite Height\",35785831,LENGTHUNIT[\"metre\",1,ID[\"EPSG\",9001]]],PARAMETER[\"False easting\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8806]],PARAMETER[\"False northing\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8807]]],CS[Cartesian,2],AXIS[\"(E)\",east,ORDER[1],LENGTHUNIT[\"metre\",1,ID[\"EPSG\",9001]]],AXIS[\"(N)\",north,ORDER[2],LENGTHUNIT[\"metre\",1,ID[\"EPSG\",9001]]]]" ;
        geostationary_grid:semi_major_axis = 6378169. ;
        geostationary_grid:semi_minor_axis = 6356583.8 ;
        geostationary_grid:inverse_flattening = 295.488065897014 ;
        geostationary_grid:reference_ellipsoid_name = "unknown" ;
        geostationary_grid:longitude_of_prime_meridian = 0. ;
        geostationary_grid:prime_meridian_name = "Greenwich" ;
        geostationary_grid:geographic_crs_name = "unknown" ;
        geostationary_grid:horizontal_datum_name = "unknown" ;
        geostationary_grid:projected_crs_name = "unknown" ;
        geostationary_grid:grid_mapping_name = "geostationary" ;
        geostationary_grid:sweep_angle_axis = "y" ;
        geostationary_grid:perspective_point_height = 35785831. ;
        geostationary_grid:latitude_of_projection_origin = 0. ;
        geostationary_grid:longitude_of_projection_origin = 0. ;
        geostationary_grid:false_easting = 0. ;
        geostationary_grid:false_northing = 0. ;
```

There are tools for converting between CRS and CF grid mapping, for example

- [pyproj](https://pyproj4.github.io/pyproj/dev/build_crs_cf.html)
- [pyresample](https://pyresample.readthedocs.io/en/latest/api/pyresample.html#pyresample.geometry.AreaDefinition.from_cf)


### Precision

Always use 64 bit double for coordinates (lat/lon, time, pressure levels, ...) and round the values to the
number of significant digits in order to minimize floating point errors. Choose a time origin close to your dataset
(not Julian Day for example).


## Missing Records

If a product could not be generated for whatever reason (missing input data, processing failure, ...), an "empty"
product containing only fill values has to be generated. Composite files consisting of multiple timestamps must always
contain the same number of timestamps. If no data could be generated for a certain timestamp, all variables must be set
to fill value at that particular timestamp.

In order to quickly indicate the overall status of each record in a file, every file must provide a `record_status`
variable. Example:

```
netcdf test {
dimensions:
        time = 1234 ;
variables:
        byte record_status(time) ;
                record_status:long_name = "Record Status" ;
                record_status:comment = "Overall status of each record (timestamp) in this file. If a record is flagged as not ok, it is recommended not to use it." ;
                record_status:flag_values = 0B, 1B, 2B ;
                record_status:flag_meanings = "ok void bad_quality" ; }
```

The default for valid records is 0 (ok). If a record is missing, set the corresponding status to 1 (void). Quality
concerns should be indicated with record status 3 (bad_quality).


## Compression

> **_New in version 3!_**

Compression recommendations:

- Enable NetCDF's internal zlib compression.
- Round floating point data to the number of significant digits and store them as float type. Together with
  zlib enabled this achieves good compression.
- Only pack data with scale factor and offset if there's no alternative, because it can make reading the data more
  complicated.

### Quantization

Quantization can dramatically improve compression. However, it is lossy.

- Starting with version 4.9.0, `libnetcdf` offers a selection of
  [quantization algorithms](https://docs.unidata.ucar.edu/netcdf-c/4.9.2/md__media_psf_Home_Desktop_netcdf_releases_v4_9_2_release_netcdf_c_docs_quantize.html).
- In addition, the `netCDF4` Python library offers quantization via the `least_significant_digit`
  keyword argument, see
  [Dataset.createVariable](https://unidata.github.io/netcdf4-python/#netCDF4.Dataset.createVariable).


Here's a comparison of some compression and quantization methods:


#### File size

Random noise rounded/quantized to two significant digits.

| Compression method             | Type                                 | Size (bytes) | Compression |
|:-------------------------------|--------------------------------------|-------------:|------------:|
| None                           | lossless                             |      328,192 |         1.0 |
| zlib                           | lossless                             |      283,436 |         1.2 |
| rounded + zlib                 | lossless (within physical precision) |      210,369 |         1.6 |
| least_significant_digit + zlib | lossy                                |       90,909 |         3.6 |
| BitGroom + zlib                | lossy                                |       70,156 |         4.7 |

#### Truncation Error

Round/truncate (1.123456, 1001.123456) to the given number of digits.

| Significant Digits |     Rounded | least_significant_digit |      BitGroom |
|-------------------:|------------:|------------------------:|--------------:|
|  **Small Numbers** |             |                         |               |
|                  6 |    1.123456 |              1.12345600 |    1.12345552 |
|                  5 |    1.123460 |              1.12345886 |    1.12345505 |
|                  4 |    1.123500 |              1.12347412 |    1.12344360 |
|                  3 |    1.124000 |              1.12304688 |    1.12304688 |
|                  2 |    1.120000 |              1.12500000 |    1.12109375 |
|                  1 |    1.100000 |              1.12500000 |    1.09375000 |
|  **Large Numbers** |             |                         |               |
|                  6 | 1001.123456 |           1001.12345600 | 1001.12353516 |
|                  5 | 1001.123460 |           1001.12345886 | 1001.12500000 |
|                  4 | 1001.123500 |           1001.12347412 | 1001.12500000 |
|                  3 | 1001.124000 |           1001.12304688 | 1001.25000000 |
|                  2 | 1001.120000 |           1001.12500000 | 1002.00000000 |
|                  1 | 1001.100000 |           1001.12500000 | 1008.00000000 |

BitGroom achieves the best compression, but only makes sense if the data range is small, because the truncation
error increases for larger numbers. Files compressed with `least_significant_digits` are a bit larger,
but the truncation error is much smaller.
