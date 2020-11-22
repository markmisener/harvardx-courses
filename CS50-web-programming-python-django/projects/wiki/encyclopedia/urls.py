from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.display_entry, name="display_entry"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("add", views.add, name="add"),
    path("random_entry", views.random_entry, name="random"),
]
