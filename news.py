def get_news_data():
    pass

from newsdataapi import NewsDataApiClient

# API key authorization, Initialize the client with your API key

api = NewsDataApiClient(apikey="pub_7010333054546430074af27fb166d1410fdaa")

# You can pass empty or with request parameters {ex. (country = "us")}

response = api.news_api(language=  "en")

print(response)