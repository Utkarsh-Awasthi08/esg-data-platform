from django.contrib import admin
from .models import (
    UploadedFile,
    FuelRecord,
    ProcurementRecord,
    ElectricityRecord,
    FuelESGRecord,
    ElectricityESGRecord,
    ProcurementESGRecord
)

admin.site.register(UploadedFile)
admin.site.register(FuelRecord)
admin.site.register(ProcurementRecord)
admin.site.register(ElectricityRecord)
admin.site.register(FuelESGRecord)
admin.site.register(ElectricityESGRecord)
admin.site.register(ProcurementESGRecord)