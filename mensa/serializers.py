from rest_framework import serializers
from .models import Meal, Booking, Canteen, DailyMeal


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'
from rest_framework import serializers

class DailyMealSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='meal.type', read_only=True)
    description = serializers.CharField(source='meal.description', read_only=True)
    price = serializers.CharField(source='meal.price', read_only=True)
    name = serializers.CharField(source='meal.name', read_only=True)

    class Meta:
        model = DailyMeal
        fields = '__all__'  # Include tutti i campi di DailyMeal
        extra_fields = ['meal_type']  # Include il campo personalizzato


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
class CanteenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canteen
        fields = '__all__'