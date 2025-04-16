import subprocess

import netCDF4
import netcdf_flattener


def flatten():
    # Flatten netCDF groups, because CF checker doesn't support groups, yet
    # (https://github.com/cedadev/cf-checker/issues/73)
    with netCDF4.Dataset("test.nc") as input_ds:
        with netCDF4.Dataset("flat.nc", mode="w") as output_ds:
            netcdf_flattener.flatten(input_ds, output_ds)

            # Remove attributes added by flattener
            for attr in output_ds.ncattrs():
                if attr.startswith("__flattener"):
                    output_ds.delncattr(attr)


if __name__ == "__main__":
    flatten()
    subprocess.run(["cfchecks", "flat.nc"], check=True)  # noqa: S607
