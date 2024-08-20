from typing import List, Dict, Any


def get_schema_as_dict(platform_schema: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convert a list of schema dictionaries into a dictionary.

    Parameters
    ----------
    platform_schema : List[Dict[str, Any]]
        A list of dictionaries where each dictionary represents a schema field. 
        Each dictionary should contain the keys 'field_name' and 'field_default_value'.

    Returns
    -------
    Dict[str, Any]
        A dictionary where the keys are the 'field_name' values from the input list, 
        and the corresponding values are the 'field_default_value' from each dictionary.

    Examples
    --------
    >>> platform_schema = [
    ...     {'field_name': 'id', 'field_default_value': None},
    ...     {'field_name': 'name', 'field_default_value': ''},
    ...     {'field_name': 'age', 'field_default_value': 0}
    ... ]
    >>> get_schema_as_dict(platform_schema)
    {'id': None, 'name': '', 'age': 0}

    Notes
    -----
    This function assumes that each dictionary in the `platform_schema` list contains the keys
    'field_name' and 'field_default_value'. If these keys are missing, the function may raise
    a `KeyError`.

    Dependencies
    ------------
    - typing.List
    - typing.Dict
    - typing.Any
    """
    return {schema['field_name']: schema['field_default_value'] for schema in platform_schema}
    

phenocams_schema = [
    {'field_name': 'catalog_guid',
     'field_type': 'VARCHAR',
     'field_default_value': None},
    {'field_name': 'year', 
     'field_type': 'INTEGER', 
     'field_default_value': None},
    {'field_name': 'creation_date',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'day_of_year',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'station_acronym',
    'field_type': 'VARCHAR',
    'field_default_value': None } ,
    {'field_name': 'location_id',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'platform_id',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'ecosystem_of_interest',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'platform_type',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'is_legacy',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'L0_name',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'is_L1',
     'field_type': 'BOOLEAN', 
     'field_default_value': False},
    {'field_name': 'is_ready_for_products_use',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'is_data_processing_disabled',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'catalog_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'origin_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'version_data_processing',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'version_code_sstc_core',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'version_platform_flags',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'version_qflag',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'version_schema_platform_phenocams',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'flags_confirmed',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'has_snow_presence',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'sun_elevation_angle',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'sun_azimuth_angle',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'solar_elevation_class',
    'field_type': 'INTEGER',
    'field_default_value': None},
    {'field_name': 'QFLAG_image_value',
    'field_type': 'INTEGER',
    'field_default_value': None},
    {'field_name': 'QFLAG_image_weight',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'is_in_dataportal',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'fieldsites_filename',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'fieldsites_PID',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'L1_QFI_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'L2_RGB_CIMV_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'L2_GCC_CIMV_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'L2_RCC_CIMV_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'L2_RGB_CISDV_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'L2_GCC_CISDV_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'L2_RCC_CISDV_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'L3_ROI_TS_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'ROI_01_flag_disable_for_processing',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_sun_altitude_low_20deg',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_shadows',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_haze',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_high_brightness',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_low_brightness',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_glare',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_clouds',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_fog',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_water_drops',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_heavy_rain',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_snow',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_ice',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_dirt',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_obstructions',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_birds',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_insects',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_blur',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_mount_loose',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_camera_error',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_01_flag_other',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_disable_for_processing',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_sun_altitude_low_20deg',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_shadows',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_haze',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_high_brightness',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_low_brightness',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_glare',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_clouds',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_fog',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_water_drops',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_heavy_rain',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_snow',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_ice',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_dirt',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_obstructions',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_birds',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_insects',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_blur',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_mount_loose',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_camera_error',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_02_flag_other',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_disable_for_processing',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_sun_altitude_low_20deg',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_shadows',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_haze',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_high_brightness',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_low_brightness',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_glare',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_clouds',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_fog',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_water_drops',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_heavy_rain',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_snow',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_ice',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_dirt',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_obstructions',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_birds',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_insects',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_blur',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_mount_loose',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_camera_error',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'ROI_03_flag_other',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'L2_ROI_01_num_pixels',
    'field_type': 'INTEGER',
    'field_default_value': None},
    {'field_name': 'L2_ROI_01_SUM_Red',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L2_ROI_01_SUM_Green',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L2_ROI_01_SUM_Blue',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_has_snow_presence',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'L3_ROI_01_is_data_processing_disabled',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'L3_ROI_01_QFLAG_value',
    'field_type': 'INTEGER',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_QFLAG_weight',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_num_pixels',
    'field_type': 'INTEGER',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_SUM_Red',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_SUM_Green',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_SUM_Blue',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_MEAN_Red',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_MEAN_Green',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_MEAN_Blue',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_SD_Red',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_SD_Green',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_SD_Blue',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_MEANS_RGB_SUM',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_GCC_daily_value',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_01_RCC_daily_value',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L2_ROI_02_num_pixels',
    'field_type': 'INTEGER',
    'field_default_value': None},
    {'field_name': 'L2_ROI_02_SUM_Red',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L2_ROI_02_SUM_Green',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L2_ROI_02_SUM_Blue',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_has_snow_presence',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'L3_ROI_02_is_data_processing_disabled',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'L3_ROI_02_QFLAG_value',
    'field_type': 'INTEGER',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_QFLAG_weight',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_num_pixels',
    'field_type': 'INTEGER',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_SUM_Red',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_SUM_Green',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_SUM_Blue',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_MEAN_Red',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_MEAN_Green',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_MEAN_Blue',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_SD_Red',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_SD_Green',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_SD_Blue',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_MEANS_RGB_SUM',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_GCC_daily_value',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_02_RCC_daily_value',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L2_ROI_03_num_pixels',
    'field_type': 'INTEGER',
    'field_default_value': None},
    {'field_name': 'L2_ROI_03_SUM_Red',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L2_ROI_03_SUM_Green',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L2_ROI_03_SUM_Blue',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_has_snow_presence',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'L3_ROI_03_is_data_processing_disabled',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'L3_ROI_03_QFLAG_value',
    'field_type': 'INTEGER',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_QFLAG_weight',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_num_pixels',
    'field_type': 'INTEGER',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_SUM_Red',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_SUM_Green',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_SUM_Blue',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_MEAN_Red',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_MEAN_Green',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_MEAN_Blue',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_SD_Red',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_SD_Green',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_SD_Blue',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_MEANS_RGB_SUM',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_GCC_daily_value',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'L3_ROI_03_RCC_daily_value',
    'field_type': 'DOUBLE',
    'field_default_value': None}]