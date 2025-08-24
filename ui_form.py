import re
from typing import Any, Dict
import streamlit as st
from models import Dependent, EducationItem

def render_editable_form(form_dict: Dict[str, Any]) -> Dict[str, Any]:
    st.subheader("Intake Form (editable)")

    # Basic Personal Info
    st.markdown("### Basic Personal Info")
    b = form_dict["basic_personal_info"]
    b["full_name"] = st.text_input("Full name", value=b.get("full_name") or "")
    b["date_of_birth"] = st.text_input("Date of birth (YYYY-MM-DD)", value=b.get("date_of_birth") or "")
    b["gender"] = st.text_input("Gender (optional)", value=b.get("gender") or "")
    b["nationality"] = st.text_input("Nationality", value=b.get("nationality") or "")
    b["passport_or_id"] = st.text_input("Passport/ID (optional)", value=b.get("passport_or_id") or "")
    b["phone"] = st.text_input("Phone", value=b.get("phone") or "")
    b["email"] = st.text_input("Email", value=b.get("email") or "")
    b["preferred_language"] = st.text_input("Preferred language", value=b.get("preferred_language") or "")

    # Address & Permits
    st.markdown("### Address & Permits")
    a = form_dict["address_and_permits"]
    a["address_line1"] = st.text_input("Address line 1", value=a.get("address_line1") or "")
    a["address_line2"] = st.text_input("Address line 2 (optional)", value=a.get("address_line2") or "")
    a["city"] = st.text_input("City", value=a.get("city") or "")
    a["state_or_province"] = st.text_input("State/Province", value=a.get("state_or_province") or "")
    a["postal_code"] = st.text_input("Postal/ZIP", value=a.get("postal_code") or "")
    a["country"] = st.text_input("Country", value=a.get("country") or "")
    a["permit_type"] = st.text_input("Permit/Status type", value=a.get("permit_type") or "")
    a["permit_number"] = st.text_input("Permit number", value=a.get("permit_number") or "")
    a["permit_expiry_date"] = st.text_input("Permit expiry (YYYY-MM-DD)", value=a.get("permit_expiry_date") or "")

    # Employment
    st.markdown("### Employment")
    e = form_dict["employment"]
    e["status"] = st.text_input("Employment status", value=e.get("status") or "")
    e["employer_name"] = st.text_input("Employer name", value=e.get("employer_name") or "")
    e["job_title"] = st.text_input("Job title", value=e.get("job_title") or "")
    e["start_date"] = st.text_input("Job start date (YYYY-MM-DD)", value=e.get("start_date") or "")
    e["income_per_month"] = st.text_input("Monthly income (e.g., 1200 USD)", value=e.get("income_per_month") or "")
    e["pay_frequency"] = st.text_input("Pay frequency (monthly/biweekly/weekly/hourly)", value=e.get("pay_frequency") or "")
    wp_idx = 0
    if e.get("work_permit_required") is True: wp_idx = 1
    if e.get("work_permit_required") is False: wp_idx = 2
    wp_choice = st.selectbox("Work permit required?", options=["", "yes", "no"], index=wp_idx)
    e["work_permit_required"] = True if wp_choice == "yes" else False if wp_choice == "no" else None

    # Housing
    st.markdown("### Housing")
    h = form_dict["housing"]
    h["status"] = st.text_input("Housing status", value=h.get("status") or "")
    h["address_if_different"] = st.text_input("Housing address (if different)", value=h.get("address_if_different") or "")
    h["landlord_name"] = st.text_input("Landlord name (optional)", value=h.get("landlord_name") or "")
    h["lease_start_date"] = st.text_input("Lease start (YYYY-MM-DD)", value=h.get("lease_start_date") or "")
    h["lease_end_date"] = st.text_input("Lease end (YYYY-MM-DD)", value=h.get("lease_end_date") or "")
    h["monthly_rent"] = st.text_input("Monthly rent (e.g., 900 USD)", value=h.get("monthly_rent") or "")
    rooms_val = h.get("rooms")
    h["rooms"] = st.number_input("Rooms", min_value=0, max_value=50, value=int(rooms_val) if isinstance(rooms_val, int) else 0)

    # Dependents
    st.markdown("### Dependents")
    di = form_dict["dependents_information"]
    num = di.get("number_of_dependents") if isinstance(di.get("number_of_dependents"), int) else 0
    di["number_of_dependents"] = st.number_input("Number of dependents", min_value=0, max_value=20, value=num)

    dep_list = di.get("dependents", [])
    while len(dep_list) < di["number_of_dependents"]:
        dep_list.append(Dependent().model_dump())
    if len(dep_list) > di["number_of_dependents"]:
        dep_list = dep_list[: di["number_of_dependents"]]
    di["dependents"] = dep_list

    for i, dep in enumerate(dep_list, start=1):
        with st.expander(f"Dependent {i}"):
            dep["name"] = st.text_input(f"Name (dep {i})", value=dep.get("name") or "")
            dep["relationship"] = st.text_input(f"Relationship (dep {i})", value=dep.get("relationship") or "")
            dep["date_of_birth"] = st.text_input(f"DOB (YYYY-MM-DD) (dep {i})", value=dep.get("date_of_birth") or "")
            ic_idx = 0
            if dep.get("in_country") is True: ic_idx = 1
            if dep.get("in_country") is False: ic_idx = 2
            ic_choice = st.selectbox(f"In country? (dep {i})", options=["", "yes", "no"], index=ic_idx, key=f"dep_{i}_in_country")
            dep["in_country"] = True if ic_choice == "yes" else False if ic_choice == "no" else None
            dep["special_needs"] = st.text_input(f"Special needs (dep {i})", value=dep.get("special_needs") or "")

    # Financial
    st.markdown("### Financial")
    f = form_dict["financial_information"]
    ba_idx = 0
    if f.get("has_bank_account") is True: ba_idx = 1
    if f.get("has_bank_account") is False: ba_idx = 2
    ba_choice = st.selectbox("Bank account?", options=["", "yes", "no"], index=ba_idx)
    f["has_bank_account"] = True if ba_choice == "yes" else False if ba_choice == "no" else None
    f["bank_name"] = st.text_input("Bank name (optional)", value=f.get("bank_name") or "")
    f["monthly_income"] = st.text_input("Total monthly income", value=f.get("monthly_income") or "")
    f["monthly_expenses"] = st.text_input("Total monthly expenses", value=f.get("monthly_expenses") or "")
    f["savings_amount"] = st.text_input("Savings amount", value=f.get("savings_amount") or "")
    f["debts_amount"] = st.text_input("Debts amount", value=f.get("debts_amount") or "")

    # Education
    st.markdown("### Education (optional)")
    edu = form_dict["education"]
    edu["highest_level"] = st.text_input("Highest education level", value=edu.get("highest_level") or "")
    items = edu.get("items", [])
    add_more = st.number_input("Number of education entries", min_value=0, max_value=20, value=len(items))
    while len(items) < add_more:
        items.append(EducationItem().model_dump())
    if len(items) > add_more:
        items = items[:add_more]
    edu["items"] = items
    for i, it in enumerate(items, start=1):
        with st.expander(f"Education item {i}"):
            it["degree"] = st.text_input(f"Degree (item {i})", value=it.get("degree") or "")
