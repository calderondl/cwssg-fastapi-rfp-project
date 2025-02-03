import pandas
import re
import os
import calendar

# Split capacity values into numeric and unit parts
def clean_capacity(value):
    if not value:
        return 0, "Unknown"
    
    value = str(value)
    match = re.match(r"(\d+(\.\d+)?)\s*(\w+)", value)
    return (float(match.group(1)), match.group(3)) if match else (0, "Unknown")

# Transform the raw dataset into structured tables
def process_data(df):    
    # Column mapping: Existing → Required
    column_mapping = {
        # RFP Table
        "rfp_documents": "request_for_proposal_document",
        "rfp_identifier": "request_for_proposal_identifier",
        "rfp_upload_date": "request_for_proposal_upload_date_time",
        "service_request_rfp_attachment": "request_for_proposal_attachment_count",

        # Billed Entities Table
        "billed_entity_zip": "billed_entity_zip_code",
        "billed_entity_zip_ext": "billed_entity_zip_code_ext",
    }
    df = df.rename(columns=column_mapping)

    # Prioritize Current, fallback to Original
    df.sort_values(by=['application_number', 'form_version'], key=lambda x: x == 'Current', ascending=False, inplace=True)
    df = df.drop_duplicates(subset=['application_number'], keep='first')

    # Handle missing values
    df['quantity'] = df['quantity'].fillna(1)
    df['entities'] = df['entities'].fillna(1)

    # Total Services Requested new column
    df['total_services_requested'] = df['quantity'].astype(int) * df['entities'].astype(int)

    # Split Capacity columns
    df[['min_capacity_num', 'min_capacity_unit']] = df['minimum_capacity'].apply(lambda x: pandas.Series(clean_capacity(x)))
    df[['max_capacity_num', 'max_capacity_unit']] = df['maximum_capacity'].apply(lambda x: pandas.Series(clean_capacity(x)))

    # RFP Table
    rfp_cols = [
        'application_number', 'request_for_proposal_document', 'request_for_proposal_identifier',
        'request_for_proposal_upload_date_time', 'minimum_capacity', 'maximum_capacity',
        'entities', 'quantity', 'service_request_id', 'request_for_proposal_attachment_count',
        'form_version', 'funding_year', 'fcc_form_470_status', 'allowable_contract_date',
        'certified_date_time', 'last_modified_date_time', 'total_services_requested',
        'min_capacity_num', 'min_capacity_unit', 'max_capacity_num', 'max_capacity_unit'
    ]
    rfp_df = df[rfp_cols]
    rfp_df.to_csv("output/rfp_data.csv", index=False)

    # Billed Entities Table
    billed_df = df[['billed_entity_number', 'billed_entity_name', 'billed_entity_city', 'billed_entity_state',
                    'billed_entity_zip_code', 'billed_entity_zip_code_ext', 'billed_entity_email',
                    'billed_entity_phone', 'billed_entity_phone_ext']].drop_duplicates()
    billed_df.insert(0, 'billed_entity_id', range(1, 1 + len(billed_df)))
    billed_df.to_csv("output/billed_entities.csv", index=False)

    # Contacts Table
    contacts_df = df[['contact_name', 'contact_address1', 'contact_city', 'contact_state', 'contact_zip',
                      'contact_zip_ext', 'contact_phone', 'contact_email']].drop_duplicates()
    contacts_df.insert(0, 'contact_id', range(1, 1 + len(contacts_df)))
    contacts_df.to_csv("output/contacts.csv", index=False)

    # Services Table
    services_df = df[['service_request_id', 'service_category', 'service_type', 'function']].drop_duplicates()
    services_df.insert(0, 'service_id', range(1, 1 + len(services_df)))
    services_df.to_csv("output/services.csv", index=False)

    # Averange services requested per month
    df['month'] = pandas.to_datetime(df['request_for_proposal_upload_date_time'], errors='coerce').dt.strftime('%B')
    monthly_averages = df.groupby('month')['total_services_requested'].mean().astype(int).round(0).to_dict()
    sorted_monthly_averages = {month: monthly_averages.get(month, 0) for month in calendar.month_name if month in monthly_averages}

    return len(rfp_df), len(os.listdir("output")), sorted_monthly_averages