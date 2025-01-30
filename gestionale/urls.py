from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='index.html')), name='index'),
    path("accounts/", include("django.contrib.auth.urls")),
]
