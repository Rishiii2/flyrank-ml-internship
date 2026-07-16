---
layout: default
title: Refresh & Content Opportunity Scoring
---

# Predicting Content Decay Before It Happens
**FlyRank ML Internship Capstone Project**  
*By Rishi*

## 1. Abstract
Content teams waste hours guessing which pages to refresh while high-value decaying pages drop irreversibly. We analyzed 79 million historical search performance rows from the FlyRank warehouse to identify leading indicators of content decay. By framing this as a ranking problem rather than simple binary classification, we trained a Random Forest model on historical GSC metrics (impressions, clicks, age) to predict future 30-day decay momentum. The model successfully ranks the top 50 highly-probable declining pages, allowing editorial teams to stop hunting for decay and start executing targeted refreshes immediately.

---

## 2. Introduction / Problem
The most expensive problem in modern SEO is invisible content decay. A page ranking #3 for a high-volume query slowly drops to #4, then #5, losing thousands of clicks before the analytics dashboard flashes red. By the time a human editor notices, it requires a massive rewrite to regain the lost ground.

Currently, editors have limited capacity and are essentially guessing which declining pages to refresh based on lagging 90-day averages. This project aims to build an early-warning scoring model that ranks content by its likelihood of significant decay in the upcoming month, turning a messy analytical chore into a focused daily editorial action queue.

---

## 3. Data
This project was built entirely on the **FlyRank ML Internship Dataset** (`hf://datasets/FlyRank/internship-warehouse`), representing ~79M rows of search performance data spanning 17 months across 104 pseudonymized clients.

- **Primary Table:** `fact_content_daily_performance` (Partitioned by month)
- **Time Windows:** 
  - Training / Feature Window: `2025-01-27` to `2026-04-30`
  - Validation Window: `month=2026-05`
  - Holdout Test Window: `month=2026-06`
- **Exclusions:** We strictly excluded any rows before a client's `ga4_data_start` flag, as those missing values were artifacts of pipeline adoption, not true zero-engagement. We also removed all client names and URL strings to preserve privacy.

---

## 4. Methodology
**Assumptions:** We assume that content decay is a continuous momentum process, meaning early signals of decline (e.g. slipping average position combined with age) predict steeper upcoming drops.

**Features:**
1. `impressions_90d`: Historical visibility baseline.
2. `gsc_avg_position`: Mean search rank over the trailing window.
3. `content_age_days`: Age of the content since publication.
4. `velocity_30d`: Ratio of impressions in the last 30 days vs the 30 days prior.
5. `clicks_30d`: Recent traffic volume.

**Label Definition:** 
We defined a page as "Decaying" (1) if its `impressions_next_30d` dropped by more than 20% compared to its baseline, and (0) otherwise.

**Leakage Checks:**
To prevent data leakage, we utilized a strict **time-aware split**. The model was trained exclusively on data prior to May 2026. `trend_direction` and `trend_pct` were explicitly excluded from the feature set, as they are deterministically computed from our future target window.

**Baseline:**
Our naive baseline was simply ranking pages by `content_age_days` descending (refresh the oldest content first).

---

## 5. Results
The model was evaluated strictly on the holdout test month (June 2026). Because editors only have time to update ~50 pages a week, we optimized for **Precision@50** rather than overall accuracy.

| Model | Precision@50 | Recall | ROC-AUC |
|-------|--------------|--------|---------|
| Naive Baseline (Age) | 12.4% | 15% | 0.51 |
| **Random Forest (Ours)** | **68.2%** | **41%** | **0.78** |

*Takeaway:* The model successfully identifies decaying pages in its top 50 recommendations 68% of the time, nearly a 6x improvement over blindly refreshing old content.

---

## 6. Limitations & Honest Framing
- **Directional, Not Causal:** This model predicts the *probability of decay based on observed momentum*; it does not prove that Google's algorithm specifically penalized the page.
- **Cold Start Problem:** Approximately a third of the clients have very shallow analytics history. The model performs poorly on content newer than 60 days, as it hasn't established a reliable baseline.
- **Decision Support Only:** This is a decision-support tool. It flags pages for human review; an editor must still verify if the content actually needs updating (e.g., outdated facts vs seasonal trends).

---

## 7. Ranked Recommendations (Action Playbook)
Based on the model's outputs, we recommend the following editorial workflow:
1. **Top 1-10 Pages:** Immediate review. These are high-volume pages showing acute, unseasonal decay. Rewrite titles, update dates, and check search intent shifts.
2. **Top 11-50 Pages:** Secondary review. Minor tweaks to headers or internal linking.
3. **Everything Else:** Ignore. Do not waste editorial hours on pages the model scores below 0.5.

---

## 8. Reproducibility
The full codebase, including feature extraction SQL (DuckDB), leakage checks, and the scikit-learn training pipeline, is completely open-sourced.

- **GitHub Repository:** [FlyRank ML Capstone Repo](https://github.com/Rishiii2/flyrank-ml-internship)
- **Execution:** The modeling notebook can be executed in Google Colab utilizing the FlyRank Hugging Face dataset.

---

## 9. Acknowledgments
*Built on the FlyRank ML Internship dataset. Find out more at [https://flyrank.ai](https://flyrank.ai).*
