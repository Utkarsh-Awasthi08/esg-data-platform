import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class UploadedFile(models.Model):

    SOURCE_CHOICES = [
        ('SAP', 'SAP'),
        ('UTILITY', 'UTILITY'),
    ]

    TYPE_CHOICES = [
        ('FUEL', 'FUEL'),
        ('PROCUREMENT', 'PROCUREMENT'),
        ('ELECTRICITY', 'ELECTRICITY'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    filename = models.CharField(max_length=255)

    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)

    file_type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename


class FuelRecord(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('FAILED', 'FAILED'),
        ('WARNING', 'WARNING'),
        ('SUSPICIOUS', 'SUSPICIOUS'),
        ('APPROVED', 'APPROVED'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    uploaded_file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        related_name='fuel_records'
    )

    MANDT = models.CharField(max_length=50, blank=True, null=True)
    EBELN = models.CharField(max_length=50, blank=True, null=True)
    EBELP = models.CharField(max_length=50, blank=True, null=True)
    AEDAT = models.CharField(max_length=50, blank=True, null=True)
    MATNR = models.CharField(max_length=100, blank=True, null=True)
    TXZ01 = models.TextField(blank=True, null=True)
    MENGE = models.FloatField(blank=True, null=True)
    MEINS = models.CharField(max_length=50, blank=True, null=True)
    NETPR = models.FloatField(blank=True, null=True)
    PEINH = models.CharField(max_length=50, blank=True, null=True)
    WAERS = models.CharField(max_length=20, blank=True, null=True)
    WERKS = models.CharField(max_length=50, blank=True, null=True)
    LGORT = models.CharField(max_length=50, blank=True, null=True)
    LIFNR = models.CharField(max_length=50, blank=True, null=True)
    NAME1 = models.CharField(max_length=255, blank=True, null=True)
    MATKL = models.CharField(max_length=100, blank=True, null=True)

    validation_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.TXZ01} - {self.MENGE}"


class ProcurementRecord(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('FAILED', 'FAILED'),
        ('WARNING', 'WARNING'),
        ('SUSPICIOUS', 'SUSPICIOUS'),
        ('APPROVED', 'APPROVED'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    uploaded_file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        related_name='procurement_records'
    )

    MANDT = models.CharField(max_length=50, blank=True, null=True)
    EBELN = models.CharField(max_length=50, blank=True, null=True)
    EBELP = models.CharField(max_length=50, blank=True, null=True)
    AEDAT = models.CharField(max_length=50, blank=True, null=True)
    KNTTP = models.CharField(max_length=50, blank=True, null=True)
    ANLN1 = models.CharField(max_length=50, blank=True, null=True)
    TXZ01 = models.TextField(blank=True, null=True)
    MENGE = models.FloatField(blank=True, null=True)
    MEINS = models.CharField(max_length=50, blank=True, null=True)
    NETPR = models.FloatField(blank=True, null=True)
    WAERS = models.CharField(max_length=20, blank=True, null=True)
    WERKS = models.CharField(max_length=50, blank=True, null=True)
    LIFNR = models.CharField(max_length=50, blank=True, null=True)
    NAME1 = models.CharField(max_length=255, blank=True, null=True)
    MATKL = models.CharField(max_length=100, blank=True, null=True)

    validation_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.TXZ01} - {self.MENGE}"


class ElectricityRecord(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('FAILED', 'FAILED'),
        ('WARNING', 'WARNING'),
        ('SUSPICIOUS', 'SUSPICIOUS'),
        ('APPROVED', 'APPROVED'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    uploaded_file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        related_name='electricity_records'
    )

    Account_No = models.CharField(max_length=100, blank=True, null=True)

    Facility_ID = models.CharField(max_length=100, blank=True, null=True)

    Meter_ID = models.CharField(max_length=100, blank=True, null=True)

    Register_Type = models.CharField(max_length=100, blank=True, null=True)

    Billing_Start = models.DateField(blank=True, null=True)

    Billing_End = models.DateField(blank=True, null=True)

    Previous_Reading = models.FloatField(blank=True, null=True)

    Current_Reading = models.FloatField(blank=True, null=True)

    Multiplier = models.FloatField(blank=True, null=True)

    kWh_Usage = models.FloatField(blank=True, null=True)

    Tariff_Code = models.CharField(max_length=100, blank=True, null=True)

    Rate_Per_kWh = models.FloatField(blank=True, null=True)

    Fixed_Charge = models.FloatField(blank=True, null=True)

    Tax_Amount = models.FloatField(blank=True, null=True)

    Total_Amount = models.FloatField(blank=True, null=True)

    Currency = models.CharField(max_length=20, blank=True, null=True)

    validation_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Meter_ID} - {self.kWh_Usage} kWh"
    
class FuelESGRecord(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    raw_record = models.OneToOneField(
        FuelRecord,
        on_delete=models.CASCADE,
        related_name='normalized_record'
    )

    fuel_type = models.CharField(max_length=255)

    quantity = models.FloatField()

    normalized_quantity = models.FloatField(blank=True, null=True)

    normalized_unit = models.CharField(max_length=50)

    scope = models.CharField(max_length=50, default='Scope 1')

    facility = models.CharField(max_length=255, blank=True, null=True)

    supplier = models.CharField(max_length=255, blank=True, null=True)

    activity_date = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=20, default='PENDING')

    normalized_payload = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    calculated_emission = models.FloatField(
    null=True,
    blank=True
    )

class ProcurementESGRecord(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    raw_record = models.OneToOneField(
        ProcurementRecord,
        on_delete=models.CASCADE,
        related_name='normalized_record'
    )

    procurement_category = models.CharField(max_length=255)

    material_description = models.TextField()

    quantity = models.FloatField(blank=True, null=True)

    normalized_quantity = models.FloatField(blank=True, null=True)

    unit = models.CharField(max_length=50)

    supplier = models.CharField(max_length=255)

    facility = models.CharField(max_length=255, blank=True, null=True)

    scope = models.CharField(max_length=50, default='Scope 3')

    spend_amount = models.FloatField(blank=True, null=True)

    currency = models.CharField(max_length=20)

    activity_date = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=20, default='PENDING')

    normalized_payload = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    calculated_emission = models.FloatField(
    null=True,
    blank=True
    )

class ElectricityESGRecord(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    raw_record = models.OneToOneField(
        ElectricityRecord,
        on_delete=models.CASCADE,
        related_name='normalized_record'
    )

    facility = models.CharField(max_length=255)

    meter_id = models.CharField(max_length=255)

    electricity_usage = models.FloatField()

    normalized_unit = models.CharField(max_length=50, default='kWh')

    register_type = models.CharField(max_length=100, blank=True, null=True)

    tariff_code = models.CharField(max_length=100, blank=True, null=True)

    billing_start = models.DateField(blank=True, null=True)

    billing_end = models.DateField(blank=True, null=True)

    scope = models.CharField(max_length=50, default='Scope 2')

    status = models.CharField(max_length=20, default='PENDING')

    normalized_payload = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    account_number = models.CharField(
    max_length=100,
    blank=True,
    null=True
    )

    previous_reading = models.FloatField(
    blank=True,
    null=True
    )

    current_reading = models.FloatField(
    blank=True,
    null=True
    )

    multiplier = models.FloatField(
    blank=True,
    null=True
    )

    rate_per_kwh = models.FloatField(
    blank=True,
    null=True
    )

    total_amount = models.FloatField(
    blank=True,
    null=True
    )

    currency = models.CharField(
    max_length=20,
    blank=True,
    null=True
    )

    calculated_emission = models.FloatField(
    null=True,
    blank=True
    )


class ValidationIssue(models.Model):

    SEVERITY_CHOICES = [
        ('FAILED', 'FAILED'),
        ('WARNING', 'WARNING'),
        ('SUSPICIOUS', 'SUSPICIOUS'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    #
    # Generic Relation
    #

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )

    object_id = models.UUIDField()

    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )

    #
    # Validation Data
    #

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES
    )

    issue_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.severity} - {self.issue_text}"
    

class TravelBooking(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    booking_id = models.CharField(max_length=255)

    trip_id = models.CharField(max_length=255)

    booking_status = models.CharField(max_length=100)

    amount = models.FloatField()

    currency = models.CharField(max_length=20)

    imported_at = models.DateTimeField()

    raw_payload = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)


class TravelESGRecord(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    raw_record = models.OneToOneField(
        TravelBooking,
        on_delete=models.CASCADE,
        related_name='normalized_record'
    )

    travel_type = models.CharField(
        max_length=100,
        default='Flight'
    )

    scope = models.CharField(
        max_length=50,
        default='Scope 3'
    )

    amount = models.FloatField()

    currency = models.CharField(max_length=20)

    calculated_emission = models.FloatField(
        null=True,
        blank=True
    )

    activity_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default='PENDING'
    )

    normalized_payload = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

class EmissionFactor(models.Model):

    CATEGORY_CHOICES = [
        ('fuel', 'Fuel'),
        ('electricity', 'Electricity'),
        ('procurement', 'Procurement')
    ]

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    factor_name = models.CharField(max_length=100)

    unit = models.CharField(max_length=50)

    emission_factor = models.FloatField()

    source = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.category} - {self.factor_name}"

# class ValidationIssue(models.Model):

#     SEVERITY_CHOICES = [
#         ('FAILED', 'FAILED'),
#         ('WARNING', 'WARNING'),
#         ('SUSPICIOUS', 'SUSPICIOUS'),
#     ]

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     normalized_record = models.ForeignKey(
#         ESGNormalizedRecord,
#         on_delete=models.CASCADE,
#         related_name='issues'
#     )

#     severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)

#     issue_text = models.TextField()

#     created_at = models.DateTimeField(auto_now_add=True)

# class AuditLog(models.Model):

#     ACTION_CHOICES = [
#         ('UPLOADED', 'UPLOADED'),
#         ('VALIDATED', 'VALIDATED'),
#         ('APPROVED', 'APPROVED'),
#         ('REJECTED', 'REJECTED'),
#     ]

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     normalized_record = models.ForeignKey(
#         ESGNormalizedRecord,
#         on_delete=models.CASCADE,
#         related_name='audit_logs'
#     )

#     action = models.CharField(max_length=50, choices=ACTION_CHOICES)

#     action_time = models.DateTimeField(auto_now_add=True)

#     performed_by = models.CharField(max_length=255, blank=True, null=True)