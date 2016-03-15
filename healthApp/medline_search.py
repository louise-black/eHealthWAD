import urllib, urllib2
from bs4 import BeautifulSoup

def search_medline(search_terms):
    # Specify the base and where to search
    root_url = 'https://wsearch.nlm.nih.gov/ws/query'
    name = 'healthTopics'

    # Specify how many results we wish to be returned per page.
    # Offset specifies where in the results list to start from.
    # With results_per_page = 10 and offset = 11, this would start from page 2.
    results_per_page = 10
    offset = 0

    # The query we will use is stored within variable query, and converted to appropriate form
    query = "{0}".format(search_terms)
    query = urllib.quote(query)

    # Construct the request url from the base, name and search terms
    search_url = "{0}?db={1}&term={2}&retstart={3}&retmax={4}".format(
        root_url,
        name,
        query,
        offset,
        results_per_page)

    # Create the results list to populate
    results_data = []

    try:
        # Connect to the server and read the response generated.
        results = urllib2.urlopen(search_url).read()

        # Parse the results using the BeautifulSoup package
        parse = BeautifulSoup(results, "html.parser")

        # Loop through each page returned, populating out results list.
        # Checks for and removes stray <span class="qt0"> and </span> tags and removes them
        for data in parse.findAll("document"):
            result_url = data["url"]
            tags = data.findAll("content")
            for tag in tags:
                if tag["name"] == "title":
                    working_title = tag.string
                    working_title = urllib2.unquote(working_title)
                    if '<span class="qt0">' in working_title:
                        working_title = working_title.replace('<span class="qt0">', '')
                        working_title = working_title.replace('</span>', '')
                    result_title = working_title
                if tag["name"] == "snippet":
                    working_summary = tag.string
                    working_summary = urllib2.unquote(working_summary)
                    if '<span class="qt0">' in working_summary:
                        working_summary = working_summary.replace('<span class="qt0">', '')
                        working_summary= working_summary.replace('</span>', '')
                    result_summary = working_summary
            results_data.append({'title': result_title, 'link': result_url, 'summary':result_summary})

    # Catch a URLError exception - something went wrong when connecting!
    except urllib2.URLError as e:
        print "Error when querying the Medline API: ", e

    # Return the list of results to the calling function.
    return results_data