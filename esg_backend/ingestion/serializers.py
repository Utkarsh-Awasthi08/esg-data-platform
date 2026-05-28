from rest_framework import serializers
from .models import ElectricityESGRecord, FuelESGRecord, ValidationIssue
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):

    file = serializers.FileField()

    source = serializers.CharField()

    file_type = serializers.CharField()


class ValidationIssueSerializer(serializers.ModelSerializer):

    class Meta:

        model = ValidationIssue

        fields = '__all__'

class FuelESGRecordSerializer(serializers.ModelSerializer):

    issues = serializers.SerializerMethodField()

    class Meta:

        model = FuelESGRecord

        fields = [

            'id',

            'fuel_type',

            'quantity',

            'normalized_quantity',

            'normalized_unit',

            'facility',

            'supplier',

            'status',

            'issues'

        ]

    def get_issues(self, obj):

        issues = ValidationIssue.objects.filter(

            object_id=obj.id

        )

        return ValidationIssueSerializer(

            issues,

            many=True

        ).data
    

class ElectricityESGSerializer(serializers.ModelSerializer):

    issues = serializers.SerializerMethodField()

    class Meta:

        model = ElectricityESGRecord

        fields = '__all__'

    def get_issues(self, obj):

        content_type = ContentType.objects.get_for_model(obj)

        issues = ValidationIssue.objects.filter(
            content_type=content_type,
            object_id=obj.id
        )

        return ValidationIssueSerializer(
            issues,
            many=True
        ).data
    

from .models import ProcurementESGRecord


class ProcurementESGRecordSerializer(serializers.ModelSerializer):

    issues = serializers.SerializerMethodField()

    class Meta:

        model = ProcurementESGRecord

        fields = '__all__'

    def get_issues(self, obj):

        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(obj)

        issues = ValidationIssue.objects.filter(
            content_type=content_type,
            object_id=obj.id
        )

        return ValidationIssueSerializer(issues, many=True).data