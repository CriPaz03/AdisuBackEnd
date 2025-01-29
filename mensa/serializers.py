from rest_framework import serializers
from .models import Meal, Booking, Canteen, DailyMeal, Allergen, BookingItem

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
    class Meta:
        model = BookingItem
        fields = ['id', 'meal', 'quantity', 'price']

class CanteenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canteen
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    items = BookingItemSerializer(many=True, read_only=False)
    canteen = CanteenSerializer(read_only=False, required=False)
    canteen_id = serializers.IntegerField(write_only=True, required=False)


    class Meta:
        model = Booking
        fields = ['id', 'booking_date', 'collection_date', 'status', 'total_price', 'items', 'canteen', 'canteen_id']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        canteen_id = validated_data.pop('canteen_id')
        booking = Booking.objects.create(user=self.context['request'].user, canteen=Canteen.objects.get(id=canteen_id), **validated_data)

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