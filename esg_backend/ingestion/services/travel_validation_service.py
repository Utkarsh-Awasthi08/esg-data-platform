from ingestion.models import ValidationIssue


def validate_travel_record(record):

    if record.amount > 10000:

        ValidationIssue.objects.create(
            content_object=record,
            severity='SUSPICIOUS',
            issue_text='Very high travel expense'
        )

    if not record.activity_date:

        ValidationIssue.objects.create(
            content_object=record,
            severity='WARNING',
            issue_text='Missing travel date'
        )