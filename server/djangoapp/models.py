# Uncomment the following imports before adding the Model code

# from django.db import models
# from django.utils.timezone import now
# from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

# Uncomment the following imports before adding the Model code
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)  # Car make name
    description = models.TextField()  # Description of the car make
    # Additional fields as needed
    created_at = models.DateTimeField(default=now, editable=False)  # Timestamp for creation

    def __str__(self):
        return self.name  # String representation of the CarMake object

# Car Model model
class CarModel(models.Model):
    # Establish a Many-to-One relationship with CarMake
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')  
    name = models.CharField(max_length=100)  # Car model name
    dealer_id = models.IntegerField()  # Reference to dealer in Cloudant database

    # Choices for car type
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('TRUCK', 'Truck'),
        ('COUPE', 'Coupe'),
        # Add more car types if required
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')  # Car type
    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2023)
        ],
        default=2023
    )  # Year of the car model
    description = models.TextField(blank=True, null=True)  # Optional description of the car model

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.type})"  # String representation of the CarModel object

# Register models to the Django Admin site
from django.contrib import admin
admin.site.register(CarMake)
admin.site.register(CarModel)
