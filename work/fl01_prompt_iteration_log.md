# Prompt Iteration Log: Debugging Complex Python Errors

**Target Task (from FL-01 Audit):** Debugging complex Python errors in my data pipelines.

## Baseline (V0)
**Prompt:** "Fix my python code. I'm getting a KeyError when running my content refresh script."
**Output:** Generates a massive list of 10 different reasons a KeyError can happen in Python, ranging from dictionaries to pandas, and asks me to provide the code.
**Iteration Note:** 
*   **What changed:** Nothing (baseline).
*   **Output Difference:** The AI is completely unhelpful because it's guessing blindly. It wastes time explaining what a dictionary is instead of helping me debug my actual script.

## Version 1: Role Assignment
**Prompt:** "You are a senior data engineer specializing in Python and pandas. Fix my python code. I'm getting a KeyError when running my content refresh script."
**Output:** The tone shifts dramatically. Instead of explaining basic python concepts, it assumes I am a developer. It immediately asks to see the specific pandas dataframe head and the exact stack trace, using industry-standard terminology.
**Iteration Note:**
*   **What changed:** Added **Role Assignment**.
*   **Output Difference:** The AI stopped talking down to me and skipped the beginner tutorials, saving me reading time and getting straight to technical troubleshooting.

## Version 2: Context and Motivation
**Prompt:** "You are a senior data engineer specializing in Python and pandas. I am an intern building a content opportunity scoring model. My script reads a CSV of search logs, but when I try to sort by 'impressions_90d', I get a KeyError. Fix my code."
**Output:** It correctly deduces that 'impressions_90d' is missing from the DataFrame columns. It provides a specific code snippet (`print(df.columns)`) to check the loaded columns, and warns me that CSV parsers sometimes add trailing whitespaces to headers.
**Iteration Note:**
*   **What changed:** Added **Context and Motivation**.
*   **Output Difference:** Because it knows I'm reading a CSV, it correctly hypothesized the most common CSV-related KeyError bugs (trailing whitespace in headers, wrong delimiter), providing actionable fixes instead of generic advice.

## Version 3: Few-Shot Examples
**Prompt:** "You are a senior data engineer specializing in Python and pandas. I am an intern building a content opportunity scoring model. My script reads a CSV of search logs, but when I try to sort by 'impressions_90d', I get a KeyError. 
Example of how I want you to answer:
*Root Cause:* You are trying to access a column that doesn't exist.
*Diagnostic Step:* Run `print(df.columns)` to see what columns actually loaded.
*Fix:* Rename the column if it's misspelled.
Now, give me a comprehensive answer for my issue."
**Output:** The AI perfectly mimics the structure I provided, separating its answer into Root Cause, Diagnostic Step, and Fix, covering whitespace issues, delimiter issues, and casing mismatches.
**Iteration Note:**
*   **What changed:** Added **Few-Shot Examples**.
*   **Output Difference:** The output became instantly scannable. Instead of reading a block of paragraphs, I could jump straight to the "Fix" section for three different potential causes.

## Version 4: Output Structure
**Prompt:** "You are a senior data engineer. I'm building a scoring model. My script reads a CSV, but when I sort by 'impressions_90d', I get a KeyError. 
Format your response exactly as a Markdown table with three columns: 'Potential Cause', 'How to Check (Code)', and 'How to Fix (Code)'."
**Output:** A clean, 3-row markdown table covering whitespace, delimiter issues, and case-sensitivity, with exact code snippets in the columns.
**Iteration Note:**
*   **What changed:** Added **Output Structure**.
*   **Output Difference:** The readability improved 10x. I no longer have to parse natural language at all; it acts as a perfect cheat-sheet I can copy-paste from directly.

## Version 5: Step Decomposition
**Prompt:** "You are a senior data engineer. I'm building a scoring model. My script reads a CSV, but when I sort by 'impressions_90d', I get a KeyError. 
Follow these steps exactly:
1. First, list the top 3 most likely reasons a KeyError happens when loading a CSV into Pandas.
2. Second, provide a single defensive Python function that loads a CSV and safely standardizes the column names (lowercasing, stripping whitespace) to prevent this from ever happening again.
3. Finally, output the results from Step 1 and Step 2 in a single Markdown table."
**Output:** The AI executes the steps sequentially. It provides a table where the first column explains the cause, and the next column provides the defensive `pd.read_csv` wrapper function that prevents that specific cause.
**Iteration Note:**
*   **What changed:** Added **Step Decomposition**.
*   **Output Difference:** The AI stopped just fixing the immediate bug, and provided a systemic architectural fix (a defensive loading function). Forcing it to think about the causes *before* writing the code made the resulting function much more robust.

---

## Cross-Model Comparison (Claude vs. ChatGPT)
I ran the final V5 prompt on both Claude (Sonnet) and ChatGPT (GPT-4o).
*   **Tone:** Claude maintained the "senior data engineer" persona much better, keeping explanations brief and highly technical. ChatGPT was a bit overly enthusiastic ("Great question! Let's get that fixed!") which felt slightly less professional.
*   **Accuracy & Structure:** Both models successfully generated the defensive pandas loading function and followed the strict Markdown table structure.
*   **Failure Points:** ChatGPT hallucinated a slightly more complex dictionary comprehension for renaming columns, whereas Claude used the much cleaner built-in `df.columns.str.strip().str.lower()`. 
*   **Conclusion:** Claude's output was more idiomatic and concise for this specific pandas task, making it the winner for Python data engineering debugging.

---

## Final Reusable Template

> **Role:** You are a senior software engineer specializing in `[Language/Framework]`.
> **Context:** I am working on `[Project Name/Description]`. I am encountering a `[Error Type]` when trying to `[Action you are trying to do]`. 
> Here is my stack trace and code snippet: 
> `[Insert Code/Error]`
> 
> **Instructions:** Follow these steps sequentially:
> 1. Identify the root cause of the specific error provided.
> 2. Write the corrected code snippet that resolves the error.
> 3. Write a defensive programming recommendation to prevent this class of error in the future.
> 
> **Output Structure:** Present your final answer strictly in a markdown table with three headers: "Root Cause", "Corrected Code", and "Defensive Recommendation".
