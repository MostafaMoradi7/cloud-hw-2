from django.urls import path
from .views import first_api, second_api

urlpatterns = [
    path("first/", first_api),
    path("second/", second_api,)
]
