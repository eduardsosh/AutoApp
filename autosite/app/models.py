from django.db import models

# Create your models here.


class Car(models.Model):
    Make = models.CharField(max_length=50)
    Model = models.CharField(max_length=50)
    Year = models.IntegerField()
    Fuel = models.CharField(max_length=50)
    Engine_cc = models.IntegerField()
    Gearbox = models.CharField(max_length=50)
    Color = models.CharField(max_length=50)
    
class Listing(models.Model):
    Car = models.ForeignKey(Car, on_delete=models.CASCADE)
    Price = models.IntegerField()
    Mileage = models.IntegerField()
    Location = models.CharField(max_length=50)
    Description = models.TextField()
    Date = models.DateTimeField(auto_now_add=True)
    Phone = models.CharField(max_length=50)
    Email = models.CharField(max_length=50)
    Name = models.CharField(max_length=50)
    
class Image(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing_images/')
    
