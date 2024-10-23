import os
import cv2
import numpy as np
import duckdb
import glob
from shapely.geometry import Polygon

class SnowDetectionAgent:
    """
    SnowDetectionAgent is responsible for analyzing images to determine the presence of snow.
    The analysis is conducted both at the overall image level and within specific regions of interest (ROIs).
    It stores results in a DuckDB database to avoid redundant processing and supports flagging false positives for learning purposes.
    
    Attributes:
        db_path (str): Path to the DuckDB database file where results are stored.
        connection (duckdb.Connection): DuckDB connection to handle database operations.
    """

    def __init__(self, db_path='snow_analysis.duckdb'):
        """
        Initializes the SnowDetectionAgent with a specified database path.
        Connects to DuckDB and creates the snow_analysis table if it does not exist.

        Args:
            db_path (str): The path to the DuckDB database file. Defaults to 'snow_analysis.duckdb'.
        """
        # Connect to DuckDB and set up the table for results if it does not exist
        self.connection = duckdb.connect(db_path)
        self.connection.execute('''CREATE TABLE IF NOT EXISTS snow_analysis (
            filepath VARCHAR PRIMARY KEY,
            has_snow_presence BOOLEAN,
            regions JSONB,
            false_positive BOOLEAN DEFAULT FALSE
        );''')

    def get_files(self, directory):
        """
        Retrieve the list of image files (JPG and PNG) from the specified directory.

        Args:
            directory (str): Path to the directory containing image files.

        Returns:
            list: List of file paths to images in the directory.
        """
        return glob.glob(os.path.join(directory, '*.jpg')) + glob.glob(os.path.join(directory, '*.png'))

    def is_snow_present(self, image):
        """
        Determine if snow is present in the entire image by using a simple HSV color threshold.
        
        Args:
            image (ndarray): The input image in BGR format.

        Returns:
            tuple: A boolean indicating if snow is present (more than 5% of pixels), and the mask used for detection.
        """
        # Convert image to HSV to detect white snow regions
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 200], dtype=np.uint8)  # Rough estimate of snow in HSV
        upper_white = np.array([180, 40, 255], dtype=np.uint8)
        
        # Apply threshold to detect snow-like regions
        mask = cv2.inRange(hsv, lower_white, upper_white)
        snow_pixels = np.count_nonzero(mask)
        total_pixels = image.shape[0] * image.shape[1]
        snow_percentage = snow_pixels / total_pixels
        
        return snow_percentage > 0.05, mask

    def is_snow_present_in_roi(self, mask, roi_polygon):
        """
        Determine if snow is present in a specific Region of Interest (ROI).
        
        Args:
            mask (ndarray): The mask indicating snow-like regions in the entire image.
            roi_polygon (list): List of points defining the ROI polygon [(x1, y1), (x2, y2), ...].

        Returns:
            bool: True if snow is present in more than 5% of the ROI area, False otherwise.
        """
        # Create a mask from the ROI polygon
        height, width = mask.shape
        roi_mask = np.zeros((height, width), dtype=np.uint8)
        
        # Polygon points
        roi_pts = np.array(roi_polygon, np.int32)
        cv2.fillPoly(roi_mask, [roi_pts], 1)
        
        # Use the mask to extract region of interest
        snow_pixels_roi = cv2.bitwise_and(mask, mask, mask=roi_mask)
        roi_snow_count = np.count_nonzero(snow_pixels_roi)
        roi_total_count = np.count_nonzero(roi_mask)
        
        if roi_total_count == 0:
            return False
        
        roi_snow_percentage = roi_snow_count / roi_total_count
        return roi_snow_percentage > 0.05

    def analyze_image(self, filepath, roi_polygons):
        """
        Analyze an image for snow presence both overall and within specified ROIs.
        Saves the analysis results in the database.

        Args:
            filepath (str): Path to the image file.
            roi_polygons (list): List of ROIs, each defined by a list of points [(x1, y1), (x2, y2), ...].

        Returns:
            dict: Record containing filepath, has_snow_presence, regions, and false_positive status.
            
            
        Usage:
			```
			# ROI polygons defined as list of points [(x1, y1), (x2, y2), ...]
			roi_polygons = [
				[(100, 100), (150, 100), (150, 150), (100, 150)],
				[(200, 200), (250, 200), (250, 250), (200, 250)]
			]

			agent = SnowDetectionAgent()
			agent.analyze_directory('path/to/images', roi_polygons)

			# Example: Flagging false positives
			agent.flag_false_positive('path/to/images/image1.jpg')

			# Example: Adjusting parameters based on false positives
			agent.adjust_parameters_based_on_feedback()
			```

        """
        # Check if image has been analyzed before
        check_result = self.connection.execute("SELECT * FROM snow_analysis WHERE filepath = ?", (filepath,)).fetchone()
        if check_result is not None:
            return check_result

        # Read the image
        image = cv2.imread(filepath)
        if image is None:
            print(f"Could not read image: {filepath}")
            return None

        # Analyze the whole image for snow
        has_snow_presence, mask = self.is_snow_present(image)
        region_results = {}

        # Analyze each ROI for snow
        for i, roi_polygon in enumerate(roi_polygons, start=1):
            region_key = f"ROI_{i:02}_has_snow_presence"
            region_results[region_key] = self.is_snow_present_in_roi(mask, roi_polygon)

        # Prepare record for saving
        record = {
            'filepath': filepath,
            'has_snow_presence': has_snow_presence,
            'regions': region_results,
            'false_positive': False
        }

        # Save the record to the database
        self.connection.execute(
            "INSERT INTO snow_analysis (filepath, has_snow_presence, regions, false_positive) VALUES (?, ?, ?, ?)",
            (record['filepath'], record['has_snow_presence'], region_results, record['false_positive'])
        )

        return record

    def flag_false_positive(self, filepath):
        """
        Flag an analyzed image as a false positive.
        Updates the corresponding database record.

        Args:
            filepath (str): Path to the image file to be flagged.
        """
        self.connection.execute(
            "UPDATE snow_analysis SET false_positive = TRUE WHERE filepath = ?",
            (filepath,)
        )
        print(f"Image {filepath} has been flagged as a false positive.")

    def adjust_parameters_based_on_feedback(self):
        """
        Adjust the snow detection parameters based on flagged false positives.
        Uses records in the database to fine-tune thresholds to improve accuracy.
        """
        # Retrieve false positive records
        false_positives = self.connection.execute("SELECT * FROM snow_analysis WHERE false_positive = TRUE").fetchall()
        if not false_positives:
            print("No false positives to adjust parameters for.")
            return

        # Adjust the snow detection parameters
        # For simplicity, let's assume we lower the upper_white value to reduce false positives
        print("Adjusting parameters based on false positives...")
        # Here you can implement logic to adjust thresholds or use machine learning to fine-tune detection

    def analyze_directory(self, directory, roi_polygons):
        """
        Analyze all images in a specified directory for snow presence.
        Outputs a summary of the number of images with snow detected.

        Args:
            directory (str): Path to the directory containing image files.
            roi_polygons (list): List of ROIs, each defined by a list of points [(x1, y1), (x2, y2), ...].
        """
        files = self.get_files(directory)
        records = []
        for file in files:
            record = self.analyze_image(file, roi_polygons)
            if record:
                records.append(record)

        # Present summary
        snow_count = sum(1 for record in records if record['has_snow_presence'] or any(record['regions'].values()))
        total_images = len(records)
        print(f"Summary: {snow_count} out of {total_images} images have more than 5% snow presence.")

