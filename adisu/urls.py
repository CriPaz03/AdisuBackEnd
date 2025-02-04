from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mensa.views import MealViewSet, BookingViewSet, CanteenViewSet, DailyMealViewSet
from borsa.views import AcademicYearViewSet, IseeRangeViewSet, ScholarshipViewSet, RequestViewSet
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

router = DefaultRouter()
router.register('academicyear', AcademicYearViewSet)
router.register('iseerange', IseeRangeViewSet)
router.register('scholarship', ScholarshipViewSet)
router.register('request', RequestViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/', include(router.urls)),
                  path('api/', include('user.urls')),
                  path('api/', include('mensa.urls')),
                  path('gestionale/', include('gestionale.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
