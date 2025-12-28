#!/bin/bash
# CEHR-XGPT Environment Setup
# Run with: source setup_env.sh

# Activate conda environment
conda activate cehrgpt

# Project directories
export OMOP_DIR=omop_synthea
export CEHR_GPT_DATA_DIR=omop_synthea
export CEHR_GPT_MODEL_DIR=omop_synthea/cehrgpt
export SYNTHETIC_DATA_OUTPUT_DIR=omop_synthea/cehrgpt/synthetic_data

# PySpark configuration
export SPARK_HOME=$(python -c "import pyspark; print(pyspark.__file__.rsplit('/', 1)[0])")
export PYSPARK_PYTHON=$(python -c "import sys; print(sys.executable)")
export PYSPARK_DRIVER_PYTHON=$(python -c "import sys; print(sys.executable)")
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export PATH=$SPARK_HOME/bin:$PATH

# Spark resources (adjusted for 32GB Mac M2)
export SPARK_WORKER_INSTANCES=1
export SPARK_WORKER_CORES=8
export SPARK_EXECUTOR_CORES=4
export SPARK_DRIVER_MEMORY=16g
export SPARK_EXECUTOR_MEMORY=16g
export SPARK_MASTER=local[8]

echo "✅ CEHR-XGPT environment loaded!"
echo "   OMOP_DIR: $OMOP_DIR"
echo "   SPARK_HOME: $SPARK_HOME"