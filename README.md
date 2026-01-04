# CEHR-XGPT Tutorial

A beginner's attempt to reproduce [CEHR-XGPT](https://arxiv.org/abs/2509.03643), a foundation model for electronic health records developed by researchers at Columbia University.

This repository accompanies my blog post: [Reproducing CEHR-XGPT: A Beginner's Journey into EHR Foundation Models](https://chava.cc/posts/reproducing-cehr-xgpt/)

## About This Project

I've been learning about the OMOP Common Data Model and became interested in generating synthetic patient data from an OMOP 
instance. While searching for approaches, I found CEHR-XGPT—and I think it's a fantastic piece of work. The idea of using 
time tokens to preserve temporal structure in EHR data is elegant, and the fact that a single model can handle feature 
extraction, prediction, and generation is impressive.

This repository documents my attempt to reproduce the paper's pipeline on a small local dataset. My goals are:

- Learn more about the OMOP data model by working with it hands-on
- Understand how temporal information is encoded in EHR foundation models
- Explore synthetic data generation for healthcare applications
- Get practical experience with the challenges of training generative models on clinical data

**This is not an official implementation.** For the authoritative code and pretrained models, 
please refer to the [official CEHR-GPT repository](https://github.com/knatarajan-lab/cehrgpt) maintained by the paper's authors.

## What is CEHR-XGPT?

CEHR-XGPT (pronounced "seer-ex-gpt") is a foundation model developed by Chao Pang and colleagues at Columbia University 
Irving Medical Center. Its key innovation is using **Artificial Time Tokens** to explicitly encode temporal gaps between 
medical events, enabling:

- **Feature representation** for downstream prediction tasks
- **Zero-shot prediction** without task-specific fine-tuning
- **Synthetic data generation** that preserves temporal structure

The paper demonstrates that a single unified model can perform all three tasks effectively—a significant advance over prior 
work that typically specialized in just one capability.

## Repository Structure

```
cehr-xgpt-tutorial/
├── cehrgpt_tutorials/     # Official tutorial scripts (git submodule)
├── omop_synthea/          # OMOP data exports and model outputs (gitignored)
├── export_omop.py         # Export OMOP tables from PostgreSQL to Parquet
├── cleanup_tokens.py      # Fix malformed time tokens in patient sequences
├── inspect_synthetic.py   # Analyze generated synthetic sequences
├── setup_env.sh           # Environment configuration for PySpark
└── README.md
```

## Prerequisites

- Python 3.10
- PostgreSQL database with OMOP CDM data
- ~16GB RAM recommended

## Quick Start

### 1. Clone and setup environment

```bash
git clone --recursive https://github.com/YOUR_USERNAME/cehr-xgpt-tutorial.git
cd cehr-xgpt-tutorial

conda create -n cehrgpt python=3.10 -y
conda activate cehrgpt

pip install cehrgpt --constraint cehrgpt_tutorials/constraints.txt
pip install psycopg2-binary
```

### 2. Export your OMOP data

Edit `export_omop.py` with your database credentials, then:

```bash
python export_omop.py
```

### 3. Generate patient sequences

```bash
source setup_env.sh

sh cehrgpt_tutorials/scripts/create_cehrgpt_pretraining_data.sh \
    --input_folder $OMOP_DIR \
    --output_folder $CEHR_GPT_DATA_DIR \
    --start_date 1985-01-01

python cleanup_tokens.py  # Fix any malformed tokens
```

### 4. Train the model

```bash
pip uninstall tensorflow-metal tensorflow tf-keras -y  # macOS only

python -u -m cehrgpt.runners.hf_cehrgpt_pretrain_runner \
    --model_name_or_path omop_synthea/cehrgpt_model \
    --tokenizer_name_or_path omop_synthea/cehrgpt_model \
    --output_dir omop_synthea/cehrgpt_model \
    --data_folder omop_synthea/patient_sequence \
    --dataset_prepared_path omop_synthea/dataset_cache \
    --do_train true \
    --hidden_size 192 \
    --num_hidden_layers 4 \
    --n_head 4 \
    --max_position_embeddings 512 \
    --num_train_epochs 3
```

### 5. Generate synthetic patients

```bash
python -u -m cehrgpt.generation.generate_batch_hf_gpt_sequence \
    --model_folder $CEHR_GPT_MODEL_DIR \
    --tokenizer_folder $CEHR_GPT_MODEL_DIR \
    --output_folder $SYNTHETIC_DATA_OUTPUT_DIR \
    --num_of_patients 500 \
    --context_window 512 \
    --top_p 0.95 \
    --demographic_data_path $CEHR_GPT_DATA_DIR/patient_sequence

python inspect_synthetic.py  # View results
```

## Acknowledgments

This work is entirely based on the CEHR-XGPT paper and codebase developed by:

> Chao Pang, Jiheum Park, Xinzhuo Jiang, Nishanth Parameshwar Pavinkurve, Krishna S. Kalluri, Shalmali Joshi, Noémie Elhadad, and Karthik Natarajan at Columbia University Irving Medical Center and the OHDSI community.

I'm grateful to the authors for open-sourcing their code and providing detailed tutorials that made this learning exercise possible.

## Resources

- [CEHR-XGPT Paper (arXiv)](https://arxiv.org/abs/2509.03643)
- [Official CEHR-GPT Repository](https://github.com/knatarajan-lab/cehrgpt)
- [OHDSI Forums Tutorial](https://forums.ohdsi.org/t/tutorial-synthetic-omop-data-generation-using-cehr-gpt/24320)
- [OMOP Common Data Model](https://ohdsi.github.io/CommonDataModel/)
