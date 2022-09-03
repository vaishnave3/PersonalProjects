from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.display, name="display2"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("save", views.save, name="save"),
    path("wiki/edit/<str:entry>/", views.edit, name="edit"),
    path("randompage", views.randompage, name="randompage"),
    path("saveedit/<str:edit_title>", views.saveedit, name="saveedit")
]
