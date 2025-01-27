from rest_framework import serializers
from .models import Meal, Booking, Canteen, DailyMeal, Allergen

class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = '__all__'

class MealSerializer(serializers.ModelSerializer):
    allergens = AllergenSerializer(many=True, read_only=True)
    class Meta:
        model = Meal
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
class CanteenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canteen
        fields = '__all__'

class DailyMealSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='meal.type', read_only=True)
    description = serializers.CharField(source='meal.description', read_only=True)
    price = serializers.CharField(source='meal.price', read_only=True)
    name = serializers.CharField(source='meal.name', read_only=True)
    allergens = AllergenSerializer(source='meal.allergens', many=True, read_only=True)
    canteens = CanteenSerializer(many=True, read_only=True)

    class Meta:
        model = DailyMeal
        fields = '__all__'