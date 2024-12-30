from rest_framework.viewsets import ModelViewSet
from .models import Meal, Booking
from .serializers import MealSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated

class MealViewSet(ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

