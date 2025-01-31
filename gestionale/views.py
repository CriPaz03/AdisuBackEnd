from django.shortcuts import render
from django.views.generic import ListView

from gestionale.table import BookingTable, MealTable
from mensa.models import Booking, Meal


class BookingListView(ListView):
    model = Booking
    table_class = BookingTable
    template_name = 'booking.html'
    paginate_by = 10


class MealListView(ListView):
    model = Meal
    table_class = MealTable
    template_name = "meal.html"