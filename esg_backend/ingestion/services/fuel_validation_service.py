from ingestion.models import ValidationIssue
from django.contrib.contenttypes.models import ContentType

VALID_UNITS = [
    'liters',
    'pieces',
    'kilograms'
]


VALID_FUEL_KEYWORDS = [
    'diesel',
    'gasoline',
    'jet',
    'fuel',
    'oil'
]


def validate_fuel_record(fuel_esg_record):

    issues_found = []

    fuel_type = (
        fuel_esg_record.fuel_type.lower()
        if fuel_esg_record.fuel_type
        else ''
    )

    #
    # FAILED VALIDATIONS
    #

    if (
        fuel_esg_record.normalized_quantity is None
        or fuel_esg_record.normalized_quantity <= 0
    ):

        issues_found.append({
            'severity': 'FAILED',
            'issue_text': 'Fuel quantity must be greater than zero.'
        })

    if not fuel_esg_record.normalized_unit:

        issues_found.append({
            'severity': 'FAILED',
            'issue_text': 'Normalized unit missing.'
        })

    #
    # WARNING VALIDATIONS
    #

    if not fuel_esg_record.supplier:

        issues_found.append({
            'severity': 'WARNING',
            'issue_text': 'Supplier information missing.'
        })

    if (
        fuel_esg_record.normalized_unit
        and fuel_esg_record.normalized_unit not in VALID_UNITS
    ):

        issues_found.append({
            'severity': 'WARNING',
            'issue_text': f'Unknown normalized unit: {fuel_esg_record.normalized_unit}'
        })

    #
    # SUSPICIOUS VALIDATIONS
    #

    if fuel_esg_record.normalized_quantity > 30000:

        issues_found.append({
            'severity': 'SUSPICIOUS',
            'issue_text': 'Unusually high fuel quantity detected.'
        })

    if not any(keyword in fuel_type for keyword in VALID_FUEL_KEYWORDS):

        issues_found.append({
            'severity': 'SUSPICIOUS',
            'issue_text': 'Fuel type does not match expected fuel categories.'
        })

    #
    # CREATE ISSUE ROWS
    #

    for issue in issues_found:
        ValidationIssue.objects.create(

        content_type=ContentType.objects.get_for_model(

            fuel_esg_record

        ),

        object_id=fuel_esg_record.id,

        severity=issue['severity'],

        issue_text=issue['issue_text']

    )

    #
    # DETERMINE FINAL STATUS
    #

    severities = [issue['severity'] for issue in issues_found]

    if 'FAILED' in severities:

        fuel_esg_record.status = 'FAILED'

    elif 'SUSPICIOUS' in severities:

        fuel_esg_record.status = 'SUSPICIOUS'

    elif 'WARNING' in severities:

        fuel_esg_record.status = 'WARNING'

    else:

        fuel_esg_record.status = 'APPROVED'

    fuel_esg_record.save()

    return issues_found