import pyarrow.parquet as pq
import pyarrow as pa
import os

# Find generated sequences
synth_dir = "omop_synthea/synthetic_data"
seq_dirs = [d for d in os.listdir(synth_dir) if d.startswith('top_p')]
if not seq_dirs:
    print("No generated sequences found!")
    exit(1)

seq_path = f"{synth_dir}/{seq_dirs[0]}/generated_sequences"
print(f"Loading from: {seq_path}")

# Load all parquet files
tables = []
for f in os.listdir(seq_path):
    if f.endswith('.parquet'):
        tables.append(pq.read_table(f"{seq_path}/{f}"))

table = pa.concat_tables(tables)
sequences = table.column('concept_ids').to_pylist()

print(f"Total sequences: {len(sequences)}")

# Length statistics
lengths = [len(s) for s in sequences]
print(f"\nSequence lengths:")
print(f"  Min: {min(lengths)}")
print(f"  Max: {max(lengths)}")
print(f"  Mean: {sum(lengths)/len(lengths):.1f}")

# Count visit types
visit_types = {}
for seq in sequences:
    for i, token in enumerate(seq):
        if token == '[VS]' and i + 1 < len(seq):
            vt = seq[i + 1]
            visit_types[vt] = visit_types.get(vt, 0) + 1

print(f"\nVisit type distribution:")
for vt, count in sorted(visit_types.items(), key=lambda x: -x[1])[:5]:
    print(f"  {vt}: {count}")

# Show example
print(f"\n--- Example Sequence (first 50 tokens) ---")
print(sequences[0][:50])
