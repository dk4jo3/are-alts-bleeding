import requests
import time 
import schedule
import datetime
import json
import statistics

list_cap = 10 # how many top coins to include
time_frame = '24h,7d,30d'
end_point = 'https://api.coingecko.com/api/v3/'

# declare two dics for alts and bitcoinss
bitcoin_change = {'24h_change': [], '7d_change': [], '30d_change': []}
alt_change = {'24h_change': [], '7d_change': [], '30d_change': []}

markets_end_point = end_point + \
('coins/markets?vs_currency=USD&order=market_cap_desc&per_page={}&page=1&sparkline=false&price_change_percentage=24h,7d,30d')\
.format(list_cap)

api_response = requests.get(markets_end_point)
api_data = api_response.json()

for i in api_data:
	if i['id'] == 'bitcoin':
		bitcoin_change['24h_change'].append(float(i['price_change_percentage_24h_in_currency']))
		bitcoin_change['7d_change'].append(float(i['price_change_percentage_7d_in_currency']))
		bitcoin_change['30d_change'].append(float(i['price_change_percentage_30d_in_currency']))
	else: 
		alt_change['24h_change'].append(float(i['price_change_percentage_24h_in_currency']))
		alt_change['7d_change'].append(float(i['price_change_percentage_7d_in_currency']))
		alt_change['30d_change'].append(float(i['price_change_percentage_30d_in_currency']))
		

print (bitcoin_change)
print (alt_change)


# # print results
# print ("1H Average:" + str(alt_1h_change_mean) + "%")
# print ("1D Average:" + str(alt_24h_change_mean) + "%")
# print ("1W Average:" + str(alt_7d_change_mean) + "%")

# def result_indication(n):
#     if n > 0: 
#         print ("not really")
#     if n < 0 and n > -5: 
#         print ("A little bit")
#     if n < -3:
#         print ("SELL SELL SELL")

# result_indication(alt_24h_change_mean)
