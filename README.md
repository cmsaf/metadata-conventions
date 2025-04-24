# CM SAF Metadata Conventions

Metadata conventions for CM SAF products.

## Metadata Conventions Document

The metadata conventions document is located [here](metadata_conventions.md)

## Sample File

There's a sample file available for
[download](https://public.cmsaf.dwd.de/data/perm/metadata_standard/cmsaf_cdop4_tcdr_sample.nc).
It was created by [this python script](examples/create_sample_file.py). 

Note: Although the file contains groups, coordinates are repeated in each group.
It would be nice to create coordinates only in the root group and inherit them
in subgroups. However, xarray (our go-to Python library for working with
netCDF data) currently re-defines dimensions in each group, which crashes other
tools like ncview. See https://github.com/pydata/xarray/issues/10241.
Proper dimension inheritance is possible though, for example using other
libraries like netCDF4.


## Checking Metadata Compliance

There are two tools for checking metadata compliance of your products:

1. [cf-checker](https://github.com/cedadev/cf-checker) for checking against CF conventions. 
    
   Note: The `cf-checker`
   [doesn't support groups](https://github.com/cedadev/cf-checker/issues/73), yet.
   Workaround: flatten the file using
   [netcdf-flattener](https://gitlab.eumetsat.int/open-source/netcdf-flattener)
   and check the flattened file.
   ```python
   import subprocess
   import netCDF4
   import netcdf_flattener

   def flatten(input_file, output_file):
       with netCDF4.Dataset(input_file) as input_ds:
           with netCDF4.Dataset(output_file, mode="w") as output_ds:
               netcdf_flattener.flatten(input_ds, output_ds)
   
               # Remove attributes added by flattener which trigger
               # cf-checker warnings
               for attr in output_ds.ncattrs():
                   if attr.startswith("__flattener"):
                       output_ds.delncattr(attr)
        
   if __name__ == "__main__":
       flatten("input.nc", "flat.nc")
       subprocess.run(["cfchecks", "flat.nc"], check=True)
   ```
2. `cmsaf-checker` for checking against the CM SAF metadata standard. TODO: Example
