from sstc_core.sites.spectral import sftp_tools, utils
from sstc_core.sites.spectral.stations import Station


def create_record_dictionary( remote_filepath:str, station:Station, platform_type:str,  platform_id:str,  is_legacy: False, backup_dirpath:str= 'aurora02_dirpath', start_time: str = "10:00:00", end_time: str = "14:00:00", split_subdir: str = 'data'):
    
    local_dirpath = station.platforms[platform_type][platform_id]['backups'][backup_dirpath]

    # Get creation date and formatted date
    local_filepath = sftp_tools.get_local_filepath(
        local_dirpath=local_dirpath, 
        remote_filepath=remote_filepath,
        split_subdir= split_subdir,
        )
    
    creation_date = utils.get_image_dates(local_filepath)
    formatted_date = creation_date.strftime('%Y-%m-%d %H:%M:%S')
    normalized_date = creation_date.strftime('%Y%m%d%H%M%S')
    year = creation_date.year
    day_of_year = utils.get_day_of_year(formatted_date)
    station_acronym = station.meta['station_acronym']
    location_id = station.platforms[platform_type][platform_id]['location_id']
    L0_name = f'SITES-{station_acronym}-{location_id}-{platform_id}-DOY_{day_of_year}-{normalized_date}'
    is_L1 = utils.is_within_time_window(
        formatted_date= formatted_date,
        start_time = start_time,
        end_time = end_time )
    # Create the record dictionary
    record_dict = {
        'catalog_guid': None,
        'year': year,
        'creation_date': formatted_date,
        'day_of_year': day_of_year,
        'station_acronym': station_acronym,
        'location_id': location_id,
        'platform_id': platform_id,
        'platform_type': platform_type,
        'is_legacy': is_legacy,
        'L0_name': L0_name,
        'is_L1': is_L1,
        'catalog_filepath': local_filepath,
        'source_filepath': remote_filepath, 
        'tag_id': 0,        
    }
    
    record_dict['catalog_guid'] =  utils.generate_unique_id(
        record_dict, 
        variable_names= ['creation_date', 'station_acronym', 'location_id', 'platform_id'] )
    
    return record_dict
    
