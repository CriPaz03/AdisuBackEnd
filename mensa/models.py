from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Allergen(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome Allergene", unique=True)

    def __str__(self):
        return self.name

class Meal(models.Model):
    class TypeMeal(models.TextChoices):
        first = "first", "Primo"
        second = "second", "Secondo"
        sweet = "sweet", "Dolce"


    name = models.CharField(max_length=255, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrizione")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Prezzo", null=True, blank=True)
    type = models.CharField(choices=TypeMeal.choices, max_length=255, verbose_name="Tipo di pranzo", null=True, blank=True)
    allergens = models.ManyToManyField(Allergen, verbose_name="Allergeni", blank=True)

    def __str__(self):
        return f"{self.name} - {self.price} ({self.get_type_display()})"


class Canteen(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    address = models.CharField(max_length=255, verbose_name="Indirizzo")
    city = models.CharField(max_length=255, verbose_name="Città")
    postal_code = models.IntegerField(verbose_name="Cap")
    province = models.CharField(max_length=255, verbose_name="Provincia")

    def __str__(self):
        return f"{self.name} {self.address} {self.city}"

    @property
    def get_average_rating(self):
        ratings = Rating.objects.filter(canteen=self)
        count_ratings = ratings.count()
        if count_ratings > 0:
            nominatore = 0
            for rating in ratings:
                nominatore += rating.scale
            nominatore = nominatore if nominatore > 0 else 0
            return round(nominatore / count_ratings, 1)
        return 0
class DailyMeal(models.Model):
    available = models.BooleanField(default=True, verbose_name="Pranzo disponibile")
    meal = models.ForeignKey("Meal", on_delete=models.CASCADE, verbose_name="Pasto")
    date = models.DateField(auto_now_add=True, verbose_name="Data")
    canteen = models.ForeignKey("Canteen", on_delete=models.CASCADE, verbose_name="Mensa", null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.meal} - {self.canteen}"

    @property
    def get_price_meal(self):
        return self.meal.price


class Rating(models.Model):
    class ScaleType(models.IntegerChoices):
        one = 1, "Uno"
        two = 2, "Due"
        three = 3, "Tre"
        four = 4, "Quattro"
        five = 5, "Cinque"

    scale = models.IntegerField(choices=ScaleType.choices, default=ScaleType.one)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utente", null=True, blank=True)
    meal = models.ForeignKey("Meal", on_delete=models.CASCADE, verbose_name="Pasto")
    canteen = models.ForeignKey("Canteen", on_delete=models.CASCADE, verbose_name="Mensa")


class Booking(models.Model):
    class StatusBooking(models.TextChoices):
        created = "created", "Creato"
        confirmed = "confirmed", ""
        in_progress = "in_progress", "In corso"
        complete = "finished", "Completo"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=datetime.now)
    collection_date = models.DateTimeField(default=datetime.now, verbose_name="Data ritiro")
    status = models.CharField(choices=StatusBooking.choices, max_length=255, verbose_name="Stato", default=StatusBooking.created)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Prezzo", null=True, blank=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prezzo Totale", null=True, blank=True)
    canteen = models.ForeignKey("Canteen", on_delete=models.CASCADE, verbose_name="Mensa", null=True, blank=True)

    def update_total_price(self):
        total = sum(item.price for item in self.items.all())
        self.total_price = total
        self.save()

class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, related_name='items', on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Prezzo", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.price and self.meal:
            self.price = self.meal.price * self.quantity
        super().save(*args, **kwargs)
