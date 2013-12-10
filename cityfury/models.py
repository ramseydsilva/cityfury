from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from django.core.urlresolvers import reverse


class ContactForm(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True)
    replied = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s - %s" %(self.name, self.comment[:50])

class Country(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, null=True, blank=True)
    publish = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('city', args=["all", self.name.lower()])

class Area(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City)
    publish = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Location(models.Model):
    string = models.CharField(max_length=1000)
    city = models.ForeignKey(City)

class Category(models.Model):
    name = models.CharField(max_length=50)
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Organisation(models.Model):
    name = models.CharField(max_length=200)
    views = models.IntegerField(default=0)

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

    class Meta:
        unique_together = (('user', 'post'),)

    def __unicode__(self):
        return self.user.username + " - " + self.post.caption

class PostFlag(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey("Post")
    created_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __unicode__(self):
        return "%s - %s - %s" %(self.user.username, self.post.caption, self.comment[:10])

IMAGE_POST = "I"
TEXT_POST = "T"
POST_TYPE_CHOICES = (
    (IMAGE_POST, "Image"),
    (TEXT_POST, "Text")
)

class Post(models.Model):
    type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default=IMAGE_POST)
    caption = models.CharField(max_length=500)
    description = models.TextField()
    image = ImageField(upload_to=upload_to, null=True, blank=True)
    location_string = models.CharField(max_length=500, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    area = models.ForeignKey(Area, null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    organisation = models.ForeignKey(Organisation, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    dislikes = models.ManyToManyField(User, through="Dislike", related_name="disliked_posts")
    flags = models.ManyToManyField(User, through="PostFlag", related_name="flagged_posts")
    views = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_date",)

    def __unicode__(self):
        if not self.caption:
            return "No caption: %s" %( self.id )
        return self.caption[:50]

    def get_city_absolute_url(self):
        if self.category and self.city:
            return reverse('city', args=[self.category.name.lower(), self.city.name.lower()])
        if self.category:
            return reverse("category", args=[self.category.name.lower()])
        if self.city:
            return reverse("city", args=["all", self.city.name.lower()])
        return ""

    def get_absolute_url(self):
        return reverse('post', args=[self.id])

    def save(self, *args, **kwargs):
        return super(Post, self).save(*args, **kwargs)

class ContactFlag(models.Model):
    user = models.ForeignKey(User)
    contact = models.ForeignKey("Contact")
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s - %s" %(self.user.username, self.contact.name, self.comment[:10])

class ContactCorrection(models.Model):
    name = models.CharField(max_length=300, default="", blank=True)
    title = models.CharField(max_length=300, default="", blank=True)
    website = models.CharField(max_length=300, default="", blank=True)
    email = models.CharField(max_length=300, default="", blank=True)
    phone = models.CharField(max_length=300, default="", blank=True)
    organisation = models.CharField(max_length=300, default="", blank=True)
    comments = models.TextField()
    category = models.ForeignKey(Category, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    area = models.ForeignKey(Area, null=True, blank=True)
    contact = models.ForeignKey("Contact")

    added_by = models.ForeignKey(User, null=True, blank=True)
    published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_date",)

    def __unicode__(self):
        if self.name:
            return self.name
        if self.organisation:
            return self.organisation
        if self.website:
            return self.website
        if self.phone:
            return self.phone
        if self.email:
            return self.email
        return None

    def implement_correction(self):
        self.contact.name = self.name
        self.contact.title = self.title
        self.contact.website = self.website
        self.contact.email = self.email
        self.contact.phone = self.phone
        self.contact.organisation = self.organisation
        self.published = True
        self.contact.save()

    def save(self, *args, **kwargs):
        if self.added_by and self.contact.added_by and self.added_by == self.contact.added_by:
            self.implement_correction()
        super(ContactCorrection, self).save(*args, **kwargs)

class Contact(models.Model):
    name = models.CharField(max_length=300, default="", blank=True)
    title = models.CharField(max_length=300, default="", blank=True)
    website = models.CharField(max_length=300, default="", blank=True)
    email = models.CharField(max_length=300, default="", blank=True)
    phone = models.CharField(max_length=300, default="", blank=True)
    organisation = models.CharField(max_length=300, default="", blank=True)
    comments = models.TextField()
    category = models.ForeignKey(Category, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    area = models.ForeignKey(Area, null=True, blank=True)
    post = models.ForeignKey(Post, null=True, blank=True)

    added_by = models.ForeignKey(User, null=True, blank=True)
    approved = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if self.name:
            return self.name
        if self.organisation:
            return self.organisation
        if self.website:
            return self.website
        if self.phone:
            return self.phone
        if self.email:
            return self.email
        return None
