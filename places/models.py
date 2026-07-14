from django.db import models


class Place(models.Model):
    title = models.CharField("Название", max_length=200)
    description_short = models.TextField("Краткое описание")
    description_long = models.TextField("Полное описание")
    lng = models.FloatField("Долгота")
    lat = models.FloatField("Широта")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self) -> str:
        return self.title

    def to_feature(self) -> dict:
        from django.urls import reverse

        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.lng, self.lat],
            },
            "properties": {
                "title": self.title,
                "placeId": self.pk,
                "detailsUrl": reverse("place_detail", args=[self.pk]),
            },
        }


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Место",
    )
    image = models.ImageField("Изображение", upload_to="places_images")
    ordering = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["ordering"]
        verbose_name = "Изображение места"
        verbose_name_plural = "Изображение мест"

    def __str__(self) -> str:
        return f"{self.place.title} - картинка {self.ordering}"
