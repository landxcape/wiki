from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("results", views.results, name="results"),
    path("new_page", views.new_page, name="new_page"),
    path("create_new_page", views.create_new_page, name="create_new_page")
]
