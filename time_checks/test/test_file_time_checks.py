"""
test_file_time_checks.py
========================

Tests for the checks in the `file_time_checks.py` module.
"""

from netCDF4 import Dataset

from time_checks.file_time_checks import *
from time_checks.test.mock_netcdf import MockNCDataset
from time_checks import utils, time_utils, settings, constants

# INCLUDE MockNCDataset in supported settings
settings.supported_datasets.append(MockNCDataset)


def test_check_file_name_time_format_fail_1():
    eg_names = [
        "mrsos_day_HadGEM2-ES_historical_r1i1p1_19991201-2005.nc",
        "hopeful",
        "20040101011.nc",
        "/badc/data/something-19990909-19990909.nc"
    ]

    for fname in eg_names:
        mock_ds = MockNCDataset(fname)
        assert(check_file_name_time_format(mock_ds) is False)


def test_check_file_name_time_format_success_1():
    eg_names = ["mrsos_yr_HadGEM2-ES_historical_r1i1p1_1999-2005.nc",
                "mrsos_mon_HadGEM2-ES_historical_r1i1p1_199912-200511.nc",
                "mrsos_day_HadGEM2-ES_historical_r1i1p1_19991201-20051130.nc",
                "mrsos_3hr_HadGEM2-ES_historical_r1i1p1_199912010101-200511302359.nc",
                "mrsos_6hr_HadGEM2-ES_historical_r1i1p1_199912010304-200511300501.nc",
                "/badc/data/something_19990909-19990910.nc"]

    for fname in eg_names:
        mock_ds = MockNCDataset(fname)
        assert(check_file_name_time_format(mock_ds) is True)


def test_check_file_name_matches_time_var_success_1():
    ds = Dataset('test_data/cmip5/mrsos_day_HadGEM2-ES_historical_r1i1p1_19991201-20051130.nc')
    assert(check_file_name_matches_time_var(ds, time_index_in_name=-1, tolerance='days:1') is True)

def test_check_file_name_matches_time_var_success_2():
    ds = Dataset('test_data/cmip5/tas_Amon_HadGEM2-ES_historical_r1i1p1_198412-200511.nc')
    assert(check_file_name_matches_time_var(ds, time_index_in_name=-1, tolerance='days:16') is True)


def test_check_file_name_matches_time_var_fail_1():
    ds = Dataset('test_data/cmip5/mrsos_day_HadGEM2-ES_historical_r1i1p1_19991201-20051130.nc')
    assert(check_file_name_matches_time_var(ds, time_index_in_name=-1, tolerance='hours:1') is False)


def test_check_time_format_matches_frequency_success_1():

    eg_names = ['mrsos_Oyr_HadGEM2-ES_historical_r1i1p1_1999-2005.nc',
                'mrsos_Amon_HadGEM2-ES_historical_r1i1p1_199912-200511.nc',
                'mrsos_day_HadGEM2-ES_historical_r1i1p1_19991201-20051130.nc',
                'mrsos_3hr_HadGEM2-ES_historical_r1i1p1_199912010101-200511300101.nc',
                'mrsos_6hrLev_HadGEM2-ES_historical_r1i1p1_1999120101-2005113001.nc',
                ]

    for fname in eg_names:
        mock_ds = MockNCDataset(fname)
        assert(check_time_format_matches_frequency(mock_ds, frequency_index=1, time_index_in_name=-1) is True)


def test_check_time_format_matches_frequency_fail_1():

    eg_names = ['mrsos_Oyr_HadGEM2-ES_historical_r1i1p1_19991201-20051130.nc',
                'mrsos_3hr_HadGEM2-ES_historical_r1i1p1_1999-2005.nc',
                'mrsos_6hrLev_HadGEM2-ES_historical_r1i1p1_199912-200511.nc',
                'mrsos_day_HadGEM2-ES_historical_r1i1p1_1999120101-2005113001.nc',
                'mrsos_Amon_HadGEM2-ES_historical_r1i1p1_199912010101-200511300101.nc',
                ]

    for fname in eg_names:
        mock_ds = MockNCDataset(fname)
        assert(check_time_format_matches_frequency(mock_ds, frequency_index=1, time_index_in_name=-1) is False)


def test_check_time_format_matches_frequency_test_all_combinations():

    positives = [('Oyr', '1999-2005'),
                 ('Amon', '199912-200511'),
                 ('monClim', '199912-200511'),
                 ('day', '19991201-20051130'),
                 ('3hr', '199912010101-200511300101'),
                 ('subhr', '199912010101-200511300101'),
                 ('6hrLev', '1999120101-2005113001')]
    frequencies = ('Oyr', 'Amon', 'day', '3hr', '6hrLev')
    time_ranges = ('1999-2005', '199912-200511', '19991201-20051130',
                   '199912010101-200511300101', '1999120101-2005113001')

    all_combos = [(frequency, time_range) for frequency in frequencies for time_range in time_ranges]

    for frequency, time_range in all_combos:
        fname = 'mrsos_{}_HadGEM2-ES_historical_r1i1p1_{}.nc'.format(frequency, time_range)
        mock_ds = MockNCDataset(fname)
        expected_result = (frequency, time_range) in positives
        result = check_time_format_matches_frequency(mock_ds, frequency_index=1, time_index_in_name=-1)
        assert(result == expected_result)

def test_check_regular_time_axis_increments_success_1():
    ds = Dataset('test_data/cmip5/mrsos_day_HadGEM2-ES_historical_r1i1p1_19991201-20051130.nc')
    assert(check_regular_time_axis_increments(ds, frequency_index=1) is True)


def test_check_regular_time_axis_increments_fail_1():
    ds = Dataset('test_data/cmip5/mrsos_day_HadGEM2-ES_historical_r2i1p1_19991201-20051130.nc')
    assert(check_regular_time_axis_increments(ds, frequency_index=1) is False)
 

def test_check_valid_temporal_element_success_1():
    eg_names = ['mrsos_Oyr_HadGEM2-ES_historical_r1i1p1_1999-2005.nc',
                'mrsos_Amon_HadGEM2-ES_historical_r1i1p1_199912-200511.nc',
                'mrsos_day_HadGEM2-ES_historical_r1i1p1_19991201-20051130.nc',
                'mrsos_3hr_HadGEM2-ES_historical_r1i1p1_199912010101-200511300101.nc',
                'mrsos_6hrLev_HadGEM2-ES_historical_r1i1p1_1999120101-2005113001.nc',
                ]

    for fname in eg_names:
        mock_ds = MockNCDataset(fname)
        assert(check_valid_temporal_element(mock_ds, time_index_in_name=-1) is True)

def test_check_valid_temporal_element_fail_1():
    eg_names = ['mrsos_Oyr_HadGEM2-ES_historical_r1i1p1_1999-4005.nc',
                'mrsos_Amon_HadGEM2-ES_historical_r1i1p1_199900-200513.nc',
                'mrsos_day_HadGEM2-ES_historical_r1i1p1_19991201-20051132.nc',
                'mrsos_3hr_HadGEM2-ES_historical_r1i1p1_199912010100-200511300160.nc',
                'mrsos_6hrLev_HadGEM2-ES_historical_r1i1p1_1999120100-2005113024.nc',
                ]

    for fname in eg_names:
        mock_ds = MockNCDataset(fname)
        assert(check_valid_temporal_element(mock_ds, time_index_in_name=-1) is False)


