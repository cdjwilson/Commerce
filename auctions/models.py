from email.policy import default
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", default=0, null=False)
    title = models.CharField(max_length=100, null=False)
    price = models.IntegerField(null=False)
    image = models.ImageField(upload_to="images/", null=False)
    description = models.CharField(max_length=500, null=False)
    date = models.DateTimeField(auto_now=True, null=False)
    highest_bid = models.ForeignKey("Bid", on_delete=models.SET_NULL, null=True)
    category = models.CharField(max_length=50, null=True)
    ended = models.BooleanField(default=False)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", null=False)
    listingBid = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    bid = models.IntegerField(null=False)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=False, default=0)
    listingComment = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=500, null=False, default="")

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists", null=False, default=0)
    listingWatchlist = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)