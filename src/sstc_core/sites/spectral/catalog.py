import keyring
from sstc_core.sites.spectral import sftp_tools
from sstc_core.sites.spectral.stations import Station


def get_sftp_list(
    station:Station,
    platform_type: str,
    platform_id: str,
    ):
    
    sftp_directory = station.platforms[platform_type][platform_id].get('sftp_dirpath', None)    
    credentials = sftp_tools._get_sftp_credentials()
    
    sftp_filepaths = sftp_tools.list_files_sftp(
        hostname= credentials['hostname'],
        port=credentials['port'] ,
        username=credentials['username'],
        password= credentials ['password'],
        sftp_directory=sftp_directory
    )
    
    return sftp_filepaths



def initialize_catalog(station:Station, platform_type: str = 'PhenoCams'):

    platforms = station.platforms[platform_type] 
       
    sftp_filepaths = get_sftp_list(
        station=station, 
        platform_type=platform_type)
    
    
    
    
