# app/utils/schema_formatter.py

from app.utils.field_schema_loader import normalize_keys


def format_invoice_data(raw_data: dict) -> dict:
    data = normalize_keys("invoice", raw_data)

    return {
        "invoice_number": data.get("invoice_number"),
        "date": data.get("date"),
        "due_date": data.get("due_date"),
        "vendor": data.get("vendor"),
        "customer": data.get("customer"),
        "billing_address": data.get("billing_address"),
        "shipping_address": data.get("shipping_address"),
        "line_items": data.get("line_items", []),
        "subtotal": data.get("subtotal"),
        "tax": data.get("tax"),
        "discounts": data.get("discounts"),
        "total": data.get("total"),
        "notes": data.get("notes"),
        "payment_info": data.get("payment_info"),
        "terms": data.get("terms"),
    }


def format_application_form(raw_data: dict) -> dict:
    data = normalize_keys("application_form", raw_data)

    return {
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "name": data.get("name"),  # in case full name is used
        "email": data.get("email"),
        "phone": data.get("phone"),
        "position": data.get("position"),
        "desired_salary": data.get("desired_salary"),
        "date_available": data.get("date_available"),
        "address": data.get("address"),
        "city": data.get("city"),
        "state": data.get("state"),
        "zip": data.get("zip"),
        "home_phone": data.get("home_phone"),
        "ssn": data.get("ssn"),
        "us_citizen": data.get("us_citizen"),
        "felony_conviction": data.get("felony_conviction"),
        "drug_screening": data.get("drug_screening"),
        "education_school_1": data.get("education_school_1"),
        "education_location_1": data.get("education_location_1"),
        "education_years_attended_1": data.get("education_years_attended_1"),
        "education_degree_1": data.get("education_degree_1"),
        "education_major_1": data.get("education_major_1"),
        "education_school_2": data.get("education_school_2"),
        "education_location_2": data.get("education_location_2"),
        "education_years_attended_2": data.get("education_years_attended_2"),
        "education_degree_2": data.get("education_degree_2"),
        "education_major_2": data.get("education_major_2"),
        "employment_employer": data.get("employment_employer"),
        "employment_dates_employed": data.get("employment_dates_employed"),
        "employment_work_phone": data.get("employment_work_phone"),
        "employment_position": data.get("employment_position"),
        "employment_may_contact": data.get("employment_may_contact"),
    }


def format_meeting_summary(raw_data: dict) -> dict:
    data = normalize_keys("meeting_summary", raw_data)

    return {
        "title": data.get("title"),
        "date": data.get("date"),
        "time": data.get("time"),
        "location": data.get("location"),
        "attendees": data.get("attendees", []),
        "agenda": data.get("agenda", []),
        "summary": data.get("summary"),
        "action_items": data.get("action_items", []),
        "decisions": data.get("decisions", []),
        "next_meeting": data.get("next_meeting"),
    }


def format_by_doc_type(doc_type: str, raw_data: dict) -> dict:
    if doc_type == "invoice":
        return format_invoice_data(raw_data)
    elif doc_type == "application_form":
        return format_application_form(raw_data)
    elif doc_type == "meeting_summary":
        return format_meeting_summary(raw_data)
    else:
        raise ValueError(f"No schema formatter defined for doc_type: {doc_type}")
