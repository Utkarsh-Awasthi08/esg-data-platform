from django.urls import path
from .views import ESGDashboardAPIView, FuelESGListAPIView, FuelUploadAPIView, MonthlyEmissionAPIView, ProcurementESGListAPIView, ProcurementUploadAPIView, TravelImportAPIView, ValidationInsightsAPIView
from ingestion.views import (
    ElectricityUploadAPIView,
    ElectricityESGListAPIView
)
urlpatterns = [
    path('upload/fuel/', FuelUploadAPIView.as_view()),
    path('fuel-esg/',FuelESGListAPIView.as_view()),
    path('upload/procurement/',ProcurementUploadAPIView.as_view()),
    path('upload/electricity/',ElectricityUploadAPIView.as_view()),
    path('electricity-esg/',ElectricityESGListAPIView.as_view()),
    path('procurement-esg/',ProcurementESGListAPIView.as_view()),
    path('dashboard/',ESGDashboardAPIView.as_view()),
    path('analytics/monthly-emissions/',MonthlyEmissionAPIView.as_view()),
    path('analytics/validation-insights/',ValidationInsightsAPIView.as_view()),
    path('import/travel/',TravelImportAPIView.as_view()
),
]