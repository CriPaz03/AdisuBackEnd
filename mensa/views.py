from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Meal, Booking, Canteen
from .serializers import MealSerializer, BookingSerializer, CanteenSerializer
from rest_framework.permissions import IsAuthenticated

class MealViewSet(ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

class CanteenSerializer(ModelViewSet):
    queryset = Canteen.objects.all()
    serializer_class = CanteenSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

