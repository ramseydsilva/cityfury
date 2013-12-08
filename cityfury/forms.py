from django import forms
from .models import Post
from django_select2.widgets import *
from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption', 'location_string',
                'city', 'area', 'category', 'description']

    def clean_area(self):
        print "In clean area!!!"

        area = self.cleaned_data['area']
        city = self.cleaned_data['city']

        try:
            city = City.objects.get(id=city)
        except:
            city = City.objects.get(name='Other')
            pass

        try:
            area = Area.objects.get(id=area)
        except:
            if not area.isdigit():
                area = Area(name=area, city=city)
                area.save()
                self.cleaned_data["area"] = area.id
            pass

        return self.cleaned_data

