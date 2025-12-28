import pandas as pd
from sqlalchemy import create_engine
import os

DB_HOST = "local2.chava.cc"
DB_PORT = "5432"
DB_NAME = "ohdsi"
DB_USER = "ohdsi_admin"
DB_PASSWORD = "ohdsi"
DB_SCHEMA = "cdm"

# Create connection
connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_string)

# Output directory
output_dir = "omop_synthea"
os.makedirs(output_dir, exist_ok=True)

# Tables to export - FIXED: added missing commas and condition_occurrence
tables = [
    "person",
    "visit_occurrence",
    "condition_occurrence",
    "drug_exposure",
    "procedure_occurrence",
    "concept",
    "concept_ancestor",
    "concept_relationship"
]

# Export each table
for table in tables:
    print(f"Exporting {DB_SCHEMA}.{table}...")
    query = f"SELECT * FROM {DB_SCHEMA}.{table}"
    try:
        df = pd.read_sql(query, engine)
        output_path = os.path.join(output_dir, f"{table}.parquet")
        df.to_parquet(output_path, index=False)
        print(f"   Saved {len(df):,} rows to {output_path}")
    except Exception as e:
        print(f"   Error exporting {table}: {e}")

print("\n Export complete!")
print(f"\nFiles saved to: {os.path.abspath(output_dir)}")