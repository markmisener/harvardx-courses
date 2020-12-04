from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/<str:category>", views.index, name="index"),
    path("bid/<str:listing_id>", views.bid, name="bid"),
    path("close/<str:listing_id>", views.close_listing, name="close"),
    path("comment/<str:listing_id>", views.comment, name="comment"),
    path("create-listing", views.create_listing, name="create-listing"),
    path("listing/<str:listing_id>", views.listing_view, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<str:listing_id>", views.manage_watchlist, name="manage_watchlist"),
    path("people/<str:username>", views.user_view, name="user"),
]
