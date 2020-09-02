import requests
import time 
import schedule
import datetime
import json
import statistics

def get_data(url, dir, dir2):
    api_response = requests.get(url)
    if api_response.status_code != 200:
        api_price = 'error'
    else:
        api_data = api_response.json()
        if dir2 != 0:
            api_price = api_data[dir][dir2]
        else:
            api_price = api_data[dir]
        api_price = float(api_price)
        api_price = round(api_price, 2)
        return api_price

# retrieve and organize api data

api_response = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=51")
api_data = api_response.json()

#organized data 
api_dumped_data = json.dumps(api_data[0], indent=4)

# get bitcoin price change and conver to float
btc_1h_change = float(api_data[0]['percent_change_1h'])
btc_24h_change = float(api_data[0]['percent_change_24h'])
btc_7d_change = float(api_data[0]['percent_change_7d'])

# store all changes in lists 
alt_1h_change = []
alt_24h_change = []
alt_7d_change = []

# function that takes key and append all to the list also convert them to float
def alt_change_list(time, list_name):
	for i in range(1, 51):
		list_name.append(float(api_data[i][time]))
	return list_name


alt_change_list('percent_change_1h' ,alt_1h_change)
alt_change_list('percent_change_24h' ,alt_24h_change)
alt_change_list('percent_change_7d' ,alt_7d_change)

#get vs BTC %change of alts and round them to 2 decimals
def alt_btc_change_list(list_name, btc_time_change):
	for i in range(len(list_name)):
		list_name[i] = round(list_name[i] - btc_time_change, 2)
	return list_name

alt_btc_change_list(alt_1h_change, btc_1h_change)
alt_btc_change_list(alt_24h_change, btc_24h_change)
alt_btc_change_list(alt_7d_change, btc_7d_change)


#get mean of each list, round to 3 decimal points.
alt_1h_change_mean = round(statistics.mean(alt_1h_change), 3)
alt_24h_change_mean = round(statistics.mean(alt_24h_change), 3)
alt_7d_change_mean = round(statistics.mean(alt_7d_change), 3)


# print results
print ("1H Average:" + str(alt_1h_change_mean) + "%")
print ("1D Average:" + str(alt_24h_change_mean) + "%")
print ("1W Average:" + str(alt_7d_change_mean) + "%")

def result_indication(n):
    if n > 0: 
        print ("not really")
    if n < 0 and n > -5: 
        print ("A little bit")
    if n < -3:
        print ("SELL SELL SELL")

result_indication(alt_24h_change_mean)
