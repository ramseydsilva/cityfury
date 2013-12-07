from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from django.core.urlresolvers import reverse


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('city', args=["all", self.name.lower()])

class Area(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City)

    def __unicode__(self):
        return self.name

class Location(models.Model):
    string = models.CharField(max_length=1000)
    city = models.ForeignKey(City)

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=500)

def upload_to(instance, filename):
    file = filename.split('/')[-1]
    if instance.location:
        return instance.location.city.name + '/' + file
    return 'anonymous/' + file

class CommentLike(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey("Comment")
    created_date = models.DateTimeField(auto_now_add=True)

class CommentDisLike(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey("Comment")
    created_date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    post = models.ForeignKey("Post")
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_date',)

    def __unicode__(self):
        return self.comment[:50]

class DisLike(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey("Post")
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username + " - " + self.post.caption

class Post(models.Model):
    caption = models.CharField(max_length=500)
    image = ImageField(upload_to=upload_to)
    location_string = models.CharField(max_length=500, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    area = models.ForeignKey(Area, null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if not self.caption:
            return "No caption: %s" %( self.id )
        return self.caption

    def get_category_absolute_url(self):
        return reverse('city', args=[self.city.name.lower(), self.category.name.lower()])

    def get_city_absolute_url(self):
        return get_category_absolute_url()

    def get_absolute_url(self):
        return reverse('post', args=[self.id])

    def save(self, *args, **kwargs):
        return super(Post, self).save(*args, **kwargs)
