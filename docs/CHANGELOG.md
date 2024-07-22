## [v0.1.0]
- bare bones 

## [v0.1.1]
- Added `sites_spectral_core` module. The module has `stations`, `ecosystems` dictionaries. 

## [v0.1.2]
- refactored `stations` as package within `sstc_core>sites>spectral>stations|legacy|onboarding|thematic_center`   
- Added `status` module with a description of `stations_status`
- Added in `docs` `instruments_acronyms_construction.md` supporting the platforms
- Depreciated module `sites_spectral_core`
- Added mkdocs
- added `core`module
- `abisko` module

## [v0.1.3]
- restricted platforms and locations to match active instruments duing site visit  2024

## [v0.2.0]
- trimmed `core` module.
- added modules `utils`, `sftp` and `catalog`, `io`
- added `config` package for `platforms` and `locations` as yaml files for each station.
- refactored modules `ecosystems` and `mantainance_status` as config yaml files.

## [v0.2.1]
- Loads locations and platforms configs as properties of each station module.

## [v0.2.1.1]
- Fixing config paths

## [v0.2.1.2]
- Fixed config paths 
- Added `sites>spectral>data>duckdb_catalog` in .gitignore

## [v0.2.1.3]
- Expanded `load_yaml` functionality to allow paths to be instances of `Path` or `str`.
  
## [v0.2.2]
- Refactored `platforms` as dictionary instead of list 