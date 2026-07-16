# AI Workflow Audit

## 1. Recurring Tasks Classification

| Task | Classification | Rationale |
| :--- | :--- | :--- |
| **1. Deciding on the core ML research question (framing)** | Just me | The decision of what problem actually matters requires human business context and alignment that AI lacks. |
| **2. Reviewing internship curriculum & goals** | Just me | I need to internalize the expectations and learning objectives myself; AI cannot learn this for me. |
| **3. Writing ML baseline scripts (sklearn, pandas)** | Delegate to AI with review | AI can write standard boilerplate ML code quickly, but I must review the logic and parameters. |
| **4. Data cleaning (handling missing values, formatting)** | Delegate to AI with review | AI efficiently writes imputation scripts, but I must verify the distributions haven't been skewed. |
| **5. Brainstorming feature engineering ideas** | Collaborate with AI | AI suggests novel signals and transformations; I filter them based on my domain knowledge. |
| **6. Connecting to external datasets/APIs** | Fully automate | Standard API connection code is universally the same and safe to generate blindly. |
| **7. Writing final research reports/capstones** | Collaborate with AI | I outline the claims and structure; AI helps with flow, but I must verify every single claim. |
| **8. Drafting update emails to mentors/managers** | Delegate to AI with review | AI can quickly adjust tone and structure, but I need to ensure the factual updates are accurate. |
| **9. Debugging Python stack traces** | Delegate to AI with review | AI is excellent at identifying the root cause of an error message, but I must apply and test the fix. |
| **10. Formatting markdown tables for documentation** | Fully automate | AI can reliably convert lists or CSVs into markdown tables without hallucination or logic errors. |
| **11. Reading complex ML whitepapers/documentation** | Collaborate with AI | I read the core paper, but use AI as an interactive tutor to break down dense mathematical proofs. |
| **12. Structuring GitHub repositories** | Fully automate | AI can generate a standard directory structure and `.gitignore` instantly and flawlessly. |

## 2. Target Tasks for FL-02 through FL-04

**Target Task 1: Writing data cleaning and preprocessing scripts**
* **Success Definition:** The AI generates a Python script that successfully handles missing values and data type conversions without introducing data leakage, passing all basic assertions on the first or second prompt.

**Target Task 2: Debugging complex Python errors**
* **Success Definition:** The AI accurately diagnoses the root cause of a given stack trace and provides a working code solution that resolves the error without breaking other parts of the pipeline, all within 5 minutes of prompting.

**Target Task 3: Brainstorming feature engineering ideas**
* **Success Definition:** The AI suggests at least 3 novel, domain-relevant features that I hadn't initially considered, which can be feasibly calculated from the currently available dataset features.
