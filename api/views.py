import os
import requests

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache

FIRST_API_KEY = os.getenv("FIRST_API_KEY")
FIRST_API_URL = os.getenv("FIRST_API_URL")
SECOND_API_URL = os.getenv("SECOND_API_URL")


@api_view(["GET"])
def first_api(request):
    word = request.GET.get("word")
    if not word:
        return Response(
            {"error": "Word parameter is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    cache_key = word
    cached_response = cache.get(cache_key)
    if cached_response:
        return Response(cached_response, status=status.HTTP_200_OK)
    api_url = f"{FIRST_API_URL}?word={word}"
    response = requests.get(
        api_url,
        headers={"X-Api-Key": FIRST_API_KEY},
        verify=False,
    )

    if response.status_code == requests.codes.ok:
        try:
            content = response.json()
            cache.set(word, content)
            return Response(content, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid JSON response from API."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return Response(
            {
                "error": f"Error from external API: {response.status_code}",
                "details": response.text,
            },
            status=status.HTTP_502_BAD_GATEWAY,
        )


@api_view(["GET"])
def second_api(request):
    response = requests.get(
        SECOND_API_URL,
        headers={"X-Api-Key": FIRST_API_KEY},
    )
    if response.status_code == requests.codes.ok:
        try:
            content = response.json()
            return Response(content, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid JSON response from API."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return Response(
            {
                "error": f"Error from external API: {response.status_code}",
                "details": response.text,
            },
            status=status.HTTP_502_BAD_GATEWAY,
        )