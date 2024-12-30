from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mensa.views import MealViewSet, BookingViewSet
from django.contrib import admin

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register('meals', MealViewSet)
router.register('bookings', BookingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("api/", include('user.urls')),
]
