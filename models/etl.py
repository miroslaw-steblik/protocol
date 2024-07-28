import pandas as pd
import numpy as np
from sqlalchemy import create_engine

class AdvancedDataEngineer:
    def __init__(self, source, source_type='csv'):
        """
        Initialize the data engineer object with the data source.
        :param source: The path to the data file or a database connection string.
        :param source_type: The type of the source ('csv', 'json', 'sql').
        """
        self.source = source
        self.source_type = source_type
        self.data = None

    def load_data(self):
        """
        Load data from the specified source based on the source type.
        """
        if self.source_type == 'csv':
            self.data = pd.read_csv(self.source)
        elif self.source_type == 'json':
            self.data = pd.read_json(self.source)
        elif self.source_type == 'sql':
            engine = create_engine(self.source)
            self.data = pd.read_sql_query('SELECT * FROM my_table', engine)
        else:
            raise ValueError("Unsupported source type provided.")

    def clean_data(self, drop_columns=None, fill_missing=None):
        """
        Clean the loaded data.
        :param drop_columns: A list of columns to drop.
        :param fill_missing: A dictionary mapping columns to values with which to fill missing values.
        """
        if drop_columns:
            self.data.drop(columns=drop_columns, inplace=True)
        if fill_missing:
            for column, value in fill_missing.items():
                self.data[column].fillna(value, inplace=True)

    def transform_data(self, transformations):
        """
        Apply transformations to the data.
        :param transformations: A dictionary mapping columns to functions that will transform the column's data.
        """
        for column, func in transformations.items():
            self.data[column] = self.data[column].apply(func)

    def aggregate_data(self, group_by, aggregations):
        """
        Aggregate the data.
        :param group_by: The column to group by.
        :param aggregations: A dictionary mapping columns to aggregation functions.
        """
        return self.data.groupby(group_by).agg(aggregations)




class Transformations:

    # Define transformation functions
    def convert_to_uppercase(x):
        return x.upper() if isinstance(x, str) else x

    def square_number(x):
        return x ** 2

    def convert_to_datetime(x):
        return pd.to_datetime(x)
    

    
# Define the transformations object
transformations = Transformations()

# Dictionary mapping column names to transformation functions
transformations = {
    'name_column': transformations.convert_to_uppercase,  # Convert all strings in 'name_column' to uppercase
    'number_column': transformations.square_number,       # Square all numbers in 'number_column'
    'date_column':transformations.convert_to_datetime    # Convert string dates in 'date_column' to datetime objects
}

# Dictionary mapping columns to aggregation functions
aggregations = {
    'numeric_column': 'mean',  # Calculate the mean of 'numeric_column'
    'date_column': 'max'       # Find the maximum date in 'date_column'
}

# Test the AdvancedDataEngineer
engineer = AdvancedDataEngineer('data.csv')
engineer.load_data()
engineer.clean_data(drop_columns=['unnecessary_column'], fill_missing={'missing_column': 0})
engineer.transform_data(transformations)
aggregated_data = engineer.aggregate_data('category_column', aggregations)
engineer.visualize_data('numeric_column', chart_type='histogram')
engineer.save_data('transformed_data.csv', format='csv')

print(engineer)

