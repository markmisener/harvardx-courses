from django.contrib import admin
from .models import Bid, Listing, Post, User


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "item")


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "item", "text")


class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "user",
        "category",
        "starting_bid",
        "current_price",
        "highest_bid",
        "active",
        "winner",
    )
    filter_horizontal = ("bids",)


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")
    filter_horizontal = ("watchlist", "bids", "comments")


admin.site.register(Bid, BidAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)
