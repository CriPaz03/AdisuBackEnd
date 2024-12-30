from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Meal(models.Model):
    class TypeMeal(models.TextChoices):
        first = "first", "Primo"
        second = "second", "Secondo"
        sweet = "sweet", "Dolce"


    name = models.CharField(max_length=255, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrizione")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Prezzo", null=True, blank=True)
    type = models.CharField(choices=TypeMeal.choices, max_length=255, verbose_name="Tipo di pranzo", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.price} ({self.get_type_display()})"


class DailyMeal(models.Model):
    available = models.BooleanField(default=True, verbose_name="Pranzo disponibile")
    meal = models.ForeignKey("Meal", on_delete=models.CASCADE, verbose_name="Pranzo")
    date = models.DateField(auto_now_add=True, verbose_name="Data")

    @property
    def get_price_meal(self):
        return self.meal.price


class Booking(models.Model):
    class StatusBooking(models.TextChoices):
        created = "created", "Creato"
        confirmed = "confirmed", "Confermanto"
        in_progress = "in_progress", "In corso"
        complete = "finished", "Completo"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    booking_date = models.DateTimeField(default=datetime.now)
    collection_date = models.DateTimeField(default=datetime.now, verbose_name="Data ritiro")
    status = models.CharField(choices=StatusBooking.choices, max_length=255, verbose_name="Stato", default=StatusBooking.created)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Prezzo", null=True, blank=True)


class Canteen(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    address = models.CharField(max_length=255, verbose_name="Indirizzo")
    city = models.CharField(max_length=255, verbose_name="Città")
    postal_code = models.IntegerField(verbose_name="Postal", validators=[MinValueValidator(1), MaxValueValidator(5)])
    province = models.CharField(max_length=255, verbose_name="Provincia")
