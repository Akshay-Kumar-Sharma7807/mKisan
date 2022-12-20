from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    number = PhoneNumberField(null=False, blank=False, unique=True)
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    starting_bid = models.IntegerField()
    img = models.CharField(max_length=800, blank=True)
    CategoryType = models.TextChoices('CategoryType', 'Fashion Toys Electronics Home')
    category = models.CharField(blank=True, choices=CategoryType.choices, max_length=60)
    publication_date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)



    
    def __str__(self):
        return f"{self.title} with starting bid of {self.starting_bid}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)
    bid_price = models.DecimalField(max_digits=11, decimal_places=2)
    

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)


class WatchList(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
