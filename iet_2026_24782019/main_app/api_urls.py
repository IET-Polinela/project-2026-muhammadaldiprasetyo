from rest_framework.routers import DefaultRouter
from .api_views import ReportViewSet

# Router otomatis membuat rute URL [cite: 17, 18, 103]
router = DefaultRouter()
router.register(r'report', ReportViewSet, basename='report') [cite: 104]

urlpatterns = router.urls [cite: 105]