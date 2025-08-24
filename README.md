# 🤝 Migrant Support — Category-Based Extractor (Open Source)

## Live Demo
Check out the live app here: [FormEase Streamlit App](https://huggingface.co/spaces/shaiksam65/formfill)

Paste long text **by category** (Basic Info, Address & Permits, Employment, Housing, Dependents, Financial, plus optional **Education** & **Skills**) and get a clean, editable JSON form out.  
Runs locally using **Qwen/Qwen2.5-0.5B-Instruct** via Hugging Face `transformers`.

> ⚠️ This tool is **not legal advice**. It’s an intake helper to organize information.

---

## ✨ Features

- **Category inputs**: paste big chunks per section instead of answering one-by-one.
- **Schema-safe extraction**: strict prompts ensure JSON with exactly the expected keys.
- **Merge & normalize**: fills a single form and converts date strings to ISO (`YYYY-MM-DD`) when possible.
- **Live editing**: review/correct values on the right before exporting.
- **Download JSON**: one click export of the structured intake.
- **Open source & local**: works on CPU; GPU optional.

---

## 🧠 How it Works (plain English)

- You paste long, free-text **by category** (e.g., Employment).
- The app loads the open-source model **Qwen/Qwen2.5-0.5B-Instruct** locally.
- When you click **Extract** on a category (or **Extract ALL**):
  - The app sends **only that category’s JSON schema** + your pasted text to the model with a strict “return JSON only” instruction.
  - The model returns a JSON object for that category’s fields.
  - The app parses the JSON, **copies only known keys**, and **merges** into one master form.
  - Date-like strings are normalized to `YYYY-MM-DD` when possible.
- You can **edit** the merged form on the right and **Download JSON**.

---


## Project Structure

```text
formease/
├── app.py               # Streamlit app (UI & wiring)
├── models.py            # Pydantic schemas
├── llm.py               # Model loader + generation helper (Qwen by default)
├── utils.py             # Helpers (date normalization, deep-merge, JSON parsing)
├── extractors.py        # Category-scoped extraction (prompt + cleaning)
├── ui_form.py           # Right-side editable form
├── requirements.txt     # Python dependencies

## 🖥 Requirements

- **Python 3.9+**
- Internet connection for the **first run only** (to download the model). After that, offline works.

---

## 🚀 Installation & Run

```bash
# 1) (Optional but recommended) create and activate a virtual env
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install dependencies
pip install streamlit>=1.34 transformers>=4.42 accelerate>=0.33 torch>=2.2 pydantic>=2.7 python-dateutil>=2.9

# 3) Save the app as app.py (see code below)

# 4) Run
streamlit run app.py
