import os
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
import cv2
from PIL import Image


def compute_RGB_daily_average(records_list: List[Dict[str, Any]], products_dirpath: str, datatype_acronym: str = 'RGB', product_processing_level: str = 'L2_daily') -> Path:
    """
    Computes daily average RGB images from a list of records and saves them as .jpg files.

    Args:
    records_list (List[Dict[str, Any]]): List of dictionaries where each dictionary contains metadata and the image path.
    products_dirpath (str): Path to the directory where the processed images will be saved.
    datatype_acronym (str, optional): Acronym for the data type, default is 'RGB'.
    product_processing_level (str, optional): Processing level for the product, default is 'L2_daily'.

    Returns:
    Path: Path to the directory where the daily averaged images are saved.
    """
    images = []
    daily_image_catalog_guids = []

    for record in records_list:
        try:
            catalog_guid = record['catalog_guid']
            year = record['year']
            day_of_year = record['day_of_year']
            station_acronym = record['station_acronym']
            location_id = record['location_id']
            platform_id = record['platform_id']
            catalog_filepath = record['catalog_filepath']

            output_dirpath = Path(products_dirpath) / datatype_acronym / str(year)

            if not os.path.exists(output_dirpath):
                os.makedirs(output_dirpath)

            img = cv2.imread(catalog_filepath)
            if img is not None:
                images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                daily_image_catalog_guids.append(catalog_guid)
            else:
                print(f"Warning: Unable to read image at {catalog_filepath}")
        except KeyError as e:
            print(f"Error: Missing key {e} in record {record}")
        except Exception as e:
            print(f"Unexpected error processing record {record}: {e}")

    if images:
        try:
            # Compute element-wise daily average
            avgImg = np.mean(images, axis=0)
            
            # Converting float64 type ndarray to uint8
            intImage = np.around(avgImg).astype(np.uint8)  # Round first and then convert to integer
            
            # Saving the daily average as image
            im = Image.fromarray(intImage)
            
            product_name = f'SITES-{station_acronym}-{location_id}-{platform_id}-{datatype_acronym}-{year}-DOY_{day_of_year}_{product_processing_level}.JPG'
            output_filepath = output_dirpath / product_name

            # Save image in the defined path
            im.save(output_filepath)
            print(f"Saved daily averaged image to {output_filepath}")
        except Exception as e:
            print(f"Error during image processing or saving: {e}")
    else:
        print("No images were processed. No output file created.")

    return output_dirpath