import pyarrow.parquet as pq
import pyarrow as pa
import os

patient_seq_path = "omop_synthea/patient_sequence"
files = [f for f in os.listdir(patient_seq_path) if f.endswith('.parquet')]


def clean_tokens(tokens):
    """Remove malformed inpatient tokens (negative day values)"""
    return [t for t in tokens if not str(t).startswith('i-D-')]


total_removed = 0
for f in files:
    table = pq.read_table(f"{patient_seq_path}/{f}")
    concept_ids = table.column('concept_ids').to_pylist()

    cleaned_ids = []
    for tokens in concept_ids:
        original = len([t for t in tokens if str(t).startswith('i-D-')])
        total_removed += original
        cleaned_ids.append(clean_tokens(tokens))

    new_data = {col: (cleaned_ids if col == 'concept_ids'
                      else table.column(col).to_pylist())
                for col in table.column_names}
    pq.write_table(pa.Table.from_pydict(new_data), f"{patient_seq_path}/{f}")

print(f"Removed {total_removed} malformed tokens")
