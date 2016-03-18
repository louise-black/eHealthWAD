import urllib, urllib2
import keys
from bs4 import BeautifulSoup

HEALTHFINDER_API_KEY = keys.HEALTHFINDER_API_KEY

def search_healthfinder(search_terms):
    # Specify the base
    root_url = 'http://healthfinder.gov/developer/'
    name = 'Search.xml'

    # Including quotes around the search keyword will make it an AND search (results contain all words
    # No quotes is an OR search, a search which returns results with any of the search words
    # The query we will then use is stored within variable query.
    query = '{0}'.format(search_terms)
    query = urllib.quote(query)

    # Construct the request url from the base, name, API key and search terms
    search_url = '{0}{1}?api_key={2}&keyword={3}'.format(
        root_url,
        name,
        HEALTHFINDER_API_KEY,
        query)

    # Create the results list to populate
    results_data = []

    try:
        # Connect to the server and read the response generated.
        response = urllib2.urlopen(search_url).read()

        # Parse the results using the BeautifulSoup package
        parse = BeautifulSoup(response, "html.parser")

        # Loop through each page returned, populating out results list.
        for data in parse.findAll("topic"):
            result_url = data.accessibleversion.string
            result_title = fix_data(data.title.string)
            result_summary = fix_data(data.sections.section.description.string)
            results_data.append({'title': result_title, 'link': result_url, 'summary':result_summary, 'source': "HealthFinder"})

        for data in parse.findAll("tool"):
            result_url = data.accessibleversion.string
            result_title = fix_data(data.title.string)
            result_summary = fix_data(data.categories.string)
            results_data.append({'title': result_title, 'link': result_url, 'summary':result_summary, 'source': "HealthFinder"})

    # Catch a URLError exception - something went wrong when connecting!
    except urllib2.URLError as e:
        print "Error when querying the Healthfinder API: ", e

    # Return the list of results to the calling function.
    return results_data

def fix_data(data):
    new_data = data
    corrections = {"&rsquo;": "'", "&nbsp;": " "}
    for code in corrections.keys():
        if code in data:
            new_data = new_data.replace(code, corrections[code])
    return new_data
