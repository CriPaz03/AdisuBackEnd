from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mensa.views import MealViewSet, BookingViewSet, CanteenViewSet, DailyMealViewSet
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/', include('user.urls')),
                  path('api/', include('mensa.urls')),
                  path('gestionale/', include('gestionale.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
