import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eHealth_project.settings')
import django
django.setup()
from healthApp.models import Category, Page, UserProfile
from django.contrib.auth.models import User

def populate():
    bob_user = add_user('bob','bob',"1988-01-03",'bob@gmail.com','Bob','Bob','F')
    jim_user = add_user ('jim','jim',"1996-02-04",'jim@gmail.com','Jim','Jim','M')
    joe_user = add_user ('joe','joe',"1990-05-22",'joe@gmail.com','Joe','Joe','M')
def add_user(uSername, pAssword, dob, email, forename, surname, gender):
        try:
    		u = User.objects.get(username=uSername)
    		up = UserProfile(user=u)
        except:
            u = User(username=uSername)
            u.set_password(pAssword)
            u.save()
            up = UserProfile(user=u)
            up.dob = dob
            up.email = email
            up.forename = forename
            up.surname = surname
            up.gender = gender
            up.save()
        return up

# Start execution here!
if __name__ == '__main__':
    print "Starting healthApp population script..."
    populate()
