import os
import cv2
import numpy as np
import duckdb
import glob
from shapely.geometry import Polygon
from sklearn.linear_model import LogisticRegression
import pickle
from datetime import datetime
from PIL import Image
import re
import piexif
from PIL.ExifTags import TAGS

class SnowDetectionAgent:
    """
    SnowDetectionAgent is responsible for analyzing images to determine the presence of snow.
    The analysis is conducted both at the overall image level and within specific regions of interest (ROIs).
    It stores results in a DuckDB database to avoid redundant processing and supports flagging false positives for learning purposes.
    Additionally, the agent can use machine learning to adjust snow detection parameters based on feedback.
    
    Attributes:
        db_path (str): Path to the DuckDB database file where results are stored.
        connection (duckdb.Connection): DuckDB connection to handle database operations.
        model (LogisticRegression): Machine learning model used to fine-tune snow detection.
        
	Usage:
		```
  		# ROI polygons defined as list of points [(x1, y1), (x2, y2), ...]
		roi_polygons = [
			[(100, 100), (150, 100), (150, 150), (100, 150)],
			[(200, 200), (250, 200), (250, 250), (200, 250)]
		]

		agent = SnowDetectionAgent()
		agent.analyze_directory('path/to/images', roi_polygons, extension_coordinates=(50, 50, 200, 200))

		# Example: Flagging false positives
		agent.flag_false_positive('path/to/images/image1.jpg')

		# Example: Adjusting parameters based on false positives
		agent.adjust_parameters_based_on_feedback()
		```
    """

    def __init__(self, db_path='snow_analysis.duckdb', model_path='snow_model.pkl'):
        """
        Initializes the SnowDetectionAgent with a specified database path.
        Connects to DuckDB and creates the snow_analysis table if it does not exist.
        Loads or initializes the machine learning model for adjusting snow detection parameters.

        Args:
            db_path (str): The path to the DuckDB database file. Defaults to 'snow_analysis.duckdb'.
            model_path (str): The path to the machine learning model file. Defaults to 'snow_model.pkl'.
        """
        # Connect to DuckDB and set up the table for results if it does not exist
        self.connection = duckdb.connect(db_path)
        self.connection.execute('''CREATE TABLE IF NOT EXISTS snow_analysis (
            filepath VARCHAR PRIMARY KEY,
            creation_date TIMESTAMP,
            has_snow_presence BOOLEAN,
            regions JSONB,
            false_positive BOOLEAN DEFAULT FALSE
        );''')

        self.model_path = model_path
        # Load the model if it exists, otherwise initialize a new one
        if os.path.exists(model_path):
            with open(model_path, 'rb') as model_file:
                self.model = pickle.load(model_file)
        else:
            self.model = LogisticRegression()
            self.train_initial_model()

    def extract_creation_date(self, filepath: str) -> dict:
        """
        Extract the creation date of an image from its EXIF data or filename.

        The function attempts to retrieve the creation date of an image in the following order:
        1. Extracts EXIF data from the image file to get the 'DateTimeOriginal' tag.
        2. If EXIF data is not available or does not contain 'DateTimeOriginal', it attempts to parse the filename.
           The filename is expected to contain a date in one of several specific formats.

        Args:
            filepath (str): The file path to the image whose creation date needs to be extracted.

        Returns:
            dict or None: A dictionary containing the following keys if a creation date is found:
                - 'year': The year of the creation date.
                - 'day_of_year': The day of the year (1-366).
                - 'creation_date': The creation date formatted as 'YYYY-MM-DDTHH:MM'.
                - 'extension_coordinates': A list of pixel coordinates representing the image extension.
            Returns None if no creation date can be determined.

        Example:
            filepath = "example_2023-04-15T1402.jpg"
            creation_date = extract_creation_date(filepath)
            if creation_date:
                print(f"Creation Date: {creation_date}")
            else:
                print("Creation Date not found")
        """
        creation_date = None
        extension_coordinates = []
        try:
            # Open image and extract EXIF data
            image = Image.open(filepath)
            exif_data = image._getexif()
            width, height = image.size
            extension_coordinates = [[0, 0], [width, 0], [width, height], [0, height]]
            if exif_data is not None:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == 'DateTimeOriginal':
                        # Extract creation date from EXIF data
                        creation_date = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                        return {
                            'year': creation_date.year,
                            'day_of_year': creation_date.timetuple().tm_yday,
                            'creation_date': creation_date.strftime('%Y-%m-%dT%H:%M'),
                            'extension_coordinates': extension_coordinates
                        }
        except (AttributeError, IOError, ValueError) as e:
            print(f"Error reading EXIF data: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        # If EXIF data is unavailable, attempt to parse filename
        filename = os.path.basename(filepath)
        patterns = [
            r'(\d{4}-\d{2}-\d{2})T(\d{4})\.jpg$',                # Pattern: <text_and_numbers>YYYY-MM-DDTHHMM.jpg
            r'_(\d{4}-\d{2}-\d{2})_(\d{4})\.jpg$',                # Pattern: <alfanumerical>_YYYY-MM-DD_HHMM.jpg
            r'_(\d{6})(\d{4})\.jpg$',                               # Pattern: <alfanumerical-prefix>_YYMMDDHHMM.jpg
            r'_(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2}):(\d{2})_.*\.jpg$'  # Pattern: <alfa_numerical-prefix>_YYYY-MM-DDTHH:MM:SS_<text>.jpg
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                try:
                    if len(match.groups()) == 2:
                        # Handle patterns with date and time parts separately
                        date_str, time_str = match.groups()
                        if '-' in date_str:
                            creation_date = datetime.strptime(date_str + time_str, '%Y-%m-%d%H%M')
                        else:
                            creation_date = datetime.strptime(date_str + time_str, '%y%m%d%H%M')
                    elif len(match.groups()) == 4:
                        # Handle pattern with full timestamp including hours, minutes, and seconds
                        date_str, hour, minute, second = match.groups()
                        creation_date = datetime.strptime(f"{date_str} {hour}:{minute}:{second}", '%Y-%m-%d %H:%M:%S')
                    return {
                        'year': creation_date.year,
                        'day_of_year': creation_date.timetuple().tm_yday,
                        'creation_date': creation_date.strftime('%Y-%m-%dT%H:%M'),
                        'extension_coordinates': extension_coordinates
                    }
                except ValueError as ve:
                    print(f"Error parsing filename for date: {ve}")
                    continue
        
        # Return None if no creation date is found
        return None

    def list_image_files(self, dirpath: str, extensions: list = ['.jpg', '.jpeg']):
        """
        Lists all image files in a directory and its subdirectories with specified extensions.

        Parameters:
            dirpath (str): The root directory to search for image files.
            extensions (list): A list of file extensions to include in the search. Defaults to ['.jpg', '.JPEG', '.jpeg', '.JPG'].

        Returns:
            list: A list of file paths that match the specified extensions.
        """
        file_paths = []
        for root, _, files in os.walk(dirpath):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    file_paths.append(os.path.join(root, file))
        return file_paths

    def is_snow_present(self, image, extension_coordinates=None):
        """
        Determine if snow is present in the entire image by using a simple HSV color threshold.
        Uses a machine learning model to adjust parameters based on prior feedback.
        If extension_coordinates are provided, analyze snow presence only within that area.
        
        Args:
            image (ndarray): The input image in BGR format.
            extension_coordinates (tuple): Optional. Coordinates to specify a sub-region (x, y, w, h).

        Returns:
            tuple: A boolean indicating if snow is present (more than 5% of pixels), and the mask used for detection.
        """
        if extension_coordinates:
            x, y, w, h = extension_coordinates
            image = image[y:y+h, x:x+w]

        # Convert image to HSV to detect white snow regions
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 200], dtype=np.uint8)  # Rough estimate of snow in HSV
        upper_white = np.array([180, 40, 255], dtype=np.uint8)

        # Apply machine learning model to adjust thresholds if necessary
        features = [lower_white[2], upper_white[1], upper_white[2]]
        prediction = self.model.predict([features])[0]
        if prediction == 1:
            upper_white[1] = min(upper_white[1] + 20, 255)
            upper_white[2] = min(upper_white[2] + 20, 255)
        
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

    def analyze_image(self, filepath, roi_polygons, extension_coordinates=None):
        """
        Analyze an image for snow presence both overall and within specified ROIs.
        Saves the analysis results in the database.

        Args:
            filepath (str): Path to the image file.
            roi_polygons (list): List of ROIs, each defined by a list of points [(x1, y1), (x2, y2), ...].
            extension_coordinates (tuple): Optional. Coordinates to specify a sub-region (x, y, w, h) to analyze for overall snow presence.

        Returns:
            dict: Record containing filepath, has_snow_presence, regions, and false_positive status.
            
            
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

        # Extract the creation date
        creation_date_info = self.extract_creation_date(filepath)
        if creation_date_info is None:
            print(f"Could not extract creation date for {filepath}")
            return None

        creation_date = creation_date_info['creation_date']
        extension_coordinates = creation_date_info['extension_coordinates']

        # Analyze the whole image or specific extension for snow
        has_snow_presence, mask = self.is_snow_present(image, extension_coordinates)
        region_results = {}

        # Analyze each ROI for snow
        for i, roi_polygon in enumerate(roi_polygons, start=1):
            region_key = f"ROI_{i:02}_has_snow_presence"
            region_results[region_key] = self.is_snow_present_in_roi(mask, roi_polygon)

        # Prepare record for saving
        record = {
            'filepath': filepath,
            'creation_date': creation_date,
            'has_snow_presence': has_snow_presence,
            'regions': region_results,
            'false_positive': False
        }

        # Save the record to the database
        self.connection.execute(
            "INSERT INTO snow_analysis (filepath, creation_date, has_snow_presence, regions, false_positive) VALUES (?, ?, ?, ?, ?)",
            (record['filepath'], record['creation_date'], record['has_snow_presence'], region_results, record['false_positive'])
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
        Adjust the snow detection parameters based on flagged false positives using machine learning.
        Retrieves false positives from the database and uses them to retrain the model for improved accuracy.
        """
        # Retrieve false positive records
        false_positives = self.connection.execute("SELECT * FROM snow_analysis WHERE false_positive = TRUE").fetchall()
        if not false_positives:
            print("No false positives to adjust parameters for.")
            return

        # Prepare training data based on false positives
        X = []
        y = []
        for record in false_positives:
            # Extract features from flagged records (e.g., HSV threshold values used)
            X.append([0, 40, 255])  # Placeholder values representing the thresholds used for detection
            y.append(0)  # Label as false positive

        # Add some positive examples for balance
        positive_examples = self.connection.execute("SELECT * FROM snow_analysis WHERE false_positive = FALSE LIMIT 10").fetchall()
        for record in positive_examples:
            X.append([0, 40, 255])  # Placeholder values representing thresholds used for detection
            y.append(1)  # Label as true positive

        # Train the model
        if len(X) > 1:  # Ensure there's enough data to train
            self.model.fit(X, y)
            # Save the model to disk
            with open(self.model_path, 'wb') as model_file:
                pickle.dump(self.model, model_file)
            print("Model parameters adjusted based on feedback.")
        else:
            print("Not enough data to retrain the model.")

    def train_initial_model(self):
        """
        Train an initial model with basic parameters.
        """
        X = [[0, 40, 255]]  # Initial threshold features
        y = [1]  # Assume initial values are acceptable (true positive)
        self.model.fit(X, y)
        # Save the model to disk
        with open(self.model_path, 'wb') as model_file:
            pickle.dump(self.model, model_file)

    def analyze_directory(self, directory, roi_polygons, extension_coordinates=None):
        """
        Analyze all images in a specified directory for snow presence.
        Outputs a summary of the number of images with snow detected.

        Args:
            directory (str): Path to the directory containing image files.
            roi_polygons (list): List of ROIs, each defined by a list of points [(x1, y1), (x2, y2), ...].
            extension_coordinates (tuple): Optional. Coordinates to specify a sub-region (x, y, w, h) to analyze for overall snow presence.
        """
        files = self.list_image_files(directory)
        records = []
        for file in files:
            record = self.analyze_image(file, roi_polygons, extension_coordinates)
            if record:
                records.append(record)

        # Present summary
        snow_count = sum(1 for record in records if record['has_snow_presence'] or any(record['regions'].values()))
        total_images = len(records)
        print(f"Summary: {snow_count} out of {total_images} images have more than 5% snow presence.")


