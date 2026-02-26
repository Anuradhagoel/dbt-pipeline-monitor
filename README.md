# 🚨 dbt Pipeline Monitor

An automated data quality monitor that runs dbt tests every morning and uses AI to explain failures in plain English-before your stakeholders find out.

## What It Does

Every morning at 8am this system automatically:
1. Loads data into DuckDB via dbt seeds
2. Runs dbt models to build the pipeline
3. Runs dbt data quality tests
4. Parses the results with Python
5. Sends failures to Groq AI (LLaMA 3.1) for a plain-English explanation
6. Outputs a clear, actionable alert

**Example output:**
```
✅ Passed: 2 tests
❌ Failed: 2 tests

AI ALERT SUMMARY:
==================================================
"Two data quality checks failed. The orders table 
has missing amount values on 2 rows and a missing 
customer ID on 1 row. Review source data before 
the morning reporting run."
```

## Why I Built This

Silent pipeline failures are one of the most common pain points in data engineering. By the time a stakeholder notices something is wrong, it's already too late. This project automates the detection and explanation of failures so the data team always knows first.

This same pattern is used at scale by companies like Airbnb and Netflix-the difference is they use Airflow instead of cron and PagerDuty instead of terminal output. The core logic is identical.

## Tech Stack

| Tool | Purpose | Cost |
|------|---------|------|
| dbt + DuckDB | Data modeling and quality tests | Free |
| Python | Parse dbt results | Free |
| Groq API + LLaMA 3.1 | Generate plain-English AI alerts | Free |
| Cron | Schedule daily runs | Free (built into Linux) |

**Total cost: $0**

## Project Structure

```
dbt_pipeline_monitor/
├── models/
│   ├── orders_summary.sql    # dbt model joining orders + customers
│   └── schema.yml            # data quality test definitions
├── seeds/
│   ├── orders.csv            # sample orders data (with intentional NULLs)
│   └── customers.csv         # sample customers data
├── monitor.py                # Python monitor script with AI integration
├── run_monitor.sh            # Shell script that orchestrates everything
└── README.md
```

## Setup Instructions

### Prerequisites
- Ubuntu / WSL2 (Windows users)
- Python 3.10+
- Node.js 20+

### Step 1-Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/dbt-pipeline-monitor
cd dbt-pipeline-monitor
```

### Step 2-Install dependencies
```bash
pip3 install dbt-core dbt-duckdb groq --break-system-packages
```

### Step 3-Set up dbt project
```bash
dbt init pipeline_monitor
# Select duckdb when prompted
cd pipeline_monitor
```

### Step 4-Get a free Groq API key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (no credit card needed)
3. Create an API key

### Step 5-Add your API key to run_monitor.sh
```bash
export GROQ_API_KEY="your_key_here"
```

### Step 6-Run manually to test
```bash
dbt seed
dbt run
dbt test
python3 monitor.py
```

### Step 7-Schedule with cron (runs daily at 8am)
```bash
crontab -e
# Add this line:
0 8 * * * bash /path/to/run_monitor.sh >> /path/to/monitor.log 2>&1
```

## How to Scale This

This project is intentionally simple — here's how the same pattern works at enterprise scale:

| This Project | Enterprise Version |
|-------------|-------------------|
| Cron | Apache Airflow / Prefect |
| Terminal output | Slack / PagerDuty alerts |
| DuckDB | Snowflake / BigQuery / Redshift |
| Sample CSVs | Production data warehouse |
| Local machine | Cloud infrastructure |

The core logic (automated testing → AI explanation → alert) is identical at any scale.

## Lessons Learned

- **Monitoring > reacting** -catch failures before stakeholders do
- **Trendy tools aren't always the right tools** -started with OpenClaw, hit WSL2 issues, adapted
- **Start small and ship** -this took a weekend to build and solves a real problem

## Author

Built by [@anuradha](https://www.linkedin.com/in/anuradhagoel/) as a learning project while exploring the modern data engineering stack.


