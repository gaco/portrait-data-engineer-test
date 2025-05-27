import pandas as pd
from sqlalchemy import create_engine
import os

# Database connection
engine = create_engine('postgresql://postgres:postgres@localhost:5432/healthcare')

# Directory containing CSV files
data_dir = 'source_simulator/sample_datasets'

# List of tables and their corresponding CSV files
tables = {
    'patients': 'patients.csv',
    'appointments': 'appointments.csv',
    'providers': 'providers.csv',
    'prescriptions': 'prescriptions.csv'
}

def load_data():
    """Load all CSV files into PostgreSQL tables."""
    for table_name, csv_file in tables.items():
        print(f"Loading {table_name}...")
        file_path = os.path.join(data_dir, csv_file)
        
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Load into PostgreSQL
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Successfully loaded {table_name}")

if __name__ == "__main__":
    load_data()
    print("Data loading complete!") 