# app/robo_advisor.py

import requests
import json
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)
# info inputs 




request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&apikey=demo"

response = requests.get(request_url)
#print(type(response))
#print(response.status_code)
#print(response.text)

parsed_response = json.loads(response.text)
tsd = parsed_response["Time Series (5min)"]
dates = list(tsd.keys())
latest_day = dates[0]
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
tsd = parsed_response["Time Series (5min)"]
latest_close = tsd[latest_day]["4. close"]


#Max of all high prices 
high_prices = []
for date in dates:
  high_price= tsd[date]['2. high']
  high_prices.append(float(high_price))

recent_high = max(high_prices)

#Lowest price

low_prices = []
for date in dates:
  low_price= tsd[date]['3. low']
  low_prices.append(float(low_price))

recent_low = min(low_prices)
#breakpoint()



# info output

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))} ")
print(f"RECENT LOW: {to_usd(float(recent_low))} ")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")