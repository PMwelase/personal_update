import requests

url = "https://quotes-inspirational-quotes-motivational-quotes.p.rapidapi.com/quote"

querystring = {"token":"ipworld.info"}

headers = {
	"X-RapidAPI-Key": "1c3fe2fa88mshb9f4e10177f0384p1eabe7jsn3b1a5c37a2d0",
	"X-RapidAPI-Host": "quotes-inspirational-quotes-motivational-quotes.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

def get_quote():
    text = response.json()
    quote = text['text']
    author = text["author"]
    return quote, author