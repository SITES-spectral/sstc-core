from ..io_tools import load_yaml
from pathlib import Path
from sstc_core.sites.spectral.stations import Stations 

stations_dirpath = Path(__file__).parent
spectral_dirpath = Path(stations_dirpath).parent
config_dirpath = spectral_dirpath / "config"

meta = {
    "version": '2024_v0.3',
    "station_acronym": "ANS",
    "long_station_name": "Abisko Scientific Research Station",
    "is_active": True,
    "station_name": "Abisko",
    "normalized_station_name": "abisko",
    "locations_dirpath": config_dirpath / 'locations' / 'locations_abisko.yaml',
    "platforms_dirpath": config_dirpath / 'platforms' / 'platforms_abisko.yaml',    
    'location': {'epsg:4326': {}, 'epsg:3006': {}}
}

def load_configurations():
    """
    Loads configurations for the Abisko station from YAML files.

    Returns:
    tuple: A tuple containing locations and platforms configuration data.
    """
    # Loading station locations config
    locations = load_yaml(meta["locations_dirpath"])

    # Loading station platforms config
    platforms = load_yaml(meta["platforms_dirpath"])

    return locations, platforms

def get_station_instance(db_dirpath:str = None):
    """
    Creates and returns an instance of the Stations class for the Abisko station.

    Returns:
    Stations: An instance of the Stations class.
    """
    if db_dirpath is None:
        db_dirpath = spectral_dirpath / "databases"
    station_name = meta["station_name"]
    locations, platforms = load_configurations()
    return Stations(db_dirpath, station_name, meta=meta, locations=locations, platforms=platforms)




# Example usage
if __name__ == "__main__":    
    station = get_station_instance()
    

