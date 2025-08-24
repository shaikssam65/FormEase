from typing import List, Optional
from pydantic import BaseModel, Field

class BasicPersonalInfo(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None      # ISO YYYY-MM-DD
    gender: Optional[str] = None
    nationality: Optional[str] = None
    passport_or_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    preferred_language: Optional[str] = None

class AddressAndPermits(BaseModel):
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state_or_province: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    permit_type: Optional[str] = None
    permit_number: Optional[str] = None
    permit_expiry_date: Optional[str] = None  # ISO

class Employment(BaseModel):
    status: Optional[str] = None
    employer_name: Optional[str] = None
    job_title: Optional[str] = None
    start_date: Optional[str] = None          # ISO
    income_per_month: Optional[str] = None
    pay_frequency: Optional[str] = None
    work_permit_required: Optional[bool] = None

class Housing(BaseModel):
    status: Optional[str] = None
    address_if_different: Optional[str] = None
    landlord_name: Optional[str] = None
    lease_start_date: Optional[str] = None    # ISO
    lease_end_date: Optional[str] = None      # ISO
    monthly_rent: Optional[str] = None
    rooms: Optional[int] = None

class Dependent(BaseModel):
    name: Optional[str] = None
    relationship: Optional[str] = None
    date_of_birth: Optional[str] = None       # ISO
    in_country: Optional[bool] = None
    special_needs: Optional[str] = None

class DependentsInformation(BaseModel):
    number_of_dependents: Optional[int] = None
    dependents: List[Dependent] = Field(default_factory=list)

class FinancialInformation(BaseModel):
    has_bank_account: Optional[bool] = None
    bank_name: Optional[str] = None
    monthly_income: Optional[str] = None
    monthly_expenses: Optional[str] = None
    savings_amount: Optional[str] = None
    debts_amount: Optional[str] = None

# Optional sections
class EducationItem(BaseModel):
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    institution: Optional[str] = None
    start_date: Optional[str] = None          # ISO
    end_date: Optional[str] = None            # ISO
    country: Optional[str] = None

class Education(BaseModel):
    highest_level: Optional[str] = None
    items: List[EducationItem] = Field(default_factory=list)

class Skills(BaseModel):
    skills: List[str] = Field(default_factory=list)

class FormData(BaseModel):
    basic_personal_info: BasicPersonalInfo = BasicPersonalInfo()
    address_and_permits: AddressAndPermits = AddressAndPermits()
    employment: Employment = Employment()
    housing: Housing = Housing()
    dependents_information: DependentsInformation = DependentsInformation()
    financial_information: FinancialInformation = FinancialInformation()
    education: Education = Education()
    skills: Skills = Skills()
