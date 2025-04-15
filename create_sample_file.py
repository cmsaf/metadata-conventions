"""
Changes compared to CDOP-3 Version

- Updated license
- Fixed nobs standard name modifier
- Fixed timestamp format (add Z for UTC)
- Fixed lat bounds attribute name (typo latg_name)
- Renamed bnds -> bounds for better readability
- Renamed processor attributes

TODO:
- Groups
- Update vocabularies
- Add lineage attribute
"""

import xarray as xr
import datetime as dt
from dateutil.rrule import rrule, DAILY
import numpy as np
from xarray_utils.testing import assert_data_close_and_attrs_identical


def get_bounds(coords, resol, align):
    if align == "left":
        bounds = [
            [c, c + resol]
            for c in coords
        ]
    elif align == "center":
        bounds = [
            [c - 0.5 * resol, c + 0.5 * resol]
            for c in coords
        ]
    else:
        raise NotImplementedError
    return np.array(bounds)


class DatasetMaker:
    def __init__(self, tstart, tend, lon_min, lon_max, lat_min, lat_max, grid_resol):
        self.grid_resol = grid_resol
        self.time = self.get_time(tstart, tend)
        self.lon = self.get_lon(lon_min, lon_max, grid_resol)
        self.lat = self.get_lat(lat_min, lat_max, grid_resol)
        self.time_bounds = self.get_time_bounds()
        self.lon_bounds = self.get_lon_bounds()
        self.lat_bounds = self.get_lat_bounds()
    
    def get_time(self, tstart, tend):
        time = np.array(
            list(rrule(dtstart=tstart, until=tend, freq=DAILY)),
            dtype="datetime64[ms]"
        )
        return xr.DataArray(time, dims="time", attrs={
            "bounds": "time_bounds",
            "long_name": "Time",
            "standard_name": "time",
        })
    
    def get_time_bounds(self):
        time_bounds = get_bounds(self.time.values, resol=np.timedelta64(1, "D"), align="left")
        return xr.DataArray(time_bounds, dims=("time", "bounds"), attrs={
        "long_name": "Time bounds"
    })

    def get_lon(self, lon_min, lon_max, dlon):
        lon = np.round(
            np.arange(lon_min, lon_max+dlon, dlon, dtype='f8'),
            decimals=1
        )
        
        return xr.DataArray(lon, dims="lon", attrs={
            "bounds": "lon_bounds",
            "long_name": "Longitude",
            "standard_name": "longitude",
            "units": "degrees_east"
        })
    
    def get_lon_bounds(self):
        lon_bounds = get_bounds(self.lon, self.grid_resol, align="center").astype("float64")
        return xr.DataArray(lon_bounds, dims=("lon", "bounds"), attrs={
            "long_name": "Longitude bounds"
        })
    
    
    def get_lat(self, lat_min, lat_max, dlat):
        lat = np.round(
            np.arange(lat_min, lat_max + dlat, dlat, dtype='f8'),
            decimals=1
        )
    
        return xr.DataArray(lat, dims="lat", attrs={
            "bounds": "lat_bounds",
            "long_name": "Latitude",
            "standard_name": "latitude",
            "units": "degrees_east"
        })
    
    def get_lat_bounds(self):
        lat_bounds = get_bounds(self.lat, self.grid_resol, align="center").astype("float64")
        return xr.DataArray(lat_bounds, dims=("lat", "bounds"), attrs={
            "long_name": "Latitude bounds"
        })
    
    def get_cfc(self):
        mlon, mlat = np.meshgrid(self.lon.values, self.lat.values)
        cfc = np.zeros((self.time.size, self.lat.size, self.lon.size), dtype='float64')
        for t in range(self.time.size):
            lon_term = np.sin(t/5.*np.deg2rad(mlon))**2
            lat_term = np.cos(t/10.*np.deg2rad(mlat))**2
            cfc[t, :, :] = 100 * lon_term * lat_term
        cfc = xr.DataArray(cfc, dims=("time", "lat", "lon"), attrs={
            "ancillary_variables": "nobs quality",
            "cell_methods": "time: area: mean (interval: 15 minutes interval: 3 km)",
            "long_name": "Daily Mean Cloud Fraction",
            "standard_name": "cloud_area_fraction",
            "units": "%"
        })
        cfc = cfc.where((cfc < 10) | (cfc > 20))
        return cfc.round(decimals=2)
    
    def get_nobs(self):
        mlon, mlat = np.meshgrid(self.lon.values, self.lat.values)
        lon_min = self.lon.values.min()
        lon_max = self.lon.values.max()
        nobs = np.zeros((self.time.size, self.lat.size, self.lon.size), dtype="uint8")
        times = list(range(self.time.size))
        tmax = max(times)
        for t in times:
            nobs[t, :, :] = 96 * (np.sin(t/5.*np.deg2rad(mlon + (lon_max-lon_min)/2.0*t/float(tmax))*np.deg2rad(mlat))**2)
        return xr.DataArray(nobs, dims=("time", "lat", "lon"), attrs={
            "cell_methods": "time: area: sum (interval: 15 minutes interval: 3 km)",
            "long_name": "Number of Observations",
            "standard_name": "cloud_area_fraction number_of_observations",
            "units": "1"
        })
    
    def get_quality(self):
        lat = self.lat.values
        lon = self.lon.values
        qual = np.zeros((self.time.size, lat.size, lon.size), dtype='uint8')
        low_lats = np.fabs(lat) < 30
        med_lats = np.logical_and(np.fabs(lat) > 30, np.fabs(lat) < 65)
        hi_lats = np.fabs(lat) > 65
        qual[:, low_lats, :] = 0  # good
        qual[:, med_lats, :] = 1  # medium
        qual[:, hi_lats, :] = 2   # bad
        return xr.DataArray(qual, dims=("time", "lat", "lon"), attrs={
            "flag_meanings": "good medium bad",
            "flag_values": np.array([0, 1, 2], qual.dtype),
            "long_name": "Quality",
        })

    def mask_some_timestamps(self, ds):
        time = ds["time"]
        ivoid = [4, 20]
        tvoid = time[ivoid]
        rec_status = np.array([
            1 if t in ivoid else 0
            for t in range(ds["time"].size)
        ], dtype="uint8")
        rec_status = xr.DataArray(
            rec_status, dims="time", attrs={
                "comment": "Overall status of each record (timestamp) in this file. If a record is flagged as not ok, it is recommended not to use it.",
                "flag_meanings": "ok void bad_quality",
                "flag_values": np.array([0, 1, 2], dtype=rec_status.dtype),
                "long_name": "Record Status",
            }
        )
        ds["cfc_dm"] = ds["cfc_dm"].where(~time.isin(tvoid))
        ds["nobs"] = ds["nobs"].where(~time.isin(tvoid), 0)
        ds["record_status"] = rec_status

    def get_global_attrs(self):
        isoformat = "%Y-%m-%dT%H:%M:%SZ"
        return {
            "title": "CM SAF GEoRing DAtaset (GERDA)",
            "summary": "The CM SAF GEoRing DAtaset (GERDA) provides atmospheric "
                       "parameters derived from geostationary satellites. "
                       "The spatial/temporal coverage is 1 degree/1 day from "
                       "2002-2020.",
            "id": "DOI:10.5676/EUM_SAF_CM/GERDA/V001",
            "product_version": "1.0",
            "creator_name": "DE/DWD",
            "creator_email": "contact.cmsaf@dwd.de",
            "creator_url": "http://www.cmsaf.eu/",
            "institution": "EUMETSAT/CMSAF",
            "project": "Satellite Application Facility on Climate Monitoring (CM SAF)",
            "references": "http://dx.doi.org/10.5676/EUM_SAF_CM/GERDA/V001",
            "keywords_vocabulary": "GCMD Science Keywords, Version 8.6",  # FIXME: Update
            "keywords": "CLOUD PROPERTIES > CLOUD FRACTION",
            "Conventions": "CF-1.7, ACDD-1.3",  # FIXME: Update
            "standard_name_vocabulary": "Standard Name Table (v57, 11 July 2018)",  # FIXME: Update
            "date_created": dt.datetime.now().strftime(isoformat),
            "geospatial_lat_units": "degrees_north",
            "geospatial_lat_min": self.lat_bounds.min().item(),
            "geospatial_lat_max": self.lat_bounds.max().item(),
            "geospatial_lat_resolution": "1 degree",
            "geospatial_lon_units": "degrees_east",
            "geospatial_lon_min": self.lon_bounds.min().item(),
            "geospatial_lon_max": self.lon_bounds.max().item(),
            "geospatial_lon_resolution": "1 degree",
            "time_coverage_start": self.time_bounds.min().dt.strftime(isoformat).item(),
            "time_coverage_end": self.time_bounds.max().dt.strftime(isoformat).item(),
            "time_coverage_resolution": "P1D",
            "platform": "METEOSAT > METEOSAT-11, "
                        "GOES > GOES-15, "
                        "GOES > GOES-16, "
                        "Himawari > Himawari-8",
            "platform_vocabulary": "GCMD Platforms, Version 8.6",
            "instrument": "SEVIRI > Spinning Enhanced Visible and Infrared Imager, "
                          "GOES-15 Imager > Geostationary Operational Environmental Satellite 15-Imager, "
                          "GOES-16 Imager > Geostationary Operational Environmental Satellite 16-Imager, "
                          "AHI > Advanced Himawari Imager",
            "instrument_vocabulary": "GCMD Instruments, Version 8.6",
            "variable_id": "cfc_dm",
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "CMSAF_processor": "gerda-1.0.0",
            "CMSAF_L2_processor": "gerda-l2-1.0.0",
            "CMSAF_L3_processor": "gerda-l3-1.0.0",
            "CMSAF_repeat_cylces": "METEOSAT-11=96, GOES-15=8, GOES-16=96, "
                                   "Himawari-8=144",
        }

    def get_dataset(self):
        ds = xr.Dataset(
            {
                "time_bounds": self.time_bounds,
                "lon_bounds": self.lon_bounds,
                "lat_bounds": self.lat_bounds,
                "cfc_dm": self.get_cfc(),
                "nobs": self.get_nobs(),
                "quality": self.get_quality()
            },
            coords={
                "time": self.time,
                "lon": self.lon,
                "lat": self.lat,
            },
            attrs=self.get_global_attrs()
        )
        self.mask_some_timestamps(ds)
        return ds

class DatasetWriter:
    def get_encoding(self):
        return {
            "time": {
                "dtype": "float64",
                "units": "days since 1980-01-01 00:00:00",
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
            "cfc_dm": {
                "dtype": "float32",
                "zlib": True,
            },
            "nobs": {
                "dtype": "uint8",
                "zlib": True
            },
            "quality": {
                "dtype": "uint8",
                "zlib": True
            },
            "record_status": {
                "dtype": "uint8",
            }
        }

    def write(self, dataset, filename):
        dataset.to_netcdf(filename, encoding=self.get_encoding())


maker = DatasetMaker(
    tstart=dt.datetime(1980, 1, 1),
    tend=dt.datetime(1980, 1, 31),
    lon_min=-179.5,
    lon_max=179.5,
    lat_min=-89.5,
    lat_max=89.5,
    grid_resol=1.0,
)
writer = DatasetWriter()
ds = maker.get_dataset()
writer.write(ds, "test.nc")
ds.close()

ds_tst = xr.open_dataset("test.nc")
ds_ref = xr.open_dataset("../metadata_standard/cmsaf_cdop3_tcdr_sample.nc")
assert_data_close_and_attrs_identical(ds_tst, ds_ref)
