from healthApp.bing_search import search_bing
from healthApp.healthfinder_search import search_healthfinder
from healthApp.medline_search import search_medline

def search_all(search_terms):

     # Create the results list to populate
    results_data = []
    lists = []

    bing_data = search_bing(search_terms)
    medline_data = search_medline(search_terms)
    healthfinder_data = search_healthfinder(search_terms)

    lists.append(bing_data)
    lists.append(medline_data)
    lists.append(healthfinder_data)

    smallest_data = smallestData(lists)

    pointer = 0
    for x in range(len(smallest_data)):
        results_data.append(lists[0][x])
        results_data.append(lists[1][x])
        results_data.append(lists[2][x])
        pointer = x
    lists.remove(smallest_data)

    smallest_data = smallestData(lists)

    for y in range(pointer, len(smallest_data)):
        results_data.append(lists[0][y])
        results_data.append(lists[1][y])
        pointer = y
    lists.remove(smallest_data)

    for z in range(pointer, len(lists[0])):
        results_data.append(lists[0])

    return results_data

def smallestData(list):
    smallest = list[0]
    for x in list:
        if len(x) < len(smallest):
            smallest = x
    return smallest