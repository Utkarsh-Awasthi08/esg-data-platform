from ingestion.models import ValidationIssue

from django.contrib.contenttypes.models import (
    ContentType
)


VALID_PROCUREMENT_CATEGORIES = [
    'MACH-01',
    'COMP-03',
    'LOGI-02',
    'CONV-01'
]


def validate_procurement_record(
    procurement_esg_record
):

    issues_found = []

    #
    # FAILED
    #

    if (
        procurement_esg_record.spend_amount is None
        or procurement_esg_record.spend_amount <= 0
    ):

        issues_found.append({
            'severity': 'FAILED',
            'issue_text':
            'Spend amount must be greater than zero.'
        })

    if not procurement_esg_record.material_description:

        issues_found.append({
            'severity': 'FAILED',
            'issue_text':
            'Material description missing.'
        })

    #
    # WARNING
    #

    if not procurement_esg_record.supplier:

        issues_found.append({
            'severity': 'WARNING',
            'issue_text':
            'Supplier information missing.'
        })

    if (
        procurement_esg_record.procurement_category
        not in VALID_PROCUREMENT_CATEGORIES
    ):

        issues_found.append({
            'severity': 'WARNING',
            'issue_text':
            'Unknown procurement category.'
        })

    #
    # SUSPICIOUS
    #

    if procurement_esg_record.spend_amount > 100000:

        issues_found.append({
            'severity': 'SUSPICIOUS',
            'issue_text':
            'Unusually high procurement spend detected.'
        })

    #
    # CREATE VALIDATION ISSUES
    #

    for issue in issues_found:

        ValidationIssue.objects.create(

            content_type=ContentType.objects.get_for_model(
                procurement_esg_record
            ),

            object_id=procurement_esg_record.id,

            severity=issue['severity'],

            issue_text=issue['issue_text']
        )

    #
    # FINAL STATUS
    #

    severities = [
        issue['severity']
        for issue in issues_found
    ]

    if 'FAILED' in severities:

        procurement_esg_record.status = 'FAILED'

    elif 'SUSPICIOUS' in severities:

        procurement_esg_record.status = 'SUSPICIOUS'

    elif 'WARNING' in severities:

        procurement_esg_record.status = 'WARNING'

    else:

        procurement_esg_record.status = 'APPROVED'

    procurement_esg_record.save()

    return issues_found