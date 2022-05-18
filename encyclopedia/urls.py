from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.article, name="article"),
    path("wiki/", views.search, name="search"),
    path("wiki/newpage/", views.newpage, name="newpage"),
    path("wiki/edit/", views.edit, name="edit"),
    path("wiki/editpage/", views.editpage, name="editpage"),
    path("wiki/random/", views.random, name="random")
]
