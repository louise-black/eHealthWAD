from healthApp.bing_search import search_bing
from healthApp.healthfinder_search import search_healthfinder
from healthApp.medline_search import search_medline

def search_all(search_terms):

     # Create the results list to populate
    results_data = []

    results_data += search_bing(search_terms)
    results_data += search_medline(search_terms)
    results_data += search_healthfinder(search_terms)

    return results_data