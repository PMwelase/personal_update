import http.client
import date

today = date.get_today_date()
print(today[0])
past = date.get_future_date(-2)

conn = http.client.HTTPSConnection("billboard-api2.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "api-key",
    'x-rapidapi-host': "billboard-api2.p.rapidapi.com",
}

conn.request("GET", f"/hot-100?date={past}&range=1-10", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))