from django.shortcuts import render
from healthApp.models import Category, Page, UserProfile
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify

from healthApp.forms import CategoryForm, PageForm

from healthApp.forms import UserForm, UserProfileForm, UserProfile, EditProfileForm

def index(request):


    category_list = Category.objects.all()
    page_list = Page.objects.all()
    context_dict = {'categories': category_list, 'pages': page_list}

    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, we default to zero and cast that.
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'healthApp/index.html', context_dict)

    return response


def about(request):
    category_list = Category.objects.all()
    page_list = Page.objects.all()

    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    context_dict = {'categories': category_list, 'pages': page_list, 'visits':count}

    # remember to include the visit data
    return render(request, 'healthApp/about.html', context_dict)

def category(request, user_name_slug, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}
    category_list = Category.objects.all()
    page_list = Page.objects.all()
    context_dict['categories']= category_list
    context_dict['pages'] = page_list
    private = "PRIV"

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slugCat=category_name_slug, slugUser = user_name_slug)
        context_dict['category_name'] = category.name
        private = category.pubOrPriv

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    try:
        if request.user.profile.slug != user_name_slug and private == "PRIV":
            context_dict = []
    except AttributeError:
        if private == "PRIV":
            context_dict = []

    # Go render the response and return it to the client.
    return render(request, 'healthApp/category.html', context_dict)


def add_category(request):
    context_dict = {}
    category_list = Category.objects.all()
    page_list = Page.objects.all()
    context_dict['categories']= category_list
    context_dict['pages'] = page_list
    categoryUnique = True

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            category = form.save(commit=True)
            category.user = request.user
            category.slugUser = slugify(request.user.username)
            for c in category_list:
                if c.name == category.name and c.user == category.user:
                    categoryUnique = False

            if categoryUnique:
                category.save()
            else:
                print "Category name not unique wihin user"
            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()


    context_dict['form'] = form

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'healthApp/add_category.html', context_dict)

from pageProcess import process

def add_page(request, user_name_slug, category_name_slug):

    context_dict = {}

    try:
        cat = Category.objects.get(slugCat=category_name_slug, slugUser=user_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        page_form = PageForm(request.POST)
        print request.POST
        if page_form.is_valid():
            if cat:
                page = page_form.save(commit=False)
                page.url = request.POST.get('url')
                page.category = cat
                page.views = 0
                page.subjectivity, page.polarity, page.readability = process(request.POST.get('url'))

                page.save()
                #page.url = url
                # probably better to use a redirect here.
                return category(request,user_name_slug, category_name_slug)
        else:
            print page_form.errors
    else:
        page_form = PageForm()

    context_dict ['form']=page_form
    context_dict['category'] = cat

    return render(request, 'healthApp/add_page.html', context_dict)


from healthApp.bing_search import search_bing
from healthApp.healthfinder_search import search_healthfinder
from healthApp.medline_search import search_medline
from healthApp.search_all import search_all

def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run bing_search function to get the results list
            result_list = search_all(query)

    category_list = Category.objects.all()
    page_list = Page.objects.all()
    context_dict = {'categories': category_list, 'pages': page_list,'result_list': result_list}

    return render(request, 'healthApp/search.html', context_dict)

def bing_search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run bing_search function to get the results list
            result_list = search_bing(query)
    category_list = Category.objects.all()
    page_list = Page.objects.all()
    context_dict = {'categories': category_list, 'pages': page_list,'result_list': result_list}



    return render(request, 'healthApp/bing_search.html', context_dict)

def healthfinder_search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run healthfinder_search function to get the results list
            result_list = search_healthfinder(query)

    category_list = Category.objects.all()
    page_list = Page.objects.all()
    context_dict = {'categories': category_list, 'pages': page_list,'result_list': result_list}

    return render(request, 'healthApp/healthfinder_search.html', context_dict)

def medline_search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run medline_search function to get the results list
            result_list = search_medline(query)

    category_list = Category.objects.all()
    page_list = Page.objects.all()
    context_dict = {'categories': category_list, 'pages': page_list,'result_list': result_list}

    return render(request, 'healthApp/medline_search.html', context_dict)

def profile_page(request):

    user = request.user.profile
    category_list = Category.objects.all()
    cat_list = []
    page_list = []
    pages_list = Page.objects.all()
    context_dict = {"categories":cat_list, "pages":page_list}
    for c in category_list:
        if c.user == request.user:
            cat_list.append(c)
            page_list.append(Page.objects.all().filter(category=c))

    context_dict = {"categories":cat_list, "pages":page_list}
    return render(request,
        'healthApp/profile_page.html',
        context_dict)

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.slug = slugify(user.username)
            profile.save()
            print "profile saved"

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'healthApp/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def editProfile(request):
    userProfile = UserProfile.objects.get(user = request.user)
    form = EditProfileForm(request.POST, initial = {'forename': userProfile.forename, 'surname': userProfile.surname, 'email': 			userProfile.email})
    if form.is_valid():
        userProfile.forename = request.POST['forename']
        userProfile.surname = request.POST['surname']
        userProfile.email = request.POST['email']
        userProfile.save()
        #return HttpResponseRedirect('healthApp/profile_page.html')
        return profile_page(request)
    context_dict = {"form":form}
    return render (request, "healthApp/edit_profile.html", context_dict)

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/healthApp/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your healthApp account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'healthApp/base.html', {})
