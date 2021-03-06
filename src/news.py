'''
The following functions call either the Google Knowledge Graph API
or the ContextualWeb News API for information and news about cryptocurrencies.
'''

# from bs4 import BeautifulSoup
import requests
# import re
import json
import os
from dotenv import load_dotenv

# API Key is stored in environment variable for security reasons
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

'''
Requests and receives knowledge graph data for a particular cryptocurrency 
using the google API. Deserialises the recieved JSON, and returns a section of this. 
'''
def get_about_info(crypto_name):
    # https://developers.google.com/knowledge-graph/?hl=en_US
    url = f"https://kgsearch.googleapis.com/v1/entities:search"

    parameters = {
        'key': GOOGLE_API_KEY,
        'languages': 'en',
        'limit': '1',
        'query': crypto_name
    }

    response = requests.request("GET", url, params=parameters)
    google_data = json.loads(response.text)

    with open('../logs/about.log', 'w') as about_file:
        about_file.write(json.dumps(google_data, indent=4))
    
    # print(google_data['itemListElement'][0]['result']['detailedDescription'])
    return google_data['itemListElement'][0]['result']['detailedDescription']


'''
Requests and recieves the news data for a particular query
from the ContextualWeb News API. Deserialises the recieved JSON
and returns a section of this.
'''
def get_news(query_string):
    # https://contextualweb.io/news-api/
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"

    querystring = {
        "q":query_string,
        "pageNumber":"1",
        "pageSize":"10",
        "autoCorrect":"true",
        "fromPublishedDate":"null",
        "toPublishedDate":"null"
    }

    headers = {
        'x-rapidapi-key': NEWS_API_KEY,
        'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    news_data = json.loads(response.text)
    with open('../logs/news.log', 'w') as news_file:
        news_file.write(json.dumps(news_data, indent=4))
    
    return news_data['value']












# ----------------------------------------------------------------------------------------------

# get_about_info('Bitcoin')

# def get_about_info(crypto_name):
#     url = f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles={crypto_name}"
#     response = requests.request("GET", url)
#     wiki_data = json.loads(response.text)

#     with open('about.log', 'w') as about_file:
#         about_file.write(json.dumps(wiki_data, indent=4))
    
#     page_id = next(iter(wiki_data['query']['pages']))
#     wiki_intro = wiki_data['query']['pages'][page_id]['extract']
#     # print(wiki_data['query']['pages'][page_id]['extract'])
#     return wiki_intro

# def get_about_info(crypto_name):
#     crypto_html = requests.get(f"https://coinmarketcap.com/currencies/{crypto_name}").text
#     # print(crypto_html)
#     soup = BeautifulSoup(crypto_html, 'lxml')
#     # print(soup.prettify())
#     about = soup.find('div', class_="sc-1lt0cju-0 srvSa")

#     what_is_heading = about.find(id=re.compile("what-is"))
#     founders_heading = about.find(id=re.compile("who-are-the-founders"))
#     unique_heading = about.find(id=re.compile("what-makes"))
#     final_heading = 'Related Pages:'

#     # print(what_is_heading.text)
#     # print(founders_heading.text)
#     # print(unique_heading.text)

#     what_is_content = about.text.split(what_is_heading.text)[1].split(founders_heading.text)[0]
#     founders_content = about.text.split(founders_heading.text)[1].split(unique_heading.text)[0]
#     unique_content = about.text.split(unique_heading.text)[1].split(final_heading)[0]

#     # print(what_is_content)
#     # print(founders_content)
#     # print(unique_content)
#     all_headings_content = [what_is_heading.text, what_is_content, founders_heading.text, founders_content, unique_heading.text, unique_content]
#     return all_headings_content
    