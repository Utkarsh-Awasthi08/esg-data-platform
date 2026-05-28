from ingestion.models import ValidationIssue
from django.contrib.contenttypes.models import ContentType


def validate_electricity_record(electricity_esg_record):

    issues_found = []

    #
    # FAILED
    #

    if (
        electricity_esg_record.electricity_usage is None
        or electricity_esg_record.electricity_usage <= 0
    ):

        issues_found.append({
            'severity': 'FAILED',
            'issue_text': 'Electricity usage must be greater than zero.'
        })

    if not electricity_esg_record.facility:

        issues_found.append({
            'severity': 'FAILED',
            'issue_text': 'Facility missing.'
        })

    if (
        electricity_esg_record.billing_start
        and electricity_esg_record.billing_end
        and electricity_esg_record.billing_start >
        electricity_esg_record.billing_end
    ):

        issues_found.append({
            'severity': 'FAILED',
            'issue_text': 'Billing start date cannot be after billing end date.'
        })

    #
    # WARNING
    #

    if not electricity_esg_record.tariff_code:

        issues_found.append({
            'severity': 'WARNING',
            'issue_text': 'Tariff code missing.'
        })

    if electricity_esg_record.electricity_usage > 100000:

        issues_found.append({
            'severity': 'WARNING',
            'issue_text': 'Very high electricity usage detected.'
        })

    #
    # SUSPICIOUS
    #

    if (
        electricity_esg_record.current_reading
        and electricity_esg_record.previous_reading
        and electricity_esg_record.current_reading <
        electricity_esg_record.previous_reading
    ):

        issues_found.append({
            'severity': 'SUSPICIOUS',
            'issue_text': 'Current reading is lower than previous reading.'
        })

    #
    # Usage mismatch check
    #

    if (
        electricity_esg_record.previous_reading is not None
        and electricity_esg_record.current_reading is not None
        and electricity_esg_record.multiplier is not None
    ):

        calculated_usage = (
            (
                electricity_esg_record.current_reading
                - electricity_esg_record.previous_reading
            )
            * electricity_esg_record.multiplier
        )

        actual_usage = electricity_esg_record.electricity_usage

        difference = abs(calculated_usage - actual_usage)

        if difference > 100:

            issues_found.append({
                'severity': 'SUSPICIOUS',
                'issue_text': 'Electricity usage does not match meter readings.'
            })

    #
    # CREATE ISSUES
    #

    for issue in issues_found:

        ValidationIssue.objects.create(
            content_type=ContentType.objects.get_for_model(
                electricity_esg_record
            ),
            object_id=electricity_esg_record.id,
            severity=issue['severity'],
            issue_text=issue['issue_text']
        )

    #
    # FINAL STATUS
    #

    severities = [issue['severity'] for issue in issues_found]

    if 'FAILED' in severities:

        electricity_esg_record.status = 'FAILED'

    elif 'SUSPICIOUS' in severities:

        electricity_esg_record.status = 'SUSPICIOUS'

    elif 'WARNING' in severities:

        electricity_esg_record.status = 'WARNING'

    else:

        electricity_esg_record.status = 'APPROVED'

    electricity_esg_record.save()

    return issues_found