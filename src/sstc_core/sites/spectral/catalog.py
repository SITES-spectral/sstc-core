import yaml
import os
from sstc_core.sites.spectral.io_tools import load_yaml
from sstc_core.sites.spectral.stations import Station


def update_records_count(station:Station, platforms_type: str, platform_id: str, new_count: int):
    """
    Updates the records_count for a specific platform in the YAML configuration file.

    Parameters:
        yaml_filepath (str): The path to the YAML file containing the station platforms configuration.
        platforms_type (str): The type of platform (e.g., 'PhenoCams').
        platform_id (str): The identifier for the specific platform.
        new_count (int): The new records count to update.

    Raises:
        FileNotFoundError: If the specified YAML file does not exist.
        KeyError: If the specified platform type or platform ID does not exist in the YAML structure.
    """
    
    yaml_filepath = station.meta['platforms_filepath'] 
    
    config = load_yaml(yaml_filepath)
    

    # Navigate to the specified platform and update the records_count
    try:
        config[platforms_type][platform_id]['records_count'] = new_count
    except KeyError as e:
        raise KeyError(f"The specified key '{e.args[0]}' does not exist in the YAML structure.")

    with open(yaml_filepath, 'w') as file:
        yaml.safe_dump(config, file, default_flow_style=False)

