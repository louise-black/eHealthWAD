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

        if self.views<0:
            raise ValueError, "I can't cope with a negative number here."
        else:
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
    dob = models.DateField(default = date.today)
    forename = models.CharField(max_length=30, default = '')
    surname = models.CharField(max_length=30, default = '')
    email = models.EmailField(blank=True, default = '')
    GMALE = 'M'
    GFEMALE = 'F'
    GNEUTRAL = 'P'
    GCHOICES = [(GMALE, 'Male'), (GFEMALE, 'Female'), (GNEUTRAL, 'Gender fluid')]
    gender = models.CharField(max_length = 1, default = 'P', choices = GCHOICES)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
	
    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user = instance)
    signals.post_save.connect(create_user_profile, sender = User)
