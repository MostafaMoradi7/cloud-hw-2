from django.urls import path
from .views import first_api

urlpatterns = [
    path("first/", first_api),
]
