def get_news_data():
    pass

# https://docs.python.org/3/library/json.html
# This library will be used to parse the JSON data returned by the API.
import json
# https://docs.python.org/3/library/urllib.request.html#module-urllib.request
# This library will be used to fetch the API.
import urllib.request

apikey = "aeeb4267cc8f91ca332c18c1febe0cd0"
category = "general"
url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&max=10&apikey={apikey}"



if __name__ == "__main__":
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]

        for i in range(len(articles)):
            # articles[i].title
            print(f"Title: {articles[i]['title']}")
            # articles[i].description
            print(f"Description: {articles[i]['description']}")
            # You can replace {property} below with any of the article properties returned by the API.
            # articles[i].{property}
            # print(f"{articles[i]['{property}']}")

            # Delete this line to display all the articles returned by the request. Currently only the first article is displayed.
            # break