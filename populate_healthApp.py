import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eHealth_project.settings')
import django
django.setup()
from healthApp.models import Category, Page, UserProfile
from django.contrib.auth.models import User

def populate():
    add_user(username='jill',
             password = 'jill',
             dob = "1988-01-03",
             email = 'jill@gmail.com',
             forename = 'Jill',
             surname = 'Jill',
             gender = 'F'
             )
    add_user (username = 'jim',
              password = 'jim',
              dob = "1996-02-04",
              email = 'jim@gmail.com',
              forename = 'Jim',
              surname = 'Jim',
              gender = 'M')
    add_user (username = 'joe',
              password = 'joe',
              dob = "1990-05-22",
              email = 'joe@gmail.com',
              forename = 'Joe',
              surname = 'Joe',
              gender = 'M')
def add_user(username, password, dob, email, forename, surname, gender):
    u = UserProfile.objects.get_or_create(
        #username = username,
        #password = password,
        dob = dob,
        #email = email,
        forename = forename,
        surname = surname,
        gender = gender)[0]
    u.save()
    u.user.username = username
    u.user.password = password
    u.user.email = email
    return u
# Start execution here!
if __name__ == '__main__':
    print "Starting healthApp population script..."
    populate()
