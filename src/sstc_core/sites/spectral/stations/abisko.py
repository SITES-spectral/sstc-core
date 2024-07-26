from ..io_tools import load_yaml
from pathlib import Path

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


locations, platforms = load_configurations()


    

