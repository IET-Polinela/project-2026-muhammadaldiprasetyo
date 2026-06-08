from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'category', 'description',
            'location', 'status', 'reporter', 'is_owner',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['reporter', 'is_owner', 'created_at', 'updated_at']

    def validate_status(self, value):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            raise serializers.ValidationError("Autentikasi diperlukan.")

        if request.user.is_admin:
            expected_status = self.instance.next_workflow_status() if self.instance else None
            if value != expected_status:
                raise serializers.ValidationError(
                    "Admin hanya dapat memajukan status sesuai urutan workflow."
                )
            return value

        if value not in [Report.Status.DRAFT, Report.Status.REPORTED]:
            raise serializers.ValidationError(
                "Citizen hanya dapat menyimpan draft atau mengajukan laporan."
            )
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.user.is_admin:
            if self.instance is None:
                raise serializers.ValidationError(
                    "Admin tidak dapat membuat laporan."
                )
            if set(attrs.keys()) != {'status'}:
                raise serializers.ValidationError(
                    "Admin hanya dapat memajukan status laporan."
                )
        return attrs

    def get_reporter(self, obj):
        request = self.context.get('request')
        if obj.reporter is None:
            return "Warga Anonim"

        if not request or request.user.is_anonymous:
            return "Warga Anonim"

        if obj.reporter == request.user:
            return obj.reporter.username

        return "Warga Anonim"

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return bool(request and not request.user.is_anonymous and obj.reporter == request.user)
