import json
from typing import Any

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandParser

from places.models import Place, PlaceImage


def normalize_url(url: str) -> str:
    if "github.com" in url and "/blob/" in url:
        url = url.replace("github.com", "raw.githubusercontent.com", 1)
        url = url.replace("/blob/", "/", 1)
    return url


class Command(BaseCommand):
    help = "load a place from JSON file URL"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("url", help="URL to the JSON file with place data")

    def handle(self, *args: Any, **options: Any) -> str | None:
        url = normalize_url(options["url"])

        try:
            response = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Failed to download {url}: {e}"))
            return
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f"Invalid JSON from {url}: {e}"))
            return

        place, created = Place.objects.get_or_create(
            title=data["title"],
            defaults={
                "description_short": data.get("description_short", ""),
                "description_long": data.get("description_long", ""),
                "lng": float(data["coordinates"]["lng"]),
                "lat": float(data["coordinates"]["lat"]),
            },
        )

        if not created:
            place.description_short = data.get("description_short", "")
            place.description_long = data.get("description_long", "")
            place.lng = float(data["coordinates"]["lng"])
            place.lat = float(data["coordinates"]["lat"])
            place.save()

        place.images.all().delete()
        successful_images = 0
        for order, img_url in enumerate(data.get("imgs", [])):
            try:
                img_response = requests.get(img_url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
                img_response.raise_for_status()
            except requests.RequestException as e:
                self.stderr.write(self.style.WARNING(f"Failed to download image {img_url}: {e}"))
                continue

            image_content = ContentFile(
                img_response.content,
                name=img_url.split("/")[-1],
            )

            PlaceImage.objects.create(
                place=place,
                image=image_content,
                ordering=order,
            )
            successful_images += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Place "{place.title}" loaded with {successful_images} images'
            )
        )
