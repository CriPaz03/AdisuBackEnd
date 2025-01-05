from django.db.models import F
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Meal, Booking, Canteen, DailyMeal
from .serializers import MealSerializer, BookingSerializer, CanteenSerializer, DailyMealSerializer
from rest_framework.permissions import IsAuthenticated

class MealViewSet(ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

from rest_framework.decorators import action
from rest_framework.response import Response

class DailyMealViewSet(ModelViewSet):
    queryset = DailyMeal.objects.all()
    serializer_class = DailyMealSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=True, methods=['GET'])
    def get_meals_by_id(self, request, pk=None):
        meals = self.queryset.filter(canteen_id=pk)
        serialized_meals = self.serializer_class(meals, many=True)
        return Response(serialized_meals.data)


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=True, methods=['GET'])
    def get_created(self, request, pk=None):
        return Response({'booking': Booking.objects.filter(status=Booking.StatusBooking.created)})

class CanteenSerializer(ModelViewSet):
    queryset = Canteen.objects.all()
    serializer_class = CanteenSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

