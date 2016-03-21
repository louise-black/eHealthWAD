import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eHealth_project.settings')

import django
django.setup()

from healthApp.models import Category, Page, UserProfile


def populate():

    add_user(username='jill',
             password = 'jill',
             dob = 01/03/1988,
             email = 'jill@gmail.com',
             forename = 'Jill',
             surname = 'Jill',
             gender = 'F',
             )
    add_user (username = 'jim',
              password = 'jim',
              dob = 02/04/1996,
              email = 'jim@gmail.com',
              forename = 'Jim',
              surname = 'Jim',
              gender = 'M')

    add_user (username = 'joe',
              password = 'joe',
              dob = 06/12/1990,
              email = 'joe@gmail.com',
              forename = 'Joe',
              surname = 'Joe',
              gender = 'M')
              
#Rebecca take out username attrib
def add_user(username, password, dob, email, forename, surname, gender):
    u = UserProfile.objects.get_or_create(
        username = username,
        password = password,
        dob = dob,
        email = email,
        forename = forename,
        surname = surname,
        gender = gender)
    u.url = url
    u.views = views
    u.save()
    return u

# Start execution here!
if __name__ == '__main__':
    print "Starting healthApp population script..."
    populate()
