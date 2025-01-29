from django.contrib import admin

from mensa.models import Canteen, Meal, DailyMeal, Allergen, Booking

# Register your models here.
admin.site.register(Canteen)
admin.site.register(Meal)
admin.site.register(DailyMeal)
admin.site.register(Allergen)
admin.site.register(Booking)