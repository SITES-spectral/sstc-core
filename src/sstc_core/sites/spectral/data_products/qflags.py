from sstc_core.sites.spectral import utils


def compute_qflag(
    latitude_dd: float,
    longitude_dd: float, 
    records_dict: dict,    
    timezone_str: str = 'Europe/Stockholm',
    is_per_image: bool = False, 
    default_temporal_resolution: bool = True,  # default temporal resolution is 30 min, else 1 hr or more
    ) -> int:
    """
    new processing version v2.0
    `is_per_image` if True the len of records_dict will not be considered on the qflag.
    """
    
    datetime_list = [v['creation_date'] for _, v in records_dict.items()]
    
    mean_datetime_str = utils.mean_datetime_str(datetime_list=datetime_list)
    sun_position = utils.calculate_sun_position(
        datetime_str=mean_datetime_str, 
        latitude_dd=latitude_dd, 
        longitude_dd=longitude_dd, 
        timezone_str=timezone_str
    )
    
    sun_elevation_angle = sun_position['sun_elevation_angle']
    solar_elevation_class = utils.get_solar_elevation_class(sun_elevation=sun_elevation_angle)
   
    n_records = len(records_dict)
        
    if (n_records < 3 if default_temporal_resolution else 2) and (solar_elevation_class == 1):
        QFLAG = 11
        if not is_per_image:
            weight: 0.1
        else:
            weight: 0.5
        
    elif (n_records < 3 if default_temporal_resolution else 2) and (solar_elevation_class == 2):
        QFLAG = 12
        if not is_per_image:
            weight: 0.5
        else:
            weight: 0.75
            
    elif (n_records < 3 if default_temporal_resolution else 2) and (solar_elevation_class == 3):
        QFLAG = 13
        if not is_per_image:
            weight: 0.5
        else:
            weight: 1
            
    elif ((n_records >= 3 if default_temporal_resolution else 2) and (n_records < 6 if default_temporal_resolution else 4 )) and (solar_elevation_class == 1):
        QFLAG = 21
        weight: 0.5
        
    
    elif ((n_records >= 3 if default_temporal_resolution else 2) and (n_records < 6 if default_temporal_resolution else 4)) and (solar_elevation_class == 2):
        QFLAG = 22
        weight: 0.75
  
                
    elif ((n_records >= 3 if default_temporal_resolution else 2) and (n_records < 6 if default_temporal_resolution else 4)) and (solar_elevation_class == 3):
        QFLAG = 23
        weight: 1
  
    elif (n_records >= 6 if default_temporal_resolution else 4) and (solar_elevation_class == 1):
        QFLAG = 31
        weight: 0.75
        
    
    elif (n_records >= 6 if default_temporal_resolution else 4) and (solar_elevation_class == 2):
        QFLAG = 32
        weight: 1.0
        
    elif (n_records >= 6 if default_temporal_resolution else 4) and (solar_elevation_class == 3):
        QFLAG = 33
        weight: 1
        
    
    return {'QFLAG':QFLAG, 'weight': weight}
    

        
        