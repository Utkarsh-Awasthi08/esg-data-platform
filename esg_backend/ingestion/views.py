import genericpath
import pandas as pd
from ingestion.services.calculate_travel_emission import calculate_travel_emission
from ingestion.services.travel_validation_service import validate_travel_record
from rest_framework.views import APIView
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework.response import Response
import requests
from django.db.models import Sum

from ingestion.models import (

    FuelESGRecord,

    ElectricityESGRecord,

    ProcurementESGRecord,

    ValidationIssue

)
from .services.emission_service import calculate_fuel_emission
from .services.fuel_validation_service import validate_fuel_record
from rest_framework.generics import ListAPIView
from rest_framework import generics

from .models import ProcurementESGRecord, TravelESGRecord

from .serializers import ProcurementESGRecordSerializer
from .models import FuelESGRecord
from .serializers import ElectricityESGSerializer, FuelESGRecordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.normalization_service import normalize_unit_and_quantity
from .models import UploadedFile, FuelRecord, FuelESGRecord
from .serializers import FileUploadSerializer
from .models import (
    UploadedFile,
    ProcurementRecord,
    ProcurementESGRecord
)

from .services.procurement_validation_service import (
    validate_procurement_record
)
from .models import (
    UploadedFile,
    ElectricityRecord,
    ElectricityESGRecord
)

from .services.electricity_validation_engine import (
    validate_electricity_record
)
class FuelUploadAPIView(APIView):

    def post(self, request):

        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():

            uploaded_csv = serializer.validated_data['file']

            source = serializer.validated_data['source']

            file_type = serializer.validated_data['file_type']

            uploaded_file = UploadedFile.objects.create(
                filename=uploaded_csv.name,
                source=source,
                file_type=file_type
            )

            df = pd.read_csv(uploaded_csv)

            for _, row in df.iterrows():

                fuel_record = FuelRecord.objects.create(
                    uploaded_file=uploaded_file,

                    MANDT=row.get('MANDT'),
                    EBELN=row.get('EBELN'),
                    EBELP=row.get('EBELP'),
                    AEDAT=row.get('AEDAT'),
                    MATNR=row.get('MATNR'),
                    TXZ01=row.get('TXZ01'),
                    MENGE=row.get('MENGE'),
                    MEINS=row.get('MEINS'),
                    NETPR=row.get('NETPR'),
                    PEINH=row.get('PEINH'),
                    WAERS=row.get('WAERS'),
                    WERKS=row.get('WERKS'),
                    LGORT=row.get('LGORT'),
                    LIFNR=row.get('LIFNR'),
                    NAME1=row.get('NAME1'),
                    MATKL=row.get('MATKL'),
                )

                normalized_quantity, normalized_unit = normalize_unit_and_quantity(
                    row.get('MENGE'),
                    row.get('MEINS')
                )
                calculated_emission = calculate_fuel_emission(
                    row.get('TXZ01'),
                    normalized_quantity,
                    normalized_unit
                )
                
                activity_date = None

                if pd.notna(row.get('AEDAT')):
                    activity_date = pd.to_datetime(
                    row.get('AEDAT')
                ).date()
                fuel_esg_record = FuelESGRecord.objects.create(

                    raw_record=fuel_record,

                    fuel_type=row.get('TXZ01'),

                    quantity=row.get('MENGE'),

                    normalized_quantity=normalized_quantity,

                    normalized_unit=normalized_unit,

                    calculated_emission=calculated_emission,

                    facility=row.get('WERKS'),

                    supplier=row.get('NAME1'),

                    activity_date=activity_date

                )
                validate_fuel_record(fuel_esg_record)

            return Response(
                {"message": "Fuel CSV uploaded successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=400)
    

class FuelESGListAPIView(ListAPIView):

    queryset = FuelESGRecord.objects.all().order_by('-created_at')

    serializer_class = FuelESGRecordSerializer


class ProcurementUploadAPIView(APIView):

    def post(self, request):

        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():

            uploaded_csv = serializer.validated_data['file']

            source = serializer.validated_data['source']

            file_type = serializer.validated_data['file_type']

            uploaded_file = UploadedFile.objects.create(
                filename=uploaded_csv.name,
                source=source,
                file_type=file_type
            )

            df = pd.read_csv(uploaded_csv)

            for _, row in df.iterrows():

                #
                # RAW PROCUREMENT RECORD
                #

                procurement_record = ProcurementRecord.objects.create(

                    uploaded_file=uploaded_file,

                    MANDT=row.get('MANDT'),
                    EBELN=row.get('EBELN'),
                    EBELP=row.get('EBELP'),
                    AEDAT=row.get('AEDAT'),
                    KNTTP=row.get('KNTTP'),
                    ANLN1=row.get('ANLN1'),
                    TXZ01=row.get('TXZ01'),
                    MENGE=row.get('MENGE'),
                    MEINS=row.get('MEINS'),
                    NETPR=row.get('NETPR'),
                    WAERS=row.get('WAERS'),
                    WERKS=row.get('WERKS'),
                    LIFNR=row.get('LIFNR'),
                    NAME1=row.get('NAME1'),
                    MATKL=row.get('MATKL'),
                )

                #
                # UNIT NORMALIZATION
                #

                normalized_quantity, normalized_unit = (
                    normalize_unit_and_quantity(
                        row.get('MENGE'),
                        row.get('MEINS')
                    )
                )

                #
                # ESG NORMALIZED RECORD
                #
                activity_date = None

                if pd.notna(row.get('AEDAT')):
                    activity_date = pd.to_datetime(
                    row.get('AEDAT')
                ).date()
                procurement_esg_record = (
                    ProcurementESGRecord.objects.create(

                        raw_record=procurement_record,

                        procurement_category=row.get('MATKL'),

                        material_description=row.get('TXZ01'),

                        quantity=row.get('MENGE'),

                        normalized_quantity=normalized_quantity,

                        unit=normalized_unit,

                        supplier=row.get('NAME1'),

                        facility=row.get('WERKS'),

                        spend_amount=row.get('NETPR'),

                        currency=row.get('WAERS'),

                        activity_date=activity_date
                    )
                )

                #
                # VALIDATION ENGINE
                #

                validate_procurement_record(
                    procurement_esg_record
                )

            return Response(
                {
                    "message":
                    "Procurement CSV uploaded successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=400)
    

class ElectricityUploadAPIView(APIView):

    def post(self, request):

        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():

            uploaded_csv = serializer.validated_data['file']

            source = serializer.validated_data['source']

            file_type = serializer.validated_data['file_type']

            uploaded_file = UploadedFile.objects.create(
                filename=uploaded_csv.name,
                source=source,
                file_type=file_type
            )

            df = pd.read_csv(uploaded_csv)

            for _, row in df.iterrows():

                electricity_record = ElectricityRecord.objects.create(

                    uploaded_file=uploaded_file,

                    Account_No=row.get('Account_No'),

                    Facility_ID=row.get('Facility_ID'),

                    Meter_ID=row.get('Meter_ID'),

                    Register_Type=row.get('Register_Type'),

                    Billing_Start=row.get('Billing_Start'),

                    Billing_End=row.get('Billing_End'),

                    Previous_Reading=row.get('Previous_Reading'),

                    Current_Reading=row.get('Current_Reading'),

                    Multiplier=row.get('Multiplier'),

                    kWh_Usage=row.get('kWh_Usage'),

                    Tariff_Code=row.get('Tariff_Code'),

                    Rate_Per_kWh=row.get('Rate_Per_kWh'),

                    Fixed_Charge=row.get('Fixed_Charge'),

                    Tax_Amount=row.get('Tax_Amount'),

                    Total_Amount=row.get('Total_Amount'),

                    Currency=row.get('Currency')
                )

                billing_start = None

                if pd.notna(row.get('Billing_Start')):
                    billing_start = pd.to_datetime(
                    row.get('Billing_Start')
                ).date()
                electricity_esg_record = ElectricityESGRecord.objects.create(

                    raw_record=electricity_record,

                    facility=row.get('Facility_ID'),

                    account_number=row.get('Account_No'),

                    meter_id=row.get('Meter_ID'),

                    register_type=row.get('Register_Type'),

                    electricity_usage=row.get('kWh_Usage'),

                    normalized_unit='kWh',

                    previous_reading=row.get('Previous_Reading'),

                    current_reading=row.get('Current_Reading'),

                    multiplier=row.get('Multiplier'),

                    tariff_code=row.get('Tariff_Code'),

                    rate_per_kwh=row.get('Rate_Per_kWh'),

                    total_amount=row.get('Total_Amount'),

                    currency=row.get('Currency'),

                    billing_start=billing_start,

                    billing_end=row.get('Billing_End')
                )

                validate_electricity_record(
                    electricity_esg_record
                )

            return Response(
                {
                    "message":
                    "Electricity CSV uploaded successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class ElectricityESGListAPIView(ListAPIView):

    queryset = ElectricityESGRecord.objects.all()

    serializer_class = ElectricityESGSerializer


class ProcurementESGListAPIView(generics.ListAPIView):

    queryset = ProcurementESGRecord.objects.all().order_by('-created_at')

    serializer_class = ProcurementESGRecordSerializer


class ESGDashboardAPIView(APIView):

    def get(self, request):

        fuel_total = (

            FuelESGRecord.objects.aggregate(

                total=Sum('calculated_emission')

            )['total'] or 0

        )

        electricity_total = (

            ElectricityESGRecord.objects.aggregate(

                total=Sum('calculated_emission')

            )['total'] or 0

        )

        procurement_total = (

            ProcurementESGRecord.objects.aggregate(

                total=Sum('calculated_emission')

            )['total'] or 0

        )

        travel_emission = (
            TravelESGRecord.objects.aggregate(
            total=Sum('calculated_emission')
            )['total'] or 0
        )

        total_emission = (

            fuel_total

            + electricity_total

            + procurement_total

            + travel_emission
        )

        failed_issues = ValidationIssue.objects.filter(

            severity='FAILED'

        ).count()

        warning_issues = ValidationIssue.objects.filter(

            severity='WARNING'

        ).count()

        suspicious_issues = ValidationIssue.objects.filter(

            severity='SUSPICIOUS'

        ).count()

        return Response({

            'total_emission': total_emission,

            'fuel_emission': fuel_total,

            'electricity_emission': electricity_total,

            'procurement_emission': procurement_total,

            'travel_emission': travel_emission,

            'scope_1': fuel_total,

            'scope_2': electricity_total,

            'scope_3': procurement_total,

            'failed_issues': failed_issues,

            'warning_issues': warning_issues,

            'suspicious_issues': suspicious_issues

        })
    

class MonthlyEmissionAPIView(APIView):

    def get(self, request):

        fuel_data = (
            FuelESGRecord.objects
            .annotate(month=TruncMonth('activity_date'))
            .values('month')
            .annotate(
                total_emission=Sum('calculated_emission')
            )
            .order_by('month')
        )

        electricity_data = (

            ElectricityESGRecord.objects

            .annotate(month=TruncMonth('billing_start'))

            .values('month')

            .annotate(

                total_emission=Sum('calculated_emission')

            )

            .order_by('month')

        )

        return Response({
            "fuel_emissions": fuel_data,
            "electricity_emissions": electricity_data
        })
    

class ValidationInsightsAPIView(APIView):

    def get(self, request):

        warnings = ValidationIssue.objects.filter(
            severity='WARNING'
        )

        suspicious = ValidationIssue.objects.filter(
            severity='SUSPICIOUS'
        )

        failed = ValidationIssue.objects.filter(
            severity='FAILED'
        )

        return Response({

            "total_warnings": warnings.count(),

            "total_suspicious": suspicious.count(),

            "total_failed": failed.count(),

            "warnings": [
                {
                    "severity": issue.severity,
                    "message": issue.issue_text,
                    "record_id": issue.object_id,
                    "created_at": issue.created_at
                }
                for issue in warnings
            ],

            "suspicious": [
                {
                    "severity": issue.severity,
                    "message": issue.issue_text,
                    "record_id": issue.object_id,
                    "created_at": issue.created_at
                }
                for issue in suspicious
            ],

            "failed": [
                {
                    "severity": issue.severity,
                    "message": issue.issue_text,
                    "record_id": issue.object_id,
                    "created_at": issue.created_at
                }
                for issue in failed
            ]
        })
    



class TravelImportAPIView(APIView):

    def post(self, request):

        api_url = "YOUR_BOOKINGS_API_URL"

        response = requests.get(api_url)

        data = response.json()

        bookings = data.get('data', [])

        for item in bookings:

            travel_booking = TravelBooking.objects.create(

                booking_id=item.get('bookingId'),

                trip_id=item.get('tripId'),

                booking_status=item.get('bookingStatus'),

                amount=item.get('amount'),

                currency=item.get('currency'),

                imported_at=item.get('importedAt'),

                raw_payload=item
            )

            activity_date = None

            if item.get('importedAt'):

                activity_date = pd.to_datetime(
                    item.get('importedAt')
                ).date()

            emission = calculate_travel_emission(
                item.get('amount')
            )

            travel_esg_record = (
                TravelESGRecord.objects.create(

                    raw_record=travel_booking,

                    amount=item.get('amount'),

                    currency=item.get('currency'),

                    calculated_emission=emission,

                    activity_date=activity_date
                )
            )

            validate_travel_record(
                travel_esg_record
            )

        return Response({
            "message": "Travel bookings imported successfully"
        })