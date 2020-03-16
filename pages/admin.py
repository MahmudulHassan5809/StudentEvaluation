from django.contrib import admin
from .models import SliderImage

# Register your models here.


class SliderImageAdmin(admin.ModelAdmin):
    list_display = ["slider_title", "slider_description",
                    "slider_image"]
    search_fields = ["slider_title", "slider_description"]
    list_per_page = 20


admin.site.register(SliderImage, SliderImageAdmin)
