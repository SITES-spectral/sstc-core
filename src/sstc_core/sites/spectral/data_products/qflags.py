from sstc_core.sites.spectral import utils
from sstc_core.sites.spectral.stations import Station



def get_solar_elevation_class(sun_elevation: float) -> int:
    """ 
    Categorize the solar elevation angles into 3 classes based on their values.
    The phenocam images are classified into three classes based on sun elevation angles:
    
    - Class 1: 0° - 20°
    - Class 2: 20° - 30°
    - Class 3: > 30°

    This scheme was adopted from the webcam network and image database for studying phenological changes in vegetation in Finland (Peltoniemi et al. 2018). The above class categories are coded as 1, 2, and 3 respectively. 
    Read more about this here: SITES Spectral - Data Quality Flagging (QFLAG) Documentation

    Args:
        sun_elevation (float): The sun elevation angle in degrees.

    Returns:
        int: The class category based on the sun elevation angle.
            - 1 for sun elevation angles between 0° and 20°.
            - 2 for sun elevation angles between 20° and 30°.
            - 3 for sun elevation angles greater than 30°.
    """
    
    if sun_elevation < 20:
        solClass = 1
    elif 20 <= sun_elevation <= 30:
        solClass = 2
    else:
        solClass = 3
        
    return solClass


def compute_qflag(
    latitude_dd: float,
    longitude_dd: float, 
    records_dict:dict,
    has_snow_presence:bool = False,
    timezone_str='Europe/Stockholm'):
    
    
    datetime_list = [v['creation_date'] for k, v in records_dict.items()]
    
    mean_datetime_str =  utils.mean_datetime_str(datetime_list=datetime_list)
    sun_elevation_angle, _ = utils.calculate_sun_position(
        datetime_str= mean_datetime_str, 
        latitude_dd=latitude_dd, 
        longitude_dd=longitude_dd, 
        timezone_str=timezone_str)
    solar_elevation_class = get_solar_elevation_class(sun_elevation=sun_elevation_angle)
    
    n_records = len(records_dict)
    
    if has_snow_presence:
        QFLAG = 100
    
    elif (n_records < 3) and (solar_elevation_class == 1):
        QFLAG = 211
        
    elif (n_records < 3) and (solar_elevation_class == 2):
        QFLAG = 212
    
    elif (n_records < 3) and (solar_elevation_class == 3):
        QFLAG = 213
    
    elif ((n_records >= 3) and (n_records < 6)) and (solar_elevation_class == 1):
        QFLAG = 221
    
    elif ((n_records >= 3) and (n_records < 6)) and (solar_elevation_class == 2):
        QFLAG = 222
        
    elif ((n_records >= 3) and (n_records < 6)) and (solar_elevation_class == 3):
        QFLAG = 223
        
    elif (n_records >= 6) and (solar_elevation_class == 1):
        QFLAG = 231
    
    elif (n_records >= 6) and (solar_elevation_class == 2):
        QFLAG = 232     
    
    elif (n_records >= 6) and (solar_elevation_class == 3):
        QFLAG = 233 
    
    return QFLAG