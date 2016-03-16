from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import date
from django.db.models import signals

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
            #self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)



    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    readability = models.IntegerField(default=0)
    subjectivity = models.IntegerField(default=0)
    polarity = models.IntegerField(default=0)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name = 'profile')
    picture = models.ImageField(upload_to='profile_images', blank=True)
    website = models.URLField(blank = True)
    dob = models.DateField(default = date.today)
    email = models.EmailField(blank=True)
    GMALE = 'M'
    GFEMALE = 'F'
    GNEUTRAL = 'P'
    GCHOICES = [(GMALE, 'Male'), (GFEMALE, 'Female'), (GNEUTRAL, 'Gender fluid')]
    gender = models.CharField(max_length = 1, default = 'P', choices = GCHOICES)
    # Override the __unicode__() method to return out something meaningful!
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user = instance)
    signals.post_save.connect(create_user_profile, sender = User)
