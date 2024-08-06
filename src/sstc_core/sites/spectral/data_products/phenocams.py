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

    return output_filepath


def compute_GCC_RCC(daily_rgb_filepath: str, products_dirpath: str, year: int) -> dict:
    """
    Computes GCC and RCC images from a daily average RGB image and saves them as grayscale images.

    Args:
        daily_rgb_filepath (str): File path to the daily average RGB image.
        products_dirpath (str): Path to the directory where the processed images will be saved.
        year (int): Year for which the GCC and RCC images are being processed.

    Returns:
        dict: Dictionary containing file paths to the saved GCC and RCC images.
    """
    try:
        # Define directories to save GCC and RCC images
        gcc_dirpath = Path(products_dirpath) / 'GCC' / str(year)
        rcc_dirpath = Path(products_dirpath) / 'RCC' / str(year)
        
        # Ensure the directories exist
        gcc_dirpath.mkdir(parents=True, exist_ok=True)
        rcc_dirpath.mkdir(parents=True, exist_ok=True)
        
        # Extracting image file name
        imgName = os.path.basename(daily_rgb_filepath)
        
        # Reading the RGB image
        cv_img = cv2.imread(daily_rgb_filepath)
        if cv_img is None:
            raise FileNotFoundError(f"Image file not found or unable to read: {daily_rgb_filepath}")
        
        # Extracting RGB bands as separate numpy arrays
        B = cv_img[:,:,0]
        G = cv_img[:,:,1]
        R = cv_img[:,:,2]

        # Element-wise addition of BGR array to calculate Total DN values in RGB band (i.e. R+G+B)
        DNtotal = cv_img.sum(axis=2)

        # Compute pixel-wise GCC and RCC from daily average images
        gcc = np.divide(G, DNtotal, out=np.zeros_like(G, dtype=float), where=DNtotal!=0)
        rcc = np.divide(R, DNtotal, out=np.zeros_like(R, dtype=float), where=DNtotal!=0)

        # Convert NaN to zero
        gcc = np.nan_to_num(gcc, copy=False)
        rcc = np.nan_to_num(rcc, copy=False)

        # Converting GCC and RCC to smoothly range from 0 - 255 as 'uint8' data type from 'float64'
        intImage1 = (gcc * 255).astype(np.uint8) 
        intImage2 = (rcc * 255).astype(np.uint8)

        # Convert to BGR format for saving
        cv_img_gcc = cv2.cvtColor(intImage1, cv2.COLOR_GRAY2BGR)
        cv_img_rcc = cv2.cvtColor(intImage2, cv2.COLOR_GRAY2BGR)

        # Define paths for saving images with given file names
        gcc_filepath = os.path.join(gcc_dirpath, imgName.replace('RGB', 'GCC'))
        rcc_filepath = os.path.join(rcc_dirpath, imgName.replace('RGB', 'RCC'))

        # Save images in the defined paths
        cv2.imwrite(gcc_filepath, cv_img_gcc)
        cv2.imwrite(rcc_filepath, cv_img_rcc)
        
        return {'gcc_filepath': gcc_filepath, 'rcc_filepath': rcc_filepath}

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except KeyError as e:
        print(f"Error: Missing key {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}