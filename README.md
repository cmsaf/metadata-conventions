# CM SAF Metadata Conventions

Metadata conventions for CM SAF datasets.

This is the current working draft for CDOP-4. The CDOP-3 version can be found
[here](https://github.com/cmsaf/metadata-conventions/blob/e70865e02488be40663128f857b701319b22d6b8/README.md).

## Catalog Conventions

Conventions for metadata stored in data catalogs, such as unique dataset ID, documentation or related datasets.
They help making the dataset findable and re-usable.

👉 [Catalog conventions document](catalog_conventions.md)

## File Conventions

Conventions for metadata included in each file, such as units, coordinates etc. They help understanding and working
with the data.

👉 [File conventions document](file_conventions.md)

### Sample Files

There are two sample files available for download,

- [Instantaneous](https://public.cmsaf.dwd.de/data/perm/metadata_standard/TSTin20200101000000120IMPGS01GL.nc): Multiple time steps, including some empty records.
- [Daily Mean](https://public.cmsaf.dwd.de/data/perm/metadata_standard/TSTdm20200101000000120IMPGS01GL.nc): Single time step.

They were created by this [python script](examples/create_sample_file.py).

## Compliance Checkers

Collection of tools for checking metadata compliance of your products.

### CF Conventions

Tools for checking compliance with CF conventions.

#### CF Checker

For checking compliance with CF conventions we usually recommend
[cf-checker](https://github.com/cedadev/cf-checker).
Example:

```
conda install -c conda-forge cfchecker
cfchecks myfile.nc
```

However, the project seems inactive and there are some open issues. For example,
[groups are not supported](https://github.com/cedadev/cf-checker/issues/73), yet.
Workaround: flatten the file using
[netcdf-flattener](https://gitlab.eumetsat.int/open-source/netcdf-flattener)
and check the flattened file.
```python
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
```

So if you run into issues with `cf-checker` you might want to check out the following
alternatives.

#### IOOS Compliance Checker

The [IOOS Compliance Checker](https://github.com/ioos/compliance-checker) is pretty mature
and the project is active. However, it doesn't support groups either. Example:

```
conda install -c conda-forge compliance-checker
cchecker.py -t cf:1.8 -t acdd:1.3 myfile.nc
```

#### xrlint

[xrlint](https://github.com/bcdev/xrlint) is a linter for xarray Datasets/DataTrees,
but can also be used to check NetCDF files. The project is still young, but actively
developed and groups are supported. Example:

```
conda install -c conda-forge xrlint
xrlint --init
xrlint myfile.nc
```

### CM SAF Metadata Conventions

We provide a dedicated tool [cmsaf-checker](https://github.com/cmsaf/cmsaf-checker) for checking against the CM SAF
metadata conventions.

```
pip install git+https://github.com/cmsaf/cmsaf-checker
cmsaf-checker myfile.nc
```
