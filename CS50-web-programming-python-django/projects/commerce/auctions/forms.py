from django.forms import ModelForm
from .models import Bid, Listing, Post


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "category", "image_url"]


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["text"]
