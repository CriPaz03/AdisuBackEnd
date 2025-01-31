import django_tables2 as tables
from mensa.models import Booking, Meal


class BookingTable(tables.Table):
    class Meta:
        model = Booking

class MealTable(tables.Table):
    class Meta:
        model = Meal