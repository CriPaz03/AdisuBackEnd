from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mensa.views import MealViewSet, BookingViewSet, UserViewSet

router = DefaultRouter()
router.register('meals', MealViewSet)
router.register('bookings', BookingViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]