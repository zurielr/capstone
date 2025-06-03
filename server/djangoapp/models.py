# Uncomment the following imports before adding the Model code
from django.db import models
# from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Add other fields as needed

    def __str__(self):
        return self.name  # Return the name as the string representation

class Dealer(models.Model):
    full_name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=20)
    state = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Many-to-One relationship
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices as required
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')
    body_type = models.CharField(max_length=50, default='Unknown')
    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )
    mileage = models.IntegerField()
    # Add other fields as needed

    def __str__(self):
        return f"{self.car_make.name} {self.name}"



class Review(models.Model):
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, null=True, blank=True)
    dealership = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    sentiment = models.CharField(max_length=20, default='neutral')  # Sentiment analysis result

    def __str__(self):
        return f"Review by {self.name} for {self.car.name}"

