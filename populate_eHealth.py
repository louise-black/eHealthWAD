
import os
#note: settings is in eHealth_project, not tango_with_django_project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eHealth_project.settings')

import django
django.setup()

#note: healthApp.models not rango.models
from healthApp.models import Category, Page, UserProfile

#maybe import this? not sure...
#from django.contrib.auth.models import User


def populate():

    asthma_cat = add_cat('Asthma')

    add_page(cat=asthma_cat,
        title="Asthma - NHS Choices",
        url="http://www.nhs.uk/conditions/asthma/Pages/Introduction.aspx/")

    add_page(cat=asthma_cat,
        title="Asthma: MedlinePlus",
        url="https://www.nlm.nih.gov/medlineplus/asthma.html/")

    add_page(cat=asthma_cat,
        title="healthfinder.gov - Prevent Allergy and Asthma Attacks at Home",
        url="http://healthfinder.gov/HealthTopics/Category/parenting/safety/prevent-allergy-and-asthma-attacks-at-home/")

    cancer_cat = add_cat("Cancer")

    add_page(cat=cancer_cat,
        title="Cancer Research",
        url="http://www.cancerresearchuk.org/")

    add_page(cat=cancer_cat,
        title="MedlinePlus - Cancer",
        url="https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta?v%3Aproject=medlineplus&v%3Asources=medlineplus-bundle&query=cancer")

    add_page(cat=cancer_cat,
        title="healthfinder.gov - Health Topics - Health Conditions and Diseases - Cancer",
        url="http://healthfinder.gov/HealthTopics/Category/health-conditions-and-diseases/cancer/")

    diabetes_cat = add_cat("Diabetes")

    add_page(cat=diabetes_cat,
        title="Diabetes UK - Care. Connect. Campaign. - Diabetes UK",
        url="https://www.diabetes.org.uk/")

    add_page(cat=diabetes_cat,
        title="MedlinePlus - Diabetes",
        url="https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta?v%3Aproject=medlineplus&v%3Asources=medlineplus-bundle&query=diabetes/")

    add_page(cat=diabetes_cat,
        title="healthfinder.gov - Preventing Diabetes: Questions for the doctor",
        url="http://healthfinder.gov/HealthTopics/Category/doctor-visits/talking-with-the-doctor/preventing-diabetes-questions-for-the-doctor/")


    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0, likes=0):

    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.views=views
    p.url=url

    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting healthApp population script..."
    populate()
