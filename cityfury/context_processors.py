from .models import *

def main(request):
    context = {
        'cities': City.objects.all(),
        'categories': Category.objects.all()
    }
    return context

