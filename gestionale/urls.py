from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import TemplateView

from gestionale.views import BookingListView, MealListView

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='index.html')), name='index'),
    path('meal/', login_required(MealListView.as_view()), name='meal'),
    path('cuoco/', login_required(TemplateView.as_view(template_name='cuoco.html')), name='cuoco'),
    path('booking/', login_required(BookingListView.as_view()), name='booking'),

    path("accounts/", include("django.contrib.auth.urls")),
]
