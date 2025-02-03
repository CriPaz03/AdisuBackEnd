from datetime import datetime

from rest_framework import serializers
from .models import Meal, Booking, Canteen, DailyMeal, Allergen, BookingItem, Rating


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = '__all__'


class MealSerializer(serializers.ModelSerializer):
    allergens = AllergenSerializer(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = '__all__'


class BookingItemSerializer(serializers.ModelSerializer):
    meal_type = serializers.CharField(source='meal.type', required=False)
    class Meta:
        model = BookingItem
        fields = ['id', 'meal', 'quantity', 'price', 'meal_type']


class CanteenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canteen
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    items = BookingItemSerializer(many=True, read_only=False)
    canteen = CanteenSerializer(read_only=False, required=False)
    canteen_id = serializers.IntegerField(write_only=True, required=False)
    status = serializers.CharField(source="get_status_display", read_only=True)
    class Meta:
        model = Booking
        fields = ['id', 'booking_date', 'collection_date', 'status', 'total_price', 'items', 'canteen', 'canteen_id']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        canteen_id = validated_data.pop('canteen_id')


        booking = Booking.objects.create(user=self.context['request'].user, canteen=Canteen.objects.get(id=canteen_id),
                                         **validated_data)

        for item_data in items_data:
            daily_meal = DailyMeal.objects.filter(canteen_id=canteen_id, meal=item_data["meal"], available=True)
            if daily_meal.exists():
                BookingItem.objects.create(booking=booking, **item_data)

        booking.update_total_price()
        return booking

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if items_data is not None:
            instance.items.all().delete()

            for item_data in items_data:
                BookingItem.objects.create(booking=instance, **item_data)

            instance.update_total_price()

        instance.save()
        return instance


class CanteenSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Canteen
        fields = '__all__'

    def get_average_rating(self, obj):
        return obj.get_average_rating

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

class RatingSerializer(serializers.ModelSerializer):

    meal_id = serializers.IntegerField(source='meal.id')
    canteen_id = serializers.IntegerField(source='canteen.id')

    class Meta:
        model = Rating
        field = ["scale", "meals", "meal_id", "canteen_id"]
        exclude = ['user', 'canteen', "meal"]

    def create(self, validated_data):
        user = self.context['request'].user
        canteen_id = validated_data.pop("canteen")["id"]
        meal_id = validated_data.pop("meal")["id"]
        rating = Rating.objects.filter(user=user, canteen_id=canteen_id, meal_id=meal_id)
        if rating.exists():
            rating.update(**validated_data)
        else:
            rating = Rating.objects.create(user=user, canteen_id=canteen_id, meal_id=meal_id, **validated_data)
        return rating.last()