import json
import sys
import os

def create_capstone_notebook(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# FlyRank ML Capstone: Content Opportunity Scoring Model\n",
                    "\n",
                    "This notebook trains a predictive model to identify which content is most likely to decay in the upcoming 30 days based on historical Search Console signals."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import sys\n",
                    "\n",
                    "try:\n",
                    "    import duckdb\n",
                    "    from sklearn.ensemble import RandomForestClassifier\n",
                    "    from sklearn.metrics import classification_report, roc_auc_score, precision_score\n",
                    "except ImportError:\n",
                    "    print(\"Dependencies missing. Run: pip install duckdb scikit-learn pandas\")\n",
                    "    sys.exit(0)\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Data Extraction (DuckDB & Hugging Face)"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 2,
                "metadata": {},
                "outputs": [],
                "source": [
                    "con = duckdb.connect()\n",
                    "try:\n",
                    "    from google.colab import userdata\n",
                    "    hf_token = userdata.get('HF_TOKEN')\n",
                    "    con.execute(f\"CREATE OR REPLACE SECRET hf (TYPE huggingface, TOKEN '{hf_token}')\")\n",
                    "except:\n",
                    "    print(\"Warning: No Hugging Face token found. Executing with simulated local data for reproducibility.\")\n",
                    "    # Simulated data if token fails\n",
                    "    np.random.seed(42)\n",
                    "    simulated_data = pd.DataFrame({\n",
                    "        'client_id': np.random.choice(['client_A', 'client_B'], 5000),\n",
                    "        'content_id': range(5000),\n",
                    "        'impressions_90d': np.random.randint(100, 10000, 5000),\n",
                    "        'gsc_avg_position': np.random.uniform(1, 50, 5000),\n",
                    "        'content_age_days': np.random.randint(10, 1000, 5000),\n",
                    "        'velocity_30d': np.random.uniform(0.5, 1.5, 5000),\n",
                    "        'clicks_30d': np.random.randint(0, 1000, 5000),\n",
                    "        'impressions_next_30d': np.random.randint(50, 5000, 5000),\n",
                    "        'month': np.random.choice(['2026-04', '2026-05', '2026-06'], 5000)\n",
                    "    })\n",
                    "    con.register('raw_data', simulated_data)\n",
                    "    REL = \"raw_data\"\n",
                    "\n",
                    "df = con.sql(f\"\"\"\n",
                    "    SELECT *\n",
                    "    FROM {REL}\n",
                    "\"\"\").df()\n",
                    "\n",
                    "print(f\"Extracted {len(df)} rows for modeling.\")\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Feature Engineering & Label Definition"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 3,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Define Label: Is the page decaying? \n",
                    "# (Impressions dropping by more than 20% compared to baseline)\n",
                    "baseline = df['impressions_90d'] / 3 # approximate 30d baseline\n",
                    "df['is_decaying'] = (df['impressions_next_30d'] < (baseline * 0.8)).astype(int)\n",
                    "\n",
                    "features = ['impressions_90d', 'gsc_avg_position', 'content_age_days', 'velocity_30d', 'clicks_30d']\n",
                    "X = df[features]\n",
                    "y = df['is_decaying']\n",
                    "\n",
                    "print(\"Label Distribution:\\n\", y.value_counts(normalize=True))\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Time-Aware Split (Leakage Prevention)"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 4,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Train on April/May, Test on June (Holdout)\n",
                    "train_mask = df['month'].isin(['2026-04', '2026-05'])\n",
                    "test_mask = df['month'] == '2026-06'\n",
                    "\n",
                    "X_train, y_train = X[train_mask], y[train_mask]\n",
                    "X_test, y_test = X[test_mask], y[test_mask]\n",
                    "\n",
                    "print(f\"Training instances: {len(X_train)}\")\n",
                    "print(f\"Testing instances: {len(X_test)}\")\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 4. Modeling & Results (Precision@50)"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 5,
                "metadata": {},
                "outputs": [],
                "source": [
                    "model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)\n",
                    "model.fit(X_train, y_train)\n",
                    "\n",
                    "# Predict probabilities for the holdout set\n",
                    "preds_proba = model.predict_proba(X_test)[:, 1]\n",
                    "\n",
                    "# Rank the top 50 pages most likely to decay\n",
                    "top_50_indices = np.argsort(preds_proba)[-50:][::-1]\n",
                    "top_50_true = y_test.iloc[top_50_indices]\n",
                    "\n",
                    "precision_at_50 = top_50_true.mean()\n",
                    "auc = roc_auc_score(y_test, preds_proba)\n",
                    "\n",
                    "print(f\"Model ROC-AUC Score: {auc:.3f}\")\n",
                    "print(f\"Model Precision@50:  {precision_at_50*100:.1f}%\")\n",
                    "\n",
                    "# Compare to Baseline (Age-based: refresh oldest content)\n",
                    "baseline_top_50_indices = np.argsort(X_test['content_age_days'])[-50:][::-1]\n",
                    "baseline_precision = y_test.iloc[baseline_top_50_indices].mean()\n",
                    "print(f\"Naive Age Baseline Precision@50: {baseline_precision*100:.1f}%\")\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)

if __name__ == "__main__":
    create_capstone_notebook(sys.argv[1])
