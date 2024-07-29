import importlib
from typing import Optional
from sstc_core.sites.spectral.utils import normalize_string
from pathlib import Path
import duckdb
import hashlib
from typing import Dict, Any, List, Union


class DatabaseError(Exception):
    """Base class for other exceptions"""
    pass

class RecordExistsError(DatabaseError):
    """Raised when the record already exists in the database"""
    pass

class RecordNotFoundError(DatabaseError):
    """Raised when the record is not found in the database"""
    pass



def generate_query_dict() -> Dict[str, Dict[str, Union[str, tuple]]]:
    """
    Generates a dictionary containing SQL query templates and their associated parameters.

    This function provides a centralized way to manage SQL queries and the parameters needed for
    each query. The keys of the dictionary represent the operation type, and each value is a dictionary
    containing the query template and a tuple of parameter names that are used in the query.

    Returns:
        Dict[str, Dict[str, Union[str, tuple]]]: A dictionary where each key is a string representing
        the operation (e.g., 'create_table', 'insert_record') and each value is another dictionary with:
            - 'query': The SQL query template as a string, where placeholders are used for dynamic values.
            - 'params': A tuple containing the names of the parameters expected for the query.
            
    Examples:
    
        ```python
        
        queries_dict = generate_query_dict()
        
        # Creating a table
        def create_table_example(db_manager, table_name: str, schema: str):
            query_info = queries_dict["create_table"]
            query = query_info["query"].format(table_name=table_name, schema=schema)
            db_manager.execute_query(query)

        ## Usage
        db_manager = DuckDBManager("example.db")
        create_table_example(db_manager, "users", "id INTEGER PRIMARY KEY, name TEXT")
        db_manager.close()
        
        # Inserting a record
        def insert_record_example(db_manager, table_name: str, record_dict: Dict[str, Any]):
            columns = ', '.join(record_dict.keys())
            placeholders = ', '.join(['?'] * len(record_dict))
            query_info = queries_dict["insert_record"]
            query = query_info["query"].format(table_name=table_name, columns=columns, placeholders=placeholders)
            db_manager.execute_query(query, tuple(record_dict.values()))

        ## Usage
        db_manager = DuckDBManager("example.db")
        record = {"id": 1, "name": "Alice"}
        insert_record_example(db_manager, "users", record)
        db_manager.close()
        
        # Fetching records
        def fetch_records_example(db_manager, table_name: str, condition: str):
            query_info = queries_dict["fetch_records"]
            query = query_info["query"].format(table_name=table_name, condition=condition)
            return db_manager.execute_query(query)

        ## Usage
        db_manager = DuckDBManager("example.db")
        records = fetch_records_example(db_manager, "users", "id = 1")
        print(records)  # Output: [(1, 'Alice')]
        db_manager.close()

        ``` 
    """
    queries = {
        "record_exists":{
            "query": "SELECT COUNT(*) FROM {table_name} WHERE catalog_guid ={catalog_guid}",
            "params": ("table_name", "catalog_guid"),
            
        }, 
        "create_table": {
            "query": "CREATE TABLE IF NOT EXISTS {table_name} ({schema});",
            "params": ("table_name", "schema"),
        },
        "record_exists": {
            "query": "SELECT 1 FROM {table_name} WHERE record_id = ? LIMIT 1",
            "params": ("table_name", "record_id"),
        },
        "insert_record": {
            "query": "INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
            "params": ("table_name", "record_dict"),
        },
        "insert_multiple_records": {
            "query": "INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
            "params": ("table_name", "records"),
        },
        "update_record": {
            "query": "UPDATE {table_name} SET {set_clause} WHERE {condition}",
            "params": ("table_name", "update_values", "condition"),
        },
        "delete_record": {
            "query": "DELETE FROM {table_name} WHERE {condition}",
            "params": ("table_name", "condition"),
        },
        "fetch_records": {
            "query": "SELECT * FROM {table_name} WHERE {condition}",
            "params": ("table_name", "condition"),
        },
        "fetch_by_year": {
            "query": "SELECT * FROM {table_name} WHERE year = ?",
            "params": ("table_name", "year"),
        },
        "fetch_by_is_selected": {
            "query": "SELECT * FROM {table_name} WHERE is_selected = ?",
            "params": ("table_name", "is_selected"),
        },
        "fetch_by_year_and_is_selected": {
            "query": "SELECT * FROM {table_name} WHERE year = ? AND is_selected = ?",
            "params": ("table_name", "year", "is_selected"),
        },
        "list_tables": {
            "query": "SHOW TABLES",
            "params": (),
        },
        "get_catalog_filepaths": {
            "query": "SELECT creation_date, catalog_filepath FROM {table_name} WHERE year(creation_date) = ?",
            "params": ("table_name", "year"),
        },
        "get_source_filepaths": {
            "query": "SELECT creation_date, source_filepath FROM {table_name} WHERE year(creation_date) = ?",
            "params": ("table_name", "year"),
        },
        "add_day_of_year_column": {
            "query": "ALTER TABLE {table_name} ADD COLUMN day_of_year INTEGER;",
            "params": ("table_name",),
        },
        "filter_by_time_window": {
            "query": "SELECT rowid, creation_date FROM {table_name}",
            "params": ("table_name",),
        },
        "populate_L0_name": {
            "query": "ALTER TABLE {table_name} ADD COLUMN L0_name TEXT;",
            "params": ("table_name",),
        },
        "check_is_L1": {
            "query": "ALTER TABLE {table_name} ADD COLUMN is_L1 BOOLEAN;",
            "params": ("table_name",),
        },
        "get_catalog_filepaths_by_year_and_day": {
            "query": "SELECT creation_date, day_of_year, L0_name, is_L1, location_id, platform_id, station_acronym, catalog_filepath, is_selected FROM {table_name}",
            "params": ("table_name", "year", "is_L1", "is_selected"),
        }
    }
    return queries


def generate_unique_id(creation_date: str, station_acronym: str, location_id: str, platform_id: str) -> str:
    """
    Generates a unique global identifier based on creation_date, station_acronym, location_id, and platform_id.

    Parameters:
        creation_date (str): The creation date of the record.
        station_acronym (str): The station acronym.
        location_id (str): The location ID.
        platform_id (str): The platform ID.

    Returns:
        str: A unique global identifier as a SHA-256 hash string.
    """
    # Concatenate the input values to form a unique string
    unique_string = f"{creation_date}_{station_acronym}_{location_id}_{platform_id}"
    
    # Generate the SHA-256 hash of the unique string
    unique_id = hashlib.sha256(unique_string.encode()).hexdigest()
    
    return unique_id



class DuckDBManager:
    """
    A base class for managing DuckDB database connections and operations.
    """
    def __init__(self, db_filepath: str):
        """
        Initializes the DuckDBManager with the path to the database.

        Parameters:
        db_filepath (str): The file path to the DuckDB database.
        """
        self.db_filepath = db_filepath
        self.connection = None
        self.validate_db_filepath()

    def validate_db_filepath(self):
        """
        Validates the existence of the database file path.

        Raises:
        FileNotFoundError: If the database file does not exist at the specified path.
        """
        if not Path(self.db_filepath).is_file():
            raise FileNotFoundError(f"The database file '{self.db_filepath}' does not exist. "
                                    f"Please provide a valid database file path.")

    def connect(self):
        """
        Establishes a connection to the DuckDB database.

        Raises:
        duckdb.Error: If there is an error connecting to the database.
        """
        try:
            self.connection = duckdb.connect(self.db_filepath)
        except duckdb.Error as e:
            raise duckdb.Error(f"Failed to connect to the DuckDB database: {e}")

    def execute_query(self, query: str, params: tuple = None):
        """
        Executes a SQL query on the DuckDB database.

        Parameters:
        query (str): The SQL query to execute.
        params (tuple, optional): A tuple of parameters to pass to the query.

        Returns:
        list: The result of the query as a list of tuples.

        Raises:
        duckdb.Error: If there is an error executing the query.
        """
        try:
            if self.connection is None:
                self.connect()
            if params:
                return self.connection.execute(query, params).fetchall()
            return self.connection.execute(query).fetchall()
        except duckdb.Error as e:
            raise duckdb.Error(f"Failed to execute query: {query}. Error: {e}")

    def close(self):
        """
        Closes the connection to the DuckDB database.

        This method safely closes the connection if it is open.
        """
        if self.connection:
            try:
                self.connection.close()
            except duckdb.Error as e:
                raise duckdb.Error(f"Failed to close the DuckDB database connection: {e}")
            finally:
                self.connection = None
                
     
def stations_names()->dict:
    """
    Retrieve a dictionary of station names with their respective system names and acronyms.

    Returns:
        dict: A dictionary where each key is a station name and the value is another dictionary
              containing the system name and acronym for the station.

    Example:
        ```python
        stations_names()
        {
            'Abisko': {'normalized_station_name': 'abisko', 'station_acronym': 'ANS'},
            'Asa': {'normalized_station_name': 'asa', 'station_acronym': 'ASA'},
            'Grimsö': {'normalized_station_name': 'grimso', 'station_acronym': 'GRI'},
            'Lonnstorp': {'normalized_station_name': 'lonnstorp', 'station_acronym': 'LON'},
            'Robacksdalen': {'normalized_station_name': 'robacksdalen', 'station_acronym': 'RBD'},
            'Skogaryd': {'normalized_station_name': 'skogaryd', 'station_acronym': 'SKC'},
            'Svartberget': {'normalized_station_name': 'svartberget', 'station_acronym': 'SVB'}
        }
        ```
    """
    return {
        'Abisko': {'normalized_station_name': 'abisko', 'station_acronym': 'ANS'},
        'Asa': {'normalized_station_name': 'asa', 'station_acronym': 'ASA'},
        'Grimsö': {'normalized_station_name': 'grimso', 'station_acronym': 'GRI'},
        'Lonnstorp': {'normalized_station_name': 'lonnstorp', 'station_acronym': 'LON'},
        'Robacksdalen': {'normalized_station_name': 'robacksdalen', 'station_acronym': 'RBD'},
        'Skogaryd': {'normalized_station_name': 'skogaryd', 'station_acronym': 'SKC'},
        'Svartberget': {'normalized_station_name': 'svartberget', 'station_acronym': 'SVB'}
    }



class Station(DuckDBManager):
    def __init__(self, db_dirpath: str, station_name: str):
        """
        Initializes the Station class with the directory path of the database and the station name.

        The database file is named using the normalized station name. If the file does not exist, a new
        database is created.

        Parameters:
            db_dirpath (str): The directory path where the DuckDB database is located.
            station_name (str): The name of the station.
        """
        self.station_name = station_name
        self.normalized_station_name = normalize_string(station_name)
        self.station_module = self._load_station_module()
        self.meta = getattr(self.station_module, 'meta', {})
        self.locations = getattr(self.station_module, 'locations', {})
        self.platforms = getattr(self.station_module, 'platforms', {})
        self.db_dirpath = Path(db_dirpath)
        self.db_filepath = self.db_dirpath / f"{self.normalized_station_name}.duckdb"
        self.sftp_dirpath = f'/{self.normalized_station_name}/data/'
        
        # Ensure the database file is created
        if not self.db_filepath.exists():
            self.create_new_database()
        
        super().__init__(str(self.db_filepath))

    def _load_station_module(self):
        """
        Dynamically loads the specified station submodule.

        Returns:
            module: The loaded module.
        """
        module_path = f"sstc_core.sites.spectral.stations.{self.normalized_station_name}"
        try:
            return importlib.import_module(module_path)
        except ModuleNotFoundError:
            raise ImportError(f"Module '{module_path}' could not be found or imported.")

    def create_new_database(self):
        """
        Creates a new DuckDB database file at the specified db_filepath.
        """
        # This will create a new file if it doesn't exist
        connection = duckdb.connect(str(self.db_filepath))
        connection.close()

    def get_station_data(self, query: str, params: Optional[tuple] = None):
        """
        Retrieves data from the station database based on a SQL query.

        Parameters:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to pass with the query.

        Returns:
            Any: The result of the query execution.
        """
        return self.execute_query(query, params)

    def add_station_data(self, table_name: str, data: Dict[str, Any]):
        """
        Adds data to the specified table in the station database. Creates the table if it does not exist.

        Parameters:
            table_name (str): The name of the table to insert data into.
            data (Dict[str, Any]): The data to insert as a dictionary.
        """
        if not self.table_exists(table_name):
            self.create_table(table_name, data)
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(data.values()))

    def table_exists(self, table_name: str) -> bool:
        """
        Checks if a table exists in the station database.

        Parameters:
            table_name (str): The name of the table to check.

        Returns:
            bool: True if the table exists, False otherwise.
        """
        query = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = ?"
        result = self.execute_query(query, (table_name,))
        return result[0][0] > 0

    def create_table(self, table_name: str, data: Dict[str, Any]):
        """
        Creates a new table in the station database with the schema based on the provided data.

        Parameters:
            table_name (str): The name of the table to create.
            data (Dict[str, Any]): A sample data dictionary to infer column types.
        """
        columns = []
        for column_name, value in data.items():
            column_type = self.infer_type(value)
            columns.append(f"{column_name} {column_type}")
        columns_def = ', '.join(columns)
        query = f"CREATE TABLE {table_name} ({columns_def})"
        self.execute_query(query)

    @staticmethod
    def infer_type(value: Any) -> str:
        """
        Infers the DuckDB column type from a Python value.

        Parameters:
            value (Any): The value to infer the type from.

        Returns:
            str: The DuckDB column type.
        """
        if isinstance(value, int):
            return 'INTEGER'
        elif isinstance(value, float):
            return 'DOUBLE'
        elif isinstance(value, str):
            return 'VARCHAR'
        elif isinstance(value, bool):
            return 'BOOLEAN'
        else:
            return 'VARCHAR'  # Fallback type

    def list_tables(self) -> List[str]:
        """
        Lists all tables in the station database.

        Returns:
            List[str]: A list of table names.
        """
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
        result = self.execute_query(query)
        return [row[0] for row in result]

    def close_connection(self):
        """
        Closes the connection to the station database.
        """
        self.close()
        
    def get_metadata(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns the metadata of the station.

        Returns:
            dict: A dictionary with the station name as the key and a nested dictionary containing
                  db_filepath, meta, locations, and platforms as the value.
        """
        return {
            self.station_name: {
                "sftp_dirpath": str(self.sftp_dirpath),
                "db_filepath": str(self.db_filepath),
                "meta": self.meta,
                "locations": self.locations,
                "platforms": self.platforms
            }
        }
    
    def call_load_configurations(self) -> Any:
        """
        Calls `load_configurations` from the station submodule, if available.

        Returns:
            tuple: A tuple containing locations and platforms configuration data or None if the method does not exist.
        """
        load_configurations_method = getattr(self.station_module, 'load_configurations', None)
        if callable(load_configurations_method):
            return load_configurations_method()
        return None
    
    def catalog_guid_exists(self, table_name: str, catalog_guid: str) -> bool:
        """
        Checks if a record with the specified catalog_guid exists in the given table.

        Parameters:
            table_name (str): The name of the table to check.
            catalog_guid (str): The unique identifier to search for.

        Returns:
            bool: True if the record exists, False otherwise.
        """
        query = f"SELECT COUNT(*) FROM {table_name} WHERE catalog_guid = ?"
        result = self.execute_query(query, (catalog_guid,))
        return result[0][0] > 0
    
    def insert_record(self, table_name: str, record_dict: Dict[str, Any]) -> bool:
        """
        Inserts a record into the specified table if the catalog_guid does not already exist.

        Parameters:
            table_name (str): The name of the table to insert the record into.
            record_dict (Dict[str, Any]): A dictionary representing the record to insert.

        Returns:
            bool: True if the record was inserted, False if it already existed.
        """
        catalog_guid = record_dict['catalog_guid']

        # Check if the catalog_guid already exists
        if self.catalog_guid_exists(table_name, catalog_guid):
            print(f"Record with catalog_guid {catalog_guid} already exists.")
            return False

        # Insert the record as it does not exist
        columns = ', '.join(record_dict.keys())
        placeholders = ', '.join(['?'] * len(record_dict))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        try:
            self.execute_query(query, tuple(record_dict.values()))
            print(f"Inserted record with catalog_guid {catalog_guid}")
            return True
        except duckdb.Error as e:
            print(f"Error inserting record: {e}")
            return False
        
    def get_record_count(self, table_name: str) -> int:
        """
        Returns the number of records in the specified table.

        Parameters:
            table_name (str): The name of the table to count records in.

        Returns:
            int: The number of records in the table.
        """
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = self.execute_query(query)
        return result[0][0]
    
    def get_L1_records(self, table_name: str) -> Dict[int, Dict[str, Dict[str, Any]]]:
        """
        Returns all records where `is_L1` is True, structured in a nested dictionary format.

        The dictionary structure is as follows:
        {
            year: {
                L0_name: {
                    'catalog_filepath': catalog_filepath,
                    'day_of_year': day_of_year
                },
                ...
            },
            ...
        }

        Parameters:
            table_name (str): The name of the table to query.

        Returns:
            dict: A nested dictionary with the year as the first key, `L0_name` as the second key, and 
                  `catalog_filepath` and `day_of_year` as the values.
        """
        query = f"SELECT year, L0_name, catalog_filepath, day_of_year FROM {table_name} WHERE is_L1 = TRUE"
        result = self.execute_query(query)
        
        records_by_year_and_L0_name = {}
        for row in result:
            year = row[0]
            L0_name = row[1]
            catalog_filepath = row[2]
            day_of_year = row[3]

            if year not in records_by_year_and_L0_name:
                records_by_year_and_L0_name[year] = {}
            
            records_by_year_and_L0_name[year][L0_name] = {
                'catalog_filepath': catalog_filepath,
                'day_of_year': day_of_year
            }

        return records_by_year_and_L0_name