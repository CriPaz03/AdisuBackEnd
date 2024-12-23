from rest_framework.viewsets import ModelViewSet
from .models import Meal, Booking, User
from .serializers import MealSerializer, BookingSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class MealViewSet(ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
