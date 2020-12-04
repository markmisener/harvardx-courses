from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django import forms


class Bid(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    item = models.ForeignKey("Listing", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey("Listing", on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()

    def __str__(self):
        return f"{self.id}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    starting_bid = models.DecimalField(
        max_digits=20, decimal_places=2, validators=[MinValueValidator(0)]
    )
    image_url = models.CharField(max_length=250, blank=True)

    class Category(models.TextChoices):
        CLOTHING_AND_ACCESSORIES = "Clothing and Accessories"
        ELECTRONICS_AND_GAMES = "Electronics and Games"
        OTHER = "Other"
        _ = None

    category = models.CharField(
        max_length=30, choices=Category.choices, default=Category._, blank=True,
    )
    short_description = models.CharField(max_length=25, blank=True,)
    current_price = models.DecimalField(
        max_digits=20, decimal_places=2, validators=[MinValueValidator(0)]
    )
    highest_bid = models.ForeignKey(
        "Bid", on_delete=models.CASCADE, blank=True, null=True
    )
    bids = models.ManyToManyField("Bid", blank=True, related_name="bids")
    comments = models.ManyToManyField("Post", blank=True, related_name="comments")
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, blank=True, null=True, related_name="poster"
    )
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="winning_user",
    )

    def __str__(self):
        return f"{self.title}"


class User(AbstractUser):
    listings = models.ManyToManyField("Listing", blank=True, related_name="listings")
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watching")
    bids = models.ManyToManyField("Bid", blank=True, related_name="bid_history")
    comments = models.ManyToManyField(
        "Post", blank=True, related_name="comment_history"
    )
