# Prompt Ladder: Building an ML Data Extraction Script

## Baseline (V0)
**Prompt:** "Write a python script to find declining pages in a csv."

**Representative Output:** 
```python
import pandas as pd
df = pd.read_csv('data.csv')
declining = df[df['traffic_today'] < df['traffic_yesterday']]
print(declining)
```

**Notes:**
*   **What changed in the prompt:** Nothing (Baseline).
*   **What actually improved in the output:** N/A.
*   **What still failed:** The definition of "declining" is completely arbitrary (the AI just guessed I wanted to compare today vs yesterday), and it invented column names (`traffic_today`) that don't exist in my dataset.
*   **What I would try next:** Add a **clearer goal** specifying exactly what metric defines a decline in our specific warehouse.

---

## Version 1
**Prompt:** "Write a python script to find declining pages in a csv. A page is declining if its 'trend_direction' column is 'down' and 'impressions_90d' > 1000."

**Representative Output:** 
```python
import pandas as pd
df = pd.read_csv('data.csv')
declining = df[(df['trend_direction'] == 'down') & (df['impressions_90d'] > 1000)]
print(declining)
```

**Notes:**
*   **What changed in the prompt:** Added a **Clearer Goal** (explicit business logic).
*   **What actually improved in the output:** The script stopped hallucinating logic and now filters based on the exact columns and thresholds used by my team.
*   **What still failed:** It just prints the entire dataframe to the console, which is completely unreadable for a dataset of 50,000 rows. It doesn't save the results.
*   **What I would try next:** Add a **specified output format**.

---

## Version 2
**Prompt:** "Write a python script to find declining pages in a csv. A page is declining if its 'trend_direction' column is 'down' and 'impressions_90d' > 1000. Output a ranked CSV containing only the 'url', 'impressions_90d', and 'trend_direction' columns, sorted by impressions descending."

**Representative Output:** 
```python
import pandas as pd
df = pd.read_csv('data.csv')
declining = df[(df['trend_direction'] == 'down') & (df['impressions_90d'] > 1000)]
declining = declining[['url', 'impressions_90d', 'trend_direction']]
declining = declining.sort_values(by='impressions_90d', ascending=False)
declining.to_csv('declining_pages.csv', index=False)
```

**Notes:**
*   **What changed in the prompt:** Added a **Specified Output Format**.
*   **What actually improved in the output:** The script now generates a clean, sorted, usable artifact (a CSV) containing only relevant data, rather than dumping unstructured text to the terminal.
*   **What still failed:** The script relies on hardcoded file paths (`data.csv` and `declining_pages.csv`). If I want to run this in a pipeline, I have to manually edit the source code every time.
*   **What I would try next:** Add **real context and constraints** to make it CLI-friendly.

---

## Version 3
**Prompt:** "Write a python script to find declining pages. A page is declining if its 'trend_direction' column is 'down' and 'impressions_90d' > 1000. Output a ranked CSV containing only 'url', 'impressions_90d', and 'trend_direction', sorted by impressions descending. Constraint: The script must accept the input and output file paths as command-line arguments using argparse, and gracefully handle missing 'impressions_90d' values."

**Representative Output:** 
```python
import argparse
import pandas as pd
# ... argparse setup ...
try:
    df = pd.read_csv(args.input)
    df['impressions_90d'] = df['impressions_90d'].fillna(0)
    # ... logic ...
except Exception as e:
    print(f"An error occurred: {e}")
```

**Notes:**
*   **What changed in the prompt:** Added **Real Context and Constraints** (argparse, error handling).
*   **What actually improved in the output:** The script is now dynamic and can be integrated into an automated pipeline without hardcoding.
*   **What still failed *(The "Made it Worse" moment)*:** The AI over-engineered the error handling by wrapping the entire pandas operation in a massive, generic `try-except Exception as e` block. This swallowed the stack traces, meaning when I ran it on a CSV with a misspelled column name, it just said "An error occurred: KeyError" and gave me no line number to debug.
*   **What I would try next:** Add **quality criteria** to force better coding practices.

---

## Version 4
**Prompt:** "Write a python script to find declining pages. A page is declining if 'trend_direction' is 'down' and 'impressions_90d' > 1000. Output a ranked CSV containing only 'url', 'impressions_90d', and 'trend_direction', sorted by impressions descending. Constraint: Accept input/output file paths via argparse, and fill missing 'impressions_90d' with 0. Quality criteria: Do NOT wrap the core logic in a broad try-except block. Fail fast and let pandas raise standard errors. Include PEP-8 type hints."

**Representative Output:** 
```python
import argparse
import pandas as pd

def process_data(input_path: str, output_path: str) -> None:
    df = pd.read_csv(input_path)
    df['impressions_90d'] = df['impressions_90d'].fillna(0)
    # ... logic ...
```

**Notes:**
*   **What changed in the prompt:** Added **Quality Criteria** (fail fast, type hints).
*   **What actually improved in the output:** The code is vastly cleaner. It stopped swallowing critical errors and now looks like it was written by a senior engineer rather than a defensive beginner.
*   **What still failed:** If a non-technical editor or another intern tries to run this, they have no idea what arguments to pass because there is no documentation or examples.
*   **What I would try next:** Add **verification requirements / documentation**.

---

## Version 5
**Prompt:** "Write a python script to find declining pages. A page is declining if 'trend_direction' is 'down' and 'impressions_90d' > 1000. Output a ranked CSV containing only 'url', 'impressions_90d', and 'trend_direction', sorted by impressions descending. Constraint: Accept input/output file paths via argparse, and fill missing 'impressions_90d' with 0. Quality criteria: Fail fast on missing columns, no broad try-except blocks, use PEP-8 type hints. Verification: Ensure argparse provides helpful descriptions, and include a concise module-level docstring showing an exact example bash command to run the script."

**Representative Output:** 
```python
\"\"\"
Extracts declining content opportunities from search logs.
Example usage:
    python extract_declines.py --input raw_data.csv --output targets.csv
\"\"\"
import argparse
import pandas as pd
# ... clean, type-hinted code with argparse help strings ...
```

**Notes:**
*   **What changed in the prompt:** Added **Verification Requirements**.
*   **What actually improved in the output:** The script is now a complete, self-documenting tool. A colleague can read the top of the file and instantly know how to execute it without needing to decipher the `argparse` logic.
*   **What still failed:** Nothing major. It is highly robust and ready to ship.
*   **What I would try next:** Ready for production use.

---

## Final Reusable Prompt
*Cleaned up so anyone on the track can use it for their own data extractions.*

> Write a Python script to filter and rank a dataset.
> 
> **Goal:** Filter rows where `[condition_1]` and `[condition_2]`. 
> **Output Format:** Save a ranked CSV containing only `[column_list]`, sorted by `[sort_column]` descending.
> **Constraints:** The script must accept input and output file paths as command-line arguments using `argparse`. Handle missing values in `[column_name]` by filling them with `[default_value]`.
> **Quality Criteria:** Do NOT wrap the core logic in a generic `try-except` block; let pandas fail fast and raise standard errors. Use PEP-8 type hints for all functions.
> **Verification Requirements:** Ensure argparse provides helpful descriptions for the arguments. Include a concise module-level docstring showing an exact example bash command to run the script.
