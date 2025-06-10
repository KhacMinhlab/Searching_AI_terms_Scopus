import requests
import json
import urllib
import pandas as pd
from time import sleep  # ignore API limitations

def make_df(request):
    df = pd.DataFrame(columns=['title', 'year']) 
    
    for r in request['search-results']['entry']:
        title = r.get('prism:publicationName', 'N/A')
        year = r.get('prism:coverDate', '')[:4]  # Setting the year for searching
        df = df.append({'title': title, 'year': year}, ignore_index=True)
        
    return df


def make_request(query, apiKey, start=0, view='STANDARD'):
    query_str = urllib.parse.urlencode({
        "query": query,
        "apiKey": apiKey,
        "start": start,
        "view": view
    })
    url_str = f"https://api.elsevier.com/content/search/scopus?{query_str}"
    response = requests.get(url_str)
    return response.json()


def get_all_results(query, apiKey, start=0, results_per_page=25):
    results_found = results_per_page
    df = pd.DataFrame()
    
    while results_found == results_per_page:
        request = make_request(query, apiKey, start)
        entries = request['search-results'].get('entry', [])
        if not entries:
            break
        df2 = make_df(request)
        df = pd.concat([df, df2])
        results_found = len(entries)
        start += results_per_page
        sleep(0.3)  # ignore blocked by Elsevier
        
    return df
