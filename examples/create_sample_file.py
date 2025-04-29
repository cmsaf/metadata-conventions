"""Create sample CM SAF netCDF file.

Changes compared to CDOP-3 Version

Major:

- Added groups
- Added source attribute
- Added lineage attribute
- Updated conventions/vocabulary versions
- Updated license
- Added timezone to time units
- Changed compression to float + significant_digits + zlib

Minor:
- Fixed timestamp format (added Z for UTC)
- Fixed lat bounds attribute name (typo latg_name)
- Renamed bnds -> bounds for better readability
- Renamed processor attributes
"""

import datetime as dt

import numpy as np
import pyproj
import xarray as xr
from dateutil.rrule import DAILY, rrule
from scipy.ndimage import rotate


class DataTreeMaker:
    def __init__(
        self,
        tstart,
        tend,
        lon_min,
        lon_max,
        lat_min,
        lat_max,
        grid_resol,
        void_timestamps,
    ):
        self.grid_resol = grid_resol
        self.time = self.get_time(tstart, tend)
        self.lon = self.get_lon(lon_min, lon_max, grid_resol)
        self.lat = self.get_lat(lat_min, lat_max, grid_resol)
        self.time_bounds = self.get_time_bounds()
        self.lon_bounds = self.get_lon_bounds()
        self.lat_bounds = self.get_lat_bounds()
        mask = Mask(void_timestamps)
        self.clouds = Clouds(self.time, self.lon, self.lat, mask)
        self.radiation = Radiation(self.time, self.lon, self.lat, mask)
        self.rec_status = RecordStatus(self.time, void_timestamps)

    def get_time(self, tstart, tend):
        time = np.array(
            list(rrule(dtstart=tstart, until=tend, freq=DAILY)), dtype="datetime64[ms]"
        )
        return xr.DataArray(
            time,
            dims="time",
            attrs={
                "axis": "T",
                "bounds": "time_bounds",
                "long_name": "Time",
                "standard_name": "time",
            },
        )

    def get_time_bounds(self):
        time_bounds = self._get_bounds(
            self.time.values, resol=np.timedelta64(1, "D"), align="left"
        )
        return xr.DataArray(
            time_bounds, dims=("time", "bounds"), attrs={"long_name": "Time bounds"}
        )

    def get_lon(self, lon_min, lon_max, dlon):
        lon = np.round(np.arange(lon_min, lon_max + dlon, dlon, dtype="f8"), decimals=1)

        return xr.DataArray(
            lon,
            dims="lon",
            attrs={
                "axis": "X",
                "bounds": "lon_bounds",
                "long_name": "longitude",
                "standard_name": "longitude",
                "units": "degrees_east",
            },
        )

    def get_lon_bounds(self):
        lon_bounds = self._get_bounds(self.lon, self.grid_resol, align="center").astype(
            "float64"
        )
        return xr.DataArray(
            lon_bounds, dims=("lon", "bounds"), attrs={"long_name": "Longitude bounds"}
        )

    def get_lat(self, lat_min, lat_max, dlat):
        lat = np.round(np.arange(lat_min, lat_max + dlat, dlat, dtype="f8"), decimals=1)

        return xr.DataArray(
            lat,
            dims="lat",
            attrs={
                "axis": "Y",
                "bounds": "lat_bounds",
                "long_name": "latitude",
                "standard_name": "latitude",
                "units": "degrees_north",
            },
        )

    def get_lat_bounds(self):
        lat_bounds = self._get_bounds(self.lat, self.grid_resol, align="center").astype(
            "float64"
        )
        return xr.DataArray(
            lat_bounds, dims=("lat", "bounds"), attrs={"long_name": "Latitude bounds"}
        )

    def get_grid_mapping(self):
        crs = pyproj.CRS.from_epsg(4326)
        attrs = crs.to_cf()
        attrs["long_name"] = "Regular lat-lon grid"
        return xr.DataArray(attrs=attrs)

    def get_data_tree(self):
        # Note: It would be nice to create coordinates only in the root group. However,
        # xarray re-defines dimensions in each group which crashes tools like
        # ncview. See https://github.com/pydata/xarray/issues/10241.
        # In the meantime, repeat coordinates in each group.
        coords = self.get_coords()
        return xr.DataTree.from_dict(
            {
                "/": xr.Dataset(attrs=self.get_global_attrs()),
                "/clouds": xr.merge([self.clouds.get_dataset(), coords]),
                "/radiation": xr.merge([self.radiation.get_dataset(), coords]),
            },
        )

    def get_coords(self):
        return xr.Dataset(
            {
                "time_bounds": self.time_bounds,
                "lon_bounds": self.lon_bounds,
                "lat_bounds": self.lat_bounds,
                "record_status": self.rec_status.get_record_status(),
                "latlon_grid": self.get_grid_mapping(),
            },
            coords={
                "time": self.time,
                "lon": self.lon,
                "lat": self.lat,
            },
        )

    def get_global_attrs(self):
        isoformat = "%Y-%m-%dT%H:%M:%SZ"
        lineage = "prov:wasDerivedFrom <https://user.eumetsat.int/catalogue/EO:EUM:DAT:MSG:HRSEVIRI>, <https://doi.org/10.24381/cds.bd0915c6>;"
        return {
            "Conventions": "CF-1.12,ACDD-1.3",
            "creator_email": "contact.cmsaf@dwd.de",
            "creator_name": "DE/DWD",
            "creator_url": "http://www.cmsaf.eu/",
            "date_created": dt.datetime.now().strftime(isoformat),
            "geospatial_lat_max": self.lat_bounds.max().item(),
            "geospatial_lat_min": self.lat_bounds.min().item(),
            "geospatial_lat_resolution": "1 degree",
            "geospatial_lat_units": "degrees_north",
            "geospatial_lon_max": self.lon_bounds.max().item(),
            "geospatial_lon_min": self.lon_bounds.min().item(),
            "geospatial_lon_resolution": "1 degree",
            "geospatial_lon_units": "degrees_east",
            "id": "DOI:10.5676/EUM_SAF_CM/GERDA/V001",
            "instrument": "SEVIRI > Spinning Enhanced Visible and Infrared Imager,"
            "GOES-15 Imager > Geostationary Operational Environmental Satellite 15-Imager,"
            "ABI > Advanced Baseline Imager,"
            "AHI > Advanced Himawari Imager",
            "instrument_vocabulary": "GCMD Instruments, Version 21.0",
            "institution": "EUMETSAT/CMSAF",
            "keywords": "CLOUD PROPERTIES > CLOUD FRACTION,ATMOSPHERIC RADIATION > INCOMING SOLAR RADIATION",
            "keywords_vocabulary": "GCMD Science Keywords, Version 21.0",
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "lineage": lineage,
            "platform": "METEOSAT > METEOSAT-11,GOES > GOES-15,GOES > GOES-16,Himawari > Himawari-8",
            "platform_vocabulary": "GCMD Platforms, Version 21.0",
            "product_version": "1.0",
            "project": "Satellite Application Facility on Climate Monitoring (CM SAF)",
            "references": "http://dx.doi.org/10.5676/EUM_SAF_CM/GERDA/V001",
            "source": "satellite",
            "standard_name_vocabulary": "Standard Name Table (v90, 20 March 2025)",
            "summary": "The CM SAF GEoRing DAtaset (GERDA) provides atmospheric "
            "parameters derived from geostationary satellites. "
            "It is a climate data record covering the time period 2002-2024. "
            "Use cases include climate monitoring, climate model evaluation etc.",
            "time_coverage_duration": "P1M",
            "time_coverage_end": self.time_bounds.max().dt.strftime(isoformat).item(),
            "time_coverage_resolution": "P1D",
            "time_coverage_start": self.time_bounds.min().dt.strftime(isoformat).item(),
            "title": "CM SAF GEoRing DAtaset (GERDA)",
            "CMSAF_processor": "gerda-1.0.0",
            "CMSAF_repeat_cylces": "METEOSAT-11=96, GOES-15=8, GOES-16=96, Himawari-8=144",
        }

    def _get_bounds(self, coords, resol, align):
        if align == "left":
            bounds = [[c, c + resol] for c in coords]
        elif align == "center":
            bounds = [[c - 0.5 * resol, c + 0.5 * resol] for c in coords]
        else:
            raise NotImplementedError
        return np.array(bounds)


class RecordStatus:
    def __init__(self, time, tvoid):
        self.time = time
        self.tvoid = tvoid

    def get_record_status(self):
        rec_status = np.array(
            [1 if i in self.tvoid else 0 for i in range(self.time.size)], dtype="uint8"
        )
        return xr.DataArray(
            rec_status,
            dims="time",
            attrs={
                "comment": "Overall status of each record (timestamp) in this file/group. If a record is flagged as not ok, it is recommended not to use it.",
                "flag_meanings": "ok void bad_quality",
                "flag_values": np.array([0, 1, 2], dtype=rec_status.dtype),
                "long_name": "Record Status",
            },
        )


class Mask:
    def __init__(self, void_timestamps):
        self.void_timestamps = void_timestamps

    def mask_timestamps(self, ds, vars_to_mask):
        time = ds["time"]
        time_to_mask = time[self.void_timestamps]
        for var_name, fill_value in vars_to_mask.items():
            should_be_masked = time.isin(time_to_mask)
            ds[var_name] = ds[var_name].where(~should_be_masked, fill_value)


class Clouds:
    def __init__(self, time, lon, lat, mask):
        self.time = time
        self.lon = lon
        self.lat = lat
        self.mlon, self.mlat = np.meshgrid(self.lon.values, self.lat.values)
        self.mask = mask

    def get_dataset(self):
        ds = xr.Dataset(
            {
                "cfc": self._get_cfc(),
                "nobs": self._get_nobs(),
                "quality": self._get_quality(),
            },
            attrs={
                "title": "Clouds",
                "variable_id": "cfc",
            },
        )
        self.mask.mask_timestamps(ds, {"cfc": np.nan, "nobs": 0})
        return ds

    def _get_cfc(self):
        cfc = np.zeros((self.time.size, self.lat.size, self.lon.size), dtype="float64")
        for t in range(self.time.size):
            lon_term = np.sin(t / 5.0 * np.deg2rad(self.mlon)) ** 2
            lat_term = np.cos(t / 10.0 * np.deg2rad(self.mlat)) ** 2
            cfc[t, :, :] = 100 * lon_term * lat_term
        cfc = xr.DataArray(
            cfc,
            dims=("time", "lat", "lon"),
            attrs={
                "ancillary_variables": "nobs quality",
                "cell_methods": "time: area: mean (interval: 15 minutes interval: 3 km)",
                "long_name": "Daily Mean Cloud Fraction",
                "standard_name": "cloud_area_fraction",
                "units": "%",
                "grid_mapping": "latlon_grid",
            },
        )
        return cfc.where((cfc < 10) | (cfc > 20))

    def _get_nobs(self):
        lon_min = self.lon.values.min()
        lon_max = self.lon.values.max()
        nobs = np.zeros((self.time.size, self.lat.size, self.lon.size), dtype="uint8")
        times = list(range(self.time.size))
        tmax = max(times)
        for t in times:
            nobs[t, :, :] = (
                96
                * np.sin(
                    t
                    / 5.0
                    * np.deg2rad(
                        self.mlon + (lon_max - lon_min) / 2.0 * t / float(tmax)
                    )
                    * np.deg2rad(self.mlat)
                )
                ** 2
            )
        return xr.DataArray(
            nobs,
            dims=("time", "lat", "lon"),
            attrs={
                "cell_methods": "time: area: sum (interval: 15 minutes interval: 3 km)",
                "long_name": "Number of Observations",
                "standard_name": "number_of_observations",
                "units": "1",
                "grid_mapping": "latlon_grid",
            },
        )

    def _get_quality(self):
        lat = self.lat.values
        lon = self.lon.values
        qual = np.zeros((self.time.size, lat.size, lon.size), dtype="uint8")
        low_lats = np.fabs(lat) < 30
        med_lats = np.logical_and(np.fabs(lat) > 30, np.fabs(lat) < 65)
        hi_lats = np.fabs(lat) > 65
        qual[:, low_lats, :] = 0  # good
        qual[:, med_lats, :] = 1  # medium
        qual[:, hi_lats, :] = 2  # bad
        return xr.DataArray(
            qual,
            dims=("time", "lat", "lon"),
            attrs={
                "flag_meanings": "good medium bad",
                "flag_values": np.array([0, 1, 2], qual.dtype),
                "long_name": "Quality",
                "grid_mapping": "latlon_grid",
            },
        )


class Radiation:
    def __init__(self, time, lon, lat, mask):
        self.time = time
        self.lon = lon
        self.lat = lat
        self.mask = mask

    def get_sis(self):
        heart_extent = 1.2
        ntimes, rows, cols = self.time.size, self.lat.size, self.lon.size

        # Add some margin (padding) around the heart
        y, x = np.ogrid[1 : -1 : complex(0, rows), -1 : 1 : complex(0, cols)]

        # Scale x and y to add padding (heart_extent > 1 shrinks the heart to leave room)
        x = x * heart_extent
        y = y * heart_extent

        # Create 2D heart-shaped array
        heart = (x**2 + (5 * y / 4 - np.sqrt(np.abs(x))) ** 2 - 1) <= 0

        # Rotate array for each timestep
        hearts = np.zeros((ntimes, rows, cols))
        for i in range(ntimes):
            angle = 360 * i / ntimes
            hearts[i, :, :] = rotate(heart, angle=angle, reshape=False)

        return xr.DataArray(
            hearts,
            dims=("time", "lat", "lon"),
            attrs={
                "long_name": "Daily mean Surface Downwelling Shortwave Radiation",
                "standard_name": "surface_downwelling_shortwave_flux_in_air",
                "units": "W m-2",
                "cell_methods": "time: area: mean (interval: 15 minutes interval: 3 km)",
                "grid_mapping": "latlon_grid",
            },
        )

    def get_dataset(self):
        ds = xr.Dataset(
            {
                "sis": self.get_sis(),
            },
            attrs={
                "title": "Radiation",
                "variable_id": "sis",
            },
        )
        self.mask.mask_timestamps(ds, {"sis": np.nan})
        return ds


class DataTreeWriter:
    def get_encoding(self):
        common_enc = {
            "time": {
                "dtype": "float64",
                "units": "days since 2000-01-01T00:00:00Z",
                "calendar": "standard",
                "_FillValue": None,
            },
            "time_bounds": {
                "dtype": "float64",
                "_FillValue": None,
            },
            "lon": {
                "dtype": "float64",
                "_FillValue": None,
            },
            "lon_bounds": {
                "dtype": "float64",
                "_FillValue": None,
            },
            "lat": {
                "dtype": "float64",
                "_FillValue": None,
            },
            "lat_bounds": {
                "dtype": "float64",
                "_FillValue": None,
            },
            "record_status": {
                "dtype": "uint8",
            },
        }
        group_enc = {
            "/clouds": {
                "cfc": {
                    # Assuming CFC has an absolute physical precision of 0.01
                    # (independent of the CFC value), quantize data with two
                    # significant digits to improve compression.
                    "least_significant_digit": 2,
                    "dtype": "float32",
                    "zlib": True,
                },
                "nobs": {"dtype": "uint8", "zlib": True},
                "quality": {"dtype": "uint8", "zlib": True},
            },
            "/radiation": {
                "sis": {
                    # BitGroom quantization only makes sense if all data values
                    # are in the same order of magnitude ([0, 1] here).
                    "dtype": "float32",
                    "significant_digits": 2,
                    "quantize_mode": "BitGroom",
                    "zlib": True,
                },
            },
        }

        # Repeat common encoding for each group
        for group_name in group_enc:
            group_enc[group_name] |= common_enc
        return group_enc

    def write(self, data_tree, filename):
        data_tree.to_netcdf(filename, encoding=self.get_encoding())


if __name__ == "__main__":
    maker = DataTreeMaker(
        tstart=dt.datetime(2020, 1, 1),
        tend=dt.datetime(2020, 1, 31),
        lon_min=-179.5,
        lon_max=179.5,
        lat_min=-89.5,
        lat_max=89.5,
        grid_resol=1.0,
        void_timestamps=[4, 20],
    )
    writer = DataTreeWriter()
    tree = maker.get_data_tree()
    writer.write(tree, "TSTdm20200101000000120IMPGS01GL.nc")
