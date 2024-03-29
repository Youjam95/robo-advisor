# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
import csv
import datetime as dt

load_dotenv() #> loads contents of the .env file into the script's environment

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)
# info inputs 


api_key= os.environ.get("ALPHAVANTAGE_API_KEY")
#validting imput
symbol= input("Please input the desired stock symbol")
if symbol.isdigit():
     print("This is not a valid stock symbol, please run the app again and input a valid symbol")
     exit
    


request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"

checkout_start_at = dt.datetime.now() 
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

#csv_file_path = "data/prices.csv" # a relative filepath
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers= ["timestamp","open","high","low","close","volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers )
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices= tsd[date]
        writer.writerow ({ 
         "timestamp" :  date, 
         "open" : daily_prices["1. open"] ,
         "high" : daily_prices["2. high"],
          "low"  : daily_prices["3. low"],
         "close" :daily_prices["4. close"],
         "volume": daily_prices["5. volume"] })   


#Algorithim for buying or not buying
decision = " Don't Buy"
reason = "The Stock's latest closing price is higher than 20% above its recent low."
if float(latest_close)  < (1.2 * float(recent_low ) ): 
    decision = "BUY" 
    reason = "The Stock's latest closing price is less than 20% above its recent low."

# info output

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("Requested at: " + checkout_start_at.strftime("%Y-%m-%d %I:%M %p"))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))} ")
print(f"RECENT LOW: {to_usd(float(recent_low))} ")
print("-------------------------")
print(f"RECOMMENDATION: {decision}")
print(f"RECOMMENDATION REASON: {reason}")
print("-------------------------")
print(f"Writing data to CSV : {csv_file_path}  ")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")




