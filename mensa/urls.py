from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mensa.views import MealViewSet, DailyMealViewSet, CanteenViewSet, BookingViewSet, RatingViewSet

router = DefaultRouter()
router.register('meals', MealViewSet)
router.register('daily_meals', DailyMealViewSet)
router.register('canteen', CanteenViewSet)
router.register('booking', BookingViewSet)
router.register('rating', RatingViewSet)

urlpatterns = [
    path('', include(router.urls))
]
