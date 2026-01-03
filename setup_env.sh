#!/bin/bash
# CEHR-XGPT Environment Setup
# Run with: source setup_env.sh

# Activate conda environment
conda activate cehrgpt

# Project directories
export OMOP_DIR=omop_synthea
export CEHR_GPT_DATA_DIR=omop_synthea
export CEHR_GPT_MODEL_DIR=omop_synthea/cehrgpt_model
export SYNTHETIC_DATA_OUTPUT_DIR=omop_synthea/synthetic_data

# PySpark configuration
export SPARK_HOME=$(python -c "import pyspark; print(pyspark.__file__.rsplit('/', 1)[0])")
export PYSPARK_PYTHON=$(python -c "import sys; print(sys.executable)")
export PYSPARK_DRIVER_PYTHON=$(python -c "import sys; print(sys.executable)")
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export PATH=$SPARK_HOME/bin:$PATH

# Spark resources (adjust for your machine)
export SPARK_DRIVER_MEMORY=16g
export SPARK_EXECUTOR_MEMORY=16g
export SPARK_MASTER=local[8]

# Configure Spark for Synthea's historical dates
# (Synthea can generate birth dates before 1900, which Spark 3.0+ rejects by default)
SPARK_CONF_DIR="$SPARK_HOME/conf"
if [ ! -f "$SPARK_CONF_DIR/spark-defaults.conf" ]; then
    mkdir -p "$SPARK_CONF_DIR"
    cat > "$SPARK_CONF_DIR/spark-defaults.conf" << 'EOF'
spark.sql.legacy.parquet.int96RebaseModeInWrite CORRECTED
spark.sql.legacy.parquet.datetimeRebaseModeInWrite CORRECTED
spark.sql.legacy.parquet.int96RebaseModeInRead CORRECTED
spark.sql.legacy.parquet.datetimeRebaseModeInRead CORRECTED
EOF
    echo "✅ Created Spark datetime config: $SPARK_CONF_DIR/spark-defaults.conf"
fi

echo "✅ CEHR-XGPT environment loaded!"
echo "   OMOP_DIR: $OMOP_DIR"
echo "   SPARK_HOME: $SPARK_HOME"