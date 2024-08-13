## [v0.11.20]
- Improved `phenocams.rois_mask_and_sum` to return the sum of pixel values for each channel and not treated as a single channel input image.
- Minor improvements
- record schema changed.  

## [v0.11.19] 
- Improved `phenocams.overlay_polygons` to show the roi names at the centroid of the ROI polygon
- Added `phenocams.rois_mask_and_sum` 
- Added `phenocams.convert_rois_sums_to_single_dict`
  
## [v0.11.18]
- Chasing a Heisenbug

## [v0.11.17]
- Fixed `get_solar_elevation_class` issue not showing in `utils`

## [v0.11.16]
- Fixed issue with `utils.solar_illumination_conditions`

## [v0.11.15]
- refactored `get_solar_elevation_class` into `utils` instead of `qflags`.
- Improved documentation for `compute_qflags`

## [v0.11.14]
- Fixed issue of wrongly assign results from `calculate_sun_position` as tuple instead of dictionary. 

## [v0.11.13]
- Ensured sun_elevation_angle

## [v0.11.12]
- Added `station.phenocam_rois`
- Improved record schema to accomodate rois has snow presence
- Renamed the `processing_level_products_dict` keys

## [v0.11.11]
- Added `station.get_station_platform_geolocation_point`
- Added `utils.solar_illumination_conditions` 

## [v0.11.10]
- Renamed `station.stations_names()` to `station.get_stations_names_dict()`  

## [v0.11.9]
- Fixed issue `get_time_interval`  


## [v0.11.8]
- Added `Station.get_time_interval` 

## [v0.11.7]
- Refined product names for Phenocams
  
## [v0.11.6]
- Documentation updates
- updated `compute_qflag` to handle default_temporal_resolution=True, i.e. every 30 min between images, else valid only for hourly/bi-hourly temporal resolution


## [v0.11.5]
- Added `Station.select_random_record`

## [v0.11.4]
- Updated `Station.create_table` to take a schema dictionary holding field names and data types, instead of implying the datatypes.

## [v0.11.3]
- Added `Station.delete_fields_from_table`
  
## [v0.11.2]
- Updated `Station.add_new_fields_to_table` to take a list of dictionaries that have, field_type, field_name, and field_value`   

## [v0.11.1]
- Fixed minor import issue.
- added `utils.copy_file_with_new_name`
- Updated `records` schema for phenocams

## [v0.11.0]
- Updated `Station.create_record_dictionary` by adding as input the `processing_level_products_dict` that defaults to `None`
- Added `sites.spectral.data_products.phenocams.overlay_polygons`
- Added `utils.calculate_sun_position`
- Added `sites.spectral.data_products.phenocams.get_solar_elevation_class`
- Added `sites.spectral.data_products.qflags.get_solar_elevation_class`
- Added `sites.spectral.data_products.qflags.compute_qflag`

## [v0.10.3]
- Added  `Station.get_records_ready_for_products_by_year`
- Added `sites.spectral.data_products.phenocams.compute_RGB_daily_average` Note: here is defined the `product_name = f'SITES-{station_acronym}-{location_id}-{platform_id}-{datatype_acronym}-{year}-DOY_{day_of_year}_{product_processing_level}.JPG'`
- Added `sites.spectral.data_products.phenocams.compute_GCC_RCC`
  
## [v0.10.2] 
- Added `utils.get_month_day` as string.
- Code prunning.

## [v0.10.1]
- Fixed minor issue with wrongly assigned `flag_high_quality`

## [v0.10.0]
- Added `flag_high_quality` 

## [v0.9.6] 
- Fixed issue with `Station.update_record_by_catalog_guid`

## [v0.9.5]
- Fixed on `confirmed_flags` missing saving `normalized_quality_index` 

## [v0.9.4]
- Added `Station.add_new_fields_to_table`
- Expanded `flags` to include haze, clouds, shadows and ice. 


## [v0.9.3]
- Added `Station.get_day_of_year_min_max`
- Added `Station.get_records_by_year_and_day_of_year`

## [v0.9.2]
- Fixed minor issue with optional variables not handled properly `assess_image_quality` function. 

## [v0.9.1]
- Added `skip` variable to skip the auto-assessing of image quality and auto calculation quality index. Useful when populating databases for the first time.

## [v0.9.0]
- refactored `is_quality_assessed` to `is_quality_confirmed`
- added `Station.get_unique_years`
- depeciated `Station.get_L1_records`
- Added `Station.get_records_as_dictionary_by_day_L0_name`
- Code pruning and minor refactoring

## [v0.8.5]
- Changed `flag_brightness` range to be 0 and 1.
- `detect_birds` defaults to `False` instead of `None`
- Added `utils.have_values_changed` 
  
## [v0.8.4]
- Added `utils.day_of_year_to_month_day`
- Added `utils.extract_keys_with_prefix`
- Added `utils.set_all_values_to_false`
- updated `phenocam_quality_weights.yaml` all weights set to 1 but snow=0.1 

## [v0.8.3]
- Fixed issue not loading `config.catalog_filepaths`

## [v0.8.2]
- Added `config.github_backups.yaml`
- Added `config.catalog_default_filepaths.yaml`
- Added `config.catalog_filepaths` 

## [v0.8.1]
- Fixed issue `station.stations_names`  

## [v0.8.0]
- Added `sites.spectral.tasks_manager` 

## [v0.7.7]
- Added `DuckDBManager.update_by_catalog_guid` 

## [v0.7.6]
- Added `DuckDBManager.get_filtered_records` 
- Fixed issue on `Station.get_L1_records` not returning correctly the results.

## [v0.7.5]
- Added `DuckDBManager.get_table_schema`
- Updated results of `Station.get_L1_records` to return all fields of the record. The resulted is a dictionary nested with year as the first key, day_of_year as the second key, and L0_name as the third key. 
- `stations.stations_names` now reads from `config.stations_names.yaml`  instead of the hardcoded of the dictionary.
   
## [v0.7.4]
- added `quality_index_weights_version` in the record_dict

## [v0.7.3]
- `is_ready_for_products_use` is now included in the record_dict

## [v0.7.2]
- Ensured quality flags were properly returned boolean when necessary.

## [v0.7.1]
- `detect_birds` flag has been disabled until better training model is found, defaults to False. It requires to manually label the image. 

## [v0.7.0]
- updated record schema for phenocams, to include quality flags.
- Autocalculate the quality flags when building the `records_dict`
- refactored `Station.update_is_L2` to `Station.update_is_quality_assessed`

## [v0.6.1]
-  updated quality detection flags to include `flag_other`
-  expanded `record_dict` with flags and `normalized_quality_index`

## [v0.6.0]
- Added module `sites.spectral.image_quality`
- Added `config.phenocam_quality_weights.yaml`
- Added `sites.spectral.data_products.phenocams` module 

## [v0.5.1]
- improved `station.get_L1_record
- added `station.update_is_L2` 

## [v0.5.0]
- extended `record_dict` with `is_L2=False` 

## [v0.4.2]
- added `catalog.get_records_count`   

## [v0.4.1]
- added `catalog.update_records_count` 

## [v0.4.0]
- refactored `populate_station_db` into the `Station` class instead of having it in `catalog` module
- refactored `create_record_dictionary` into the `Station` class instead of having it in `catalog` module
- code-pruning `catalog` module
  
## [v0.3.11]
- code-pruning of `DuckDBManager` 

## [v0.3.10]
- fixed bug during initailizaion of database if it does not exist. 
- refactored database auto-naming to `f"{self.normalized_station_name}_catalog.db"`  

## [v0.3.9]
- fixed bug `self.db_filepath.exists()` at `Stations` module.

## [v0.3.8]
- Added `DuckDBmanager.close_if_open`
  
## [v0.3.7] 
- Fixed db connections locked in `Station.get_record_count` and `Station.get_L1_records`

## [v0.3.6] 
- fixed wrong table name using `platform_id` instead of `platform_type`

## [v0.3.5.1] 
- fixed wrong table name using `platforms_type` instead of `platform_type`
  
## [v0.3.5] 
- Better error handling on `catalog.populate_station_db`

## [v0.3.4.2] 
- fixed bug

## [v0.3.4.1]
- Fixed refactored variable `platforms_type` in Station class.

## [v0.3.4]
- Added `Catalog.populate_station_db` 

## [v0.3.3]
- added `Station.get_record_count`
- added `Station.get_L1_records` 

## [v0.3.2]
- Added `Station.catalog_guid_exists` and `Station.insert_record` 

## [v0.3.1.7]
- expanded schema for `catalog.create_record_dict`

## [v0.3.1.6]
- Added `sftp_tools.get_new_files_to_download`
- Improved documentation.

## [v0.3.1.5]
- fixed incorrect call to `generate_unique_id` in `catalog` module

## [v0.3.1.4]
- bug fixed

## [v0.3.1.3]
- DEPRECIATED `catalog.get_sftp_list`
- Added `sftp_tools.get_local_filepath`
- Added `utils.is:within_time_window`
- Updated `sftp_tools.download_file`

## [v0.3.1.2]
- Added `catalog.get_sftp_list`
- Added `sftp_tools.is_file_downloaded_locally`
- Added `sftp_tools.get_remote_file_size`

## [v0.3.1.1]
- Improved platforms `.yaml` metadata 
- Refactored `catalog` module to use `Station` class
- Code prunning `sft_tools` module

## [v0.3.1]
- Renamed `Stations` class to `Station`
- Improved `Station` class by self construct based on the `station_name`

## [v0.3.0]
- added `utils.normalize_string`
- added `utils.generate_unique_id` creates a short hash. 
- Depreciated `stations.PlatformData` class
- Depreciated `duckdb_manager` module. Refactored insie the `stations` module
- Added `DuckDBManager` class to `stations` module
- Added stations.generate_query_dict
- Added `Stations` class that inherits from DuckDBManager   

## [v0.2.13]
- Improved result dictionary for `get_catalog_filepaths_by_year_and_day` to return if it has been selected for processing L2 & L3 processing
- added `utils.phenocam_save_selected_images`

## [v0.2.12]
- Improved result dictionary for `get_catalog_filepaths_by_year_and_day` to return its metadata. 

## [v0.2.11.2]
- Fixing incorrect use of STRFTIME on a VARCHAR field, which requires a TIMESTAMP or DATE type. To resolve this, we need to ensure that creation_date is correctly cast to TIMESTAMP before applying STRFTIME. 

## [v0.2.11.1]
- Minor fix `get_catalog_filepaths_by_year_and_day`  use STRFTIME to extract the year instead of EXTRACT which expects a DATE or TIMESTAMP type, not a VARCHAR.

## [v0.2.11]
- Added `phenocam_rois` to platforms_abisko.yaml 

## [v0.2.10]
- Improved methods for the `DuckDBManager`
  - `add_day_of_year_column`
  - `filter_by_time_window`
  - `populate_L0_name`
  - `check_is_L1` 
  - `get_catalog_filepaths_by_year_and_day` filtering capabilities based on the `year` and `is_L1` status.

## [v0.2.9.3] 
- Minor fix for day of year expected timedate formatted as '%Y-%m-%d %H:%M:%S'.
  
## [v0.2.9.2]
- Minor fix on the `get_catalog_filepaths_by_year_and_day` method. TypeError: tuple indices must be integers or slices, not str.
  
## [v0.2.9.1]
- Minor fix on the `list_tables` method
  
## [v0.2.9]
- Improved methods for the `DuckDBManager`:
  - `list_tables` new method
  - `get_catalog_filepaths` new method
  - `get_source_filepaths`
  - `get_catalog_filepaths_by_year_and_day` of the year
- Added `utils.get_day_of_year` with trailing zeros. 

## [v0.2.8.1]
- Minor fixes
  
## [v0.2.8]
- Added `duckdb_manager.download_files_and_create_records`
- Improved `sftp_tools.download_file` to split the subdirs based on a variable `split_subdir="data"`
- Updated `getting_started` docs with `secure_keyring_credentials.md`

## [v0.2.7]
- Updated `sftp_tools.download_file` to preserve the SFTP directory structure 

## [v0.2.6]
- Refactored location ids and plattform ids, to use underscore instead of hyppens to avoid errors by creating table names with hyppens in duckdb wich is not allowed. 

## [v0.2.5.2]
- Added record_id hashed for `duckdb_manager`

## [v0.2.5.1]
- updated documentation for `duckdb_manager`

## [v0.2.5] 
- Introduced `duckdb_manager` module

## [v0.2.4.0.1] 
- fixed util import error

## [v0.2.4.0] 
- added `sstc_core.sites.spectral.catalog.insert_phenocam_record_to_duckdb` function

## [v0.2.3.3] 
- Updated `sftp_tools.download_file` function

## [v0.2.3.2]
- Fixed relative importing error

## [v0.2.3.1]
- Fixed misspelling relative import of catalog

## [v0.2.3]
- Minor changes on platforms schemas
- Improved docs with getting_started and user_guide
- Added `table_name_decorator` for the `catalog` module
- Added `sites.spectral.StationData` with `get_table_name` inherited from decorator class 


## [v0.2.2]
- Refactored `platforms` as dictionary instead of list
- refactored docs subdiirectories and Rebuild docs 

## [v0.2.1.3]
- Expanded `load_yaml` functionality to allow paths to be instances of `Path` or `str`.

## [v0.2.1.2]
- Fixed config paths 
- Added `sites>spectral>data>duckdb_catalog` in .gitignore

## [v0.2.1.1]
- Fixing config paths

## [v0.2.1]
- Loads locations and platforms configs as properties of each station module.

## [v0.2.0]
- trimmed `core` module.
- added modules `utils`, `sftp` and `catalog`, `io`
- added `config` package for `platforms` and `locations` as yaml files for each station.
- refactored modules `ecosystems` and `mantainance_status` as config yaml files.


## [v0.1.3]
- restricted platforms and locations to match active instruments duing site visit  2024


## [v0.1.2]
- refactored `stations` as package within `sstc_core>sites>spectral>stations|legacy|onboarding|thematic_center`   
- Added `status` module with a description of `stations_status`
- Added in `docs` `instruments_acronyms_construction.md` supporting the platforms
- Depreciated module `sites_spectral_core`
- Added mkdocs
- added `core`module
- `abisko` module


## [v0.1.1]
- Added `sites_spectral_core` module. The module has `stations`, `ecosystems` dictionaries. 

  
## [v0.1.0]
- bare bones 

