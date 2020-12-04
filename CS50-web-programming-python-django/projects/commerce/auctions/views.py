from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bid, Listing, Post, User
from .forms import BidForm, ListingForm, PostForm

import sys


def index(request, category=None):
    listings = (
        Listing.objects.all()
        if not category
        else Listing.objects.filter(category=category)
    )
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image_url = form.cleaned_data["image_url"]
            if not image_url:
                image_url = "/static/auctions/imgs/generic-image-placeholder.png"
            category = form.cleaned_data["category"]

            new_listing = Listing(
                title=title,
                description=description,
                starting_bid=starting_bid,
                image_url=image_url,
                category=category,
                current_price=starting_bid,
                user=request.user,
                short_description=f"{description[:22]}...",
            )
            new_listing.save()

            request.user.listings.add(new_listing)

            return render(
                request,
                "auctions/index.html",
                {
                    "message": "Listing successfully created.",
                    "listings": Listing.objects.all(),
                },
            )
        else:
            return render(
                request,
                "auctions/create-listing.html",
                {"message": "Something went wrong.", "form": form},
            )

    return render(request, "auctions/create-listing.html", {"form": ListingForm()})


def listing_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if listing:
        return render(request, "auctions/listing.html", {"listing": listing})
    else:
        return render(
            request, "auctions/index.html", {"message": "Something went wrong."},
        )


def manage_watchlist(request, listing_id=""):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(pk=int(request.user.id))
    if listing in user.watchlist.all():
        user.watchlist.remove(listing)
    else:
        user.watchlist.add(listing)
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def watchlist(request):
    return render(request, "auctions/watchlist.html",)


def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(pk=int(request.user.id))

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]

            if listing.current_price < amount:
                bid = Bid(user=user, amount=amount, item=listing,)
                bid.save()

                user.bids.add(bid)
                user.save()

                listing.highest_bid = bid
                listing.current_price = bid.amount
                listing.bids.add(bid)
                listing.save()

                return render(
                    request,
                    "auctions/listing.html",
                    {"message": "Successful bid!", "listing": listing,},
                )
            else:
                return render(
                    request,
                    "auctions/bid.html",
                    {
                        "message": f"Unsuccessful bid. Bid amount must be higher than the current price of ${listing.current_price}.",
                        "listing": listing,
                        "form": form,
                    },
                )

        else:
            return render(
                request,
                "auctions/bid.html",
                {"listing": listing, "message": "Something went wrong.", "form": form,},
            )

    return render(request, "auctions/bid.html", {"listing": listing, "form": BidForm()})


def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(pk=int(request.user.id))

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post_text = form.cleaned_data["text"]

            comment = Post(user=user, text=post_text, item=listing,)
            comment.save()

            user.comments.add(comment)
            user.save()

            listing.comments.add(comment)
            listing.save()

            return render(request, "auctions/listing.html", {"listing": listing,},)

        else:
            return render(
                request,
                "auctions/listing.html",
                {"listing": listing, "message": "Something went wrong.", "form": form,},
            )

    return render(
        request, "auctions/comment.html", {"listing": listing, "form": PostForm()}
    )


def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.active = False
    listing.winner = listing.highest_bid.user
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def user_view(request, username):
    return render(
        request,
        "auctions/people.html",
        {"person": User.objects.filter(username=username).first()},
    )
