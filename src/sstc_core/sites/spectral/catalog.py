from sstc_core.sites.spectral import sftp_tools, utils
from sstc_core.sites.spectral.stations import Station


def create_record_dictionary(remote_filepath: str, station: Station, platforms_type: str, platform_id: str, 
                             is_legacy: bool = False, backup_dirpath: str = 'aurora02_dirpath', 
                             start_time: str = "10:00:00", end_time: str = "14:00:00", split_subdir: str = 'data') -> dict:
    """
    Creates a dictionary representing a record for a file, including metadata and derived attributes.

    This function constructs a record dictionary for a given file located at `remote_filepath` on an SFTP server. 
    The record includes various metadata such as creation date, station acronym, location ID, platform type, 
    platform ID, whether the data is legacy, and a generated unique ID. The function also checks if the creation 
    time of the file falls within a specified time window and generates an L0 name for the file.

    Parameters:
        remote_filepath (str): The path to the remote file on the SFTP server.
        station (Station): An instance of the Station class containing metadata and platform information.
        platforms_type (str): The type of platform (e.g., 'PhenoCams', 'UAVs', 'FixedSensors', 'Satellites').
        platform_id (str): The identifier for the specific platform.
        is_legacy (bool, optional): Indicates whether the record is considered legacy data. Defaults to False.
        backup_dirpath (str, optional): The directory path used for backup storage in the local filesystem. Defaults to 'aurora02_dirpath'.
        start_time (str, optional): The start of the time window in 'HH:MM:SS' format. Defaults to "10:00:00".
        end_time (str, optional): The end of the time window in 'HH:MM:SS' format. Defaults to "14:00:00".
        split_subdir (str, optional): The subdirectory name used to organize local paths. Defaults to 'data'.

    Returns:
        dict: A dictionary containing the record information, including metadata, derived attributes, and a unique ID.

    Example:
        ```python
        station = Station()  # Assuming Station is a class with necessary metadata
        remote_filepath = '/remote/path/to/data/subdir/file1.jpg'
        platform_type = 'camera'
        platform_id = '001'
        record_dict = create_record_dictionary(remote_filepath, station, platform_type, platform_id)
        print(record_dict)
        ```

    Raises:
        Exception: If there are issues retrieving or processing the file data.
    """
    local_dirpath = station.platforms[platform_type][platform_id]['backups'][backup_dirpath]

    # Get creation date and formatted date
    local_filepath = sftp_tools.get_local_filepath(
        local_dirpath=local_dirpath, 
        remote_filepath=remote_filepath,
        split_subdir=split_subdir
    )
    
    creation_date = utils.get_image_dates(local_filepath)
    formatted_date = creation_date.strftime('%Y-%m-%d %H:%M:%S')
    normalized_date = creation_date.strftime('%Y%m%d%H%M%S')
    year = creation_date.year
    day_of_year = utils.get_day_of_year(formatted_date)
    station_acronym = station.meta['station_acronym']
    location_id = station.platforms[platform_type][platform_id]['location_id']
    ecosystem_of_interest = station.platforms[platform_type][platform_id]['ecosystem_of_interest']
    platform_type = station.platforms[platforms_type][platform_id][ 'platform_type'] 
    L0_name = f'SITES-{station_acronym}-{location_id}-{platform_id}-DOY_{day_of_year}-{normalized_date}'
    is_L1 = utils.is_within_time_window(
        formatted_date=formatted_date,
        start_time=start_time,
        end_time=end_time
    )

    # Create the record dictionary
    record_dict = {
        'catalog_guid': None,
        'year': year,
        'creation_date': formatted_date,
        'day_of_year': day_of_year,
        'station_acronym': station_acronym,
        'location_id': location_id,
        'platform_id': platform_id,
        'ecosystem_of_interest': ecosystem_of_interest,
        'platform_type': platform_type,
        'is_legacy': is_legacy,
        'L0_name': L0_name,
        'is_L1': is_L1,
        'catalog_filepath': local_filepath,
        'source_filepath': remote_filepath, 
        'tag_id': 0,        
    }
    
    record_dict['catalog_guid'] = utils.generate_unique_id(
        record_dict, 
        variable_names=['creation_date', 'station_acronym', 'location_id', 'platform_id']
    )
    
    return record_dict


def populate_station_db(
    station: Station,
    sftp_filepaths: list,
    platform_id: str,
    platform_type: str = 'PhenoCams',
    backup_dirpath: str = 'aurora02_dirpath',
    start_time: str = "10:00:00",
    end_time: str = "14:00:00",
    split_subdir: str = 'data'
) -> bool:
    """
    Populates the station database with records based on SFTP file paths.

    This function iterates over a list of file paths from an SFTP server, creates record dictionaries,
    and inserts them into the station's DuckDB database. It checks if a record already exists based on the
    `catalog_guid` before insertion.

    Parameters:
        station (Station): An instance of the Station class for database operations.
        sftp_filepaths (list): A list of file paths on the SFTP server to process.
        platform_id (str): The identifier for the specific platform.
        platform_type (str, optional): The type of platform (default is 'PhenoCams').
        backup_dirpath (str, optional): The directory path used for backup storage in the local filesystem.
        start_time (str, optional): The start of the time window in 'HH:MM:SS' format (default is "10:00:00").
        end_time (str, optional): The end of the time window in 'HH:MM:SS' format (default is "14:00:00").
        split_subdir (str, optional): The subdirectory name to split the file path on (default is 'data').

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        for remote_filepath in sftp_filepaths:
            # Create record dictionary for the given file
            record = create_record_dictionary(
                remote_filepath=remote_filepath,
                station=station,
                platform_type=platform_type,
                platform_id=platform_id,
                is_legacy=False,
                backup_dirpath=backup_dirpath,
                start_time=start_time,
                end_time=end_time,
                split_subdir=split_subdir
            )
            
            catalog_guid = record.get('catalog_guid')
            if not catalog_guid:
                print(f"Failed to generate catalog_guid for file: {remote_filepath}")
                continue

            # Define table name based on platform details
            table_name = f"{platform_type}_{record['location_id']}_{platform_id}"

            # Check if the record already exists
            if not station.catalog_guid_exists(table_name=table_name, catalog_guid=catalog_guid):
                station.add_station_data(table_name=table_name, data=record)
            else:
                print(f"Record with catalog_guid {catalog_guid} already exists in {table_name}.")

        return True

    except Exception as e:
        print(f"An error occurred during the population of the station database: {e}")
        return False

    finally:
        station.close_connection()
