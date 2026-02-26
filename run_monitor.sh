#!/bin/bash
# ============================================
# dbt Pipeline Monitor - Daily Run Script
# Runs every morning via cron at 8am
# ============================================

# Load your Groq API key
export GROQ_API_KEY="your_groq_api_key_here"

# Navigate to the dbt project directory
cd /home/aasav/dbt_monitor/pipeline_monitor

echo "=============================="
echo "Starting Pipeline Monitor Run"
echo "$(date)"
echo "=============================="

# Step 1: Load seed data into DuckDB
echo "Loading seed data..."
~/.local/bin/dbt seed

# Step 2: Run dbt models (build the tables)
echo "Running dbt models..."
~/.local/bin/dbt run

# Step 3: Run data quality tests
echo "Running data quality tests..."
~/.local/bin/dbt test

# Step 4: Run the Python monitor to parse results and generate AI alert
echo "Running AI monitor..."
python3 monitor.py

echo "=============================="
echo "Monitor run complete"
echo "=============================="
