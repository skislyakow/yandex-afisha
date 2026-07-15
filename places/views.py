from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Place


def start(request):
    places = Place.objects.all()

    geojson = {
        "type": "FeatureCollection",
        "features": [place.to_feature() for place in places],
    }

    return render(request, "index.html", {"places_geojson": geojson})


def place_detail(request, pk):
    place = get_object_or_404(
        Place.objects.prefetch_related("images"),
        pk=pk,
    )
    images = place.images.all()

    serialized_place = {
        "title": place.title,
        "imgs": [image.image.url for image in images],
        "short_description": place.short_description,
        "long_description": place.long_description,
        "coordinates": {
            "lng": str(place.lng),
            "lat": str(place.lat),
        },
    }

    return JsonResponse(
        serialized_place,
        json_dumps_params={
            "ensure_ascii": False,
            "indent": 4,
        },
    )
