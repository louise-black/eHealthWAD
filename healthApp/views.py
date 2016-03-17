from django.shortcuts import render
from healthApp.models import Category, Page
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

from healthApp.forms import CategoryForm, PageForm

from healthApp.forms import UserForm, UserProfileForm, UserProfile, User

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

    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    # remember to include the visit data
    return render(request, 'healthApp/about.html', {'visits': count})

def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

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

    # Go render the response and return it to the client.
    return render(request, 'healthApp/category.html', context_dict)

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'healthApp/add_category.html', {'form': form})


def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'healthApp/add_page.html', context_dict)


from healthApp.bing_search import search_bing
from healthApp.healthfinder_search import search_healthfinder
from healthApp.medline_search import search_medline
from healthApp.search_all import search_all

def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        print query

        if query:
            # Run bing_search function to get the results list
            result_list = search_all(query)

    return render(request, 'healthApp/search.html', {'result_list': result_list})

def bing_search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run bing_search function to get the results list
            result_list = search_bing(query)

    return render(request, 'healthApp/bing_search.html', {'result_list': result_list})

def healthfinder_search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run healthfinder_search function to get the results list
            result_list = search_healthfinder(query)

    return render(request, 'healthApp/healthfinder_search.html', {'result_list': result_list})

def medline_search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run medline_search function to get the results list
            result_list = search_medline(query)

    return render(request, 'healthApp/medline_search.html', {'result_list': result_list})

def profile_page(request):
    userProfile = UserProfile.objects.get(user = request.user)
    return render(request,
        'healthApp/profile_page.html',
        { 'userProfile': userProfile})
