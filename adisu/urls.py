from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mensa.views import MealViewSet, BookingViewSet, CanteenSerializer
from django.contrib import admin

router = DefaultRouter()
router.register('meals', MealViewSet)
router.register('bookings', BookingViewSet)
router.register('canteen', CanteenSerializer)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("api/", include('user.urls')),
]
