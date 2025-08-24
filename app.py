import json
import streamlit as st

from llm import load_llm
from utils import blank_form_dict, deep_merge, coerce_dates_in_form
from extractor import extract_category           # <- this file below
from ui_form import render_editable_form         # requires ui_form.py

# ---------- Page ----------
st.set_page_config(page_title="Form Filling — Migrant Support", page_icon="🤝", layout="wide")
st.title("🤝 Migrant Support — Data Extractor & (Qwen 2.5 0.5B)")

# ---------- Sidebar / Model ----------
with st.sidebar:
    st.header("Model")
    model_id = st.text_input("Hugging Face model", value="Qwen/Qwen2.5-0.5B-Instruct")
    tokenizer, model = load_llm(model_id)
    st.caption("Paste long text per category on the left, click Extract. Edit on the right, then download JSON.")

# ---------- Session State Guards ----------
if "form" not in st.session_state or not isinstance(st.session_state.form, dict):
    st.session_state.form = blank_form_dict()

if "inputs" not in st.session_state or not isinstance(st.session_state.inputs, dict):
    st.session_state.inputs = {
        "basic_personal_info": "",
        "address_and_permits": "",
        "employment": "",
        "housing": "",
        "dependents_information": "",
        "financial_information": "",
        "education": "",
        "skills": "",
    }

# ---------- Layout ----------
left, right = st.columns([0.52, 0.48], gap="large")

with left:
    st.subheader("Paste text by category")

    tabs = st.tabs([
        "Basic Info", "Address & Permits", "Employment", "Housing",
        "Dependents", "Financial", "Education (opt)", "Skills (opt)"
    ])

    cat_keys = [
        "basic_personal_info", "address_and_permits", "employment", "housing",
        "dependents_information", "financial_information", "education", "skills"
    ]

    for tab, key in zip(tabs, cat_keys):
        with tab:
            st.markdown(f"**{key.replace('_',' ').title()} — Input**")
            st.session_state.inputs[key] = st.text_area(
                f"Paste all details for {key.replace('_',' ').title()}",
                value=st.session_state.inputs.get(key, ""),
                height=160
            )
            colx1, colx2 = st.columns(2)
            with colx1:
                if st.button(f"Extract {key.split('_')[0].title()}", key=f"extract_{key}"):
                    text = (st.session_state.inputs.get(key) or "").strip()
                    if not text:
                        st.warning("Please paste some text before extracting.")
                    else:
                        try:
                            extracted = extract_category(tokenizer, model, key, text) or {}
                            if not isinstance(extracted, dict):
                                extracted = {}
                            st.session_state.form = deep_merge(st.session_state.form, extracted)
                            st.session_state.form = coerce_dates_in_form(st.session_state.form)
                            st.success(f"Extracted: {key.replace('_',' ').title()}")
                        except Exception as e:
                            st.error(f"Extraction failed: {e}")
            with colx2:
                if st.button(f"Clear input ({key})", key=f"clear_{key}"):
                    st.session_state.inputs[key] = ""

    st.divider()
    if st.button("🧠 Extract ALL categories"):
        any_text = False
        try:
            for k in cat_keys:
                txt = (st.session_state.inputs.get(k) or "").strip()
                if not txt:
                    continue
                any_text = True
                extracted = extract_category(tokenizer, model, k, txt) or {}
                if not isinstance(extracted, dict):
                    extracted = {}
                st.session_state.form = deep_merge(st.session_state.form, extracted)
            if any_text:
                st.session_state.form = coerce_dates_in_form(st.session_state.form)
                st.success("All available categories extracted and merged.")
            else:
                st.warning("No category inputs found. Paste text above first.")
        except Exception as e:
            st.error(f"Bulk extraction failed: {e}")

    if st.button("↺ Reset entire form"):
        st.session_state.form = blank_form_dict()
        st.success("Form reset.")

with right:
    st.session_state.form = render_editable_form(st.session_state.form)

    st.divider()
    st.markdown("### Finish")
    final_json = json.dumps(coerce_dates_in_form(st.session_state.form), indent=2)
    st.download_button(
        label="📥 Download JSON",
        data=final_json.encode("utf-8"),
        file_name="migrant_support_intake.json",
        mime="application/json",
    )
    with st.expander("Preview JSON"):
        st.code(final_json, language="json")
