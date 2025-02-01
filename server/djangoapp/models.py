from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib import admin

# Create your models here.


# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)  # Car make name
    description = models.TextField()  # Description of the car make

    created_at = models.DateTimeField(
        default=now, editable=False
    )  # Timestamp for creation

    def __str__(self):
        return self.name  # String representation


# Car Model model
class CarModel(models.Model):
    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name='models'
    )
    name = models.CharField(max_length=100)  # Car model name
    dealer_id = models.IntegerField()  # Reference to dealer in Cloudant database

    # Choices for car type
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('TRUCK', 'Truck'),
        ('COUPE', 'Coupe'),
    ]
    type = models.CharField(
        max_length=10,
        choices=CAR_TYPES,
        default='SUV'
    )  # Car type

    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2023)
        ],
        default=2023
    )  # Year of the car model

    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.type})"


admin.site.register(CarMake)
admin.site.register(CarModel)
