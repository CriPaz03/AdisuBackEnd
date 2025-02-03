from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Meal, Booking, Canteen, DailyMeal, Rating
from .serializers import MealSerializer, BookingSerializer, CanteenSerializer, DailyMealSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
class MealViewSet(ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]


class DailyMealViewSet(ModelViewSet):
    queryset = DailyMeal.objects.all()
    serializer_class = DailyMealSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=True, methods=['GET'])
    def get_meals_by_id(self, request, pk=None):
        meals = self.queryset.filter(canteen_id=pk, available=True)
        serialized_meals = self.serializer_class(meals, many=True)
        return Response(serialized_meals.data)

    @action(methods=['POST'], detail=False)
    def check_meal_available(self, request):
        ids = request.data['ids']
        daily_meals = DailyMeal.objects.filter(id__in=ids, available=False)
        serialized_daily_meals = self.serializer_class(daily_meals, many=True)
        return Response(serialized_daily_meals.data)


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=True, methods=['GET'])
    def get_created(self, request, pk=None):
        return Response({'booking': Booking.objects.filter(status=Booking.StatusBooking.created)})

class CanteenViewSet(ModelViewSet):
    queryset = Canteen.objects.all()
    serializer_class = CanteenSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != Booking.StatusBooking.created:
            return Response({'error': 'Non puoi eliminare questo ordine'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)