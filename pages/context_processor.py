from pages.models import SliderImage


def slider(request):
    all_slider = SliderImage.objects.all()

    return {'all_slider': all_slider}
