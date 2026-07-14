from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html
from django import forms
from tinymce.widgets import TinyMCE
from .models import Place, PlaceImage


def image_preview(obj):
    if obj.image:
        return format_html(
            '<img src="{}" style="max-height: 200px; max-width: 100%;" />',
            obj.image.url,
        )
    return "-"


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    extra = 1
    readonly_fields = ["image_preview"]

    @admin.display(description="Превью")
    def image_preview(self, obj):
        return image_preview(obj)


class PlaceAdminForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"
        widgets = {
            "description_long": TinyMCE(),
        }


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    form = PlaceAdminForm
    inlines = [PlaceImageInline]
