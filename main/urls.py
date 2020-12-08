from django.urls import path

from .views import *


urlpatterns = [
    path('', index, name="index"),
    path('register', register, name="register"),
    path('new-post', post, name="post"),
    path('edit/<pk>', edit, name="edit"),
    path('delete_postNr<abc>', delete, name="delete"),

]