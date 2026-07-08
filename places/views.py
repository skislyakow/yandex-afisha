import json
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Place


def start(request):
    places = Place.objects.all()

    features = []
    for place in places:
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [place.lng, place.lat],
                },
                "properties": {
                    "title": place.title,
                    "placeId": place.pk,
                    "detailsUrl": f"/places/{place.pk}",
                },
            }
        )

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    return render(request, "index.html", {"places_geojson": geojson})


def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    images = place.images.all()

    data = {
        "title": place.title,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "imgs": [image.image.url for image in images],
    }

    return JsonResponse(data)
