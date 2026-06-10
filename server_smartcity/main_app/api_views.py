from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly 

class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    pagination_class = ReportPagination

    def get_permissions(self):
        return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]

    def perform_create(self, serializer):
        requested_status = serializer.validated_data.get(
            'status',
            Report.Status.DRAFT,
        )
        serializer.save(
            reporter=self.request.user,
            status=requested_status,
        )

    def get_queryset(self):
        user = self.request.user
        queryset = Report.objects.visible_to(user).order_by('-updated_at')

        if self.action == 'list':
            tab = self.request.query_params.get('tab', 'feed')

            if user.is_admin:
                return queryset

            if tab == 'my_reports':
                return queryset.filter(reporter=user)

            if tab == 'feed':
                return queryset.exclude(
                    status=Report.Status.DRAFT
                ).exclude(reporter=user)

        return queryset
