import requests
import time 
import numpy as np

list_cap = 51 # how many top coins to include
time_frame = '24h,7d,30d'
end_point = 'https://api.coingecko.com/api/v3/'

# declare two dics for alts and bitcoinss
bitcoin_change = {'24h': 0, '7d': 0, '30d': 0}
alt_change = {'24h': [], '7d': [], '30d': []}

markets_end_point = end_point + \
('coins/markets?vs_currency=USD&order=market_cap_desc&per_page={}&page=1&sparkline=false&price_change_percentage=24h,7d,30d')\
.format(list_cap)

api_response = requests.get(markets_end_point)
api_data = api_response.json()

for i in api_data:
	if i['id'] == 'bitcoin':
		bitcoin_change['24h'] = float(i['price_change_percentage_24h_in_currency'])
		bitcoin_change['7d'] = float(i['price_change_percentage_7d_in_currency'])
		bitcoin_change['30d'] = float(i['price_change_percentage_30d_in_currency'])
	else: 
		alt_change['24h'].append(float(i['price_change_percentage_24h_in_currency']))
		alt_change['7d'].append(float(i['price_change_percentage_7d_in_currency']))
		alt_change['30d'].append(float(i['price_change_percentage_30d_in_currency']))

# sort lists

for key in alt_change:
	alt_change[key].sort()

# get mean and median

change_stats = {}

for key in alt_change:
	change_stats[key + '_mean']= np.mean(alt_change[key])
	change_stats[key + '_median']= np.median(alt_change[key])

for key in bitcoin_change:
	bitcoin_change[key] = round((bitcoin_change[key]), 2)

for key in change_stats:
	change_stats[key] = round((change_stats[key]), 2)

print (('24 hour change: BTC: {} %, ALT_MEAN: {} %, ALT_MEDIAN: {} %').format(bitcoin_change['24h'], change_stats['24h_mean'], change_stats['24h_median']))
print (('07 day change: BTC: {} %, ALT_MEAN: {} %, ALT_MEDIAN: {} %').format(bitcoin_change['7d'], change_stats['7d_mean'], change_stats['7d_median']))
print (('30 day change: BTC: {} %, ALT_MEAN: {} %, ALT_MEDIAN: {} %').format(bitcoin_change['30d'], change_stats['30d_mean'], change_stats['30d_median']))


# result_indication(alt_24h_mean)
