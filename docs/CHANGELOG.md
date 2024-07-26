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

