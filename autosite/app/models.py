from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
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
    Link = models.CharField(max_length=256)
    User = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    
    def get_absolute_url(self):
        return reverse('listing_detail', args=[str(self.id)])
    
class Image(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing_images/')

    def delete(self, *args, **kwargs):
        print("Deleting image:", self.image.path)
        storage, path = self.image.storage, self.image.path
        super(Image, self).delete(*args, **kwargs)
        storage.delete(path)

    
class Bookmark(models.Model):   # new model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'listing')