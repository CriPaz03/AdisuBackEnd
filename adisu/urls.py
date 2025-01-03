from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mensa.views import MealViewSet, BookingViewSet, CanteenSerializer
from borsa.views import AcademicYearViewSet, IseeRangeViewSet, ScholarshipViewSet, RequestViewSet
from django.contrib import admin

router = DefaultRouter()
router.register('meals', MealViewSet)
router.register('bookings', BookingViewSet)
router.register('canteen', CanteenSerializer)
router.register('academicyear', AcademicYearViewSet)
router.register('iseerange', IseeRangeViewSet)
router.register('scholarship', ScholarshipViewSet)
router.register('request', RequestViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("api/", include('user.urls')),
]
