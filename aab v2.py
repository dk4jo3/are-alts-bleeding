import requests
import time 
import numpy as np

list_cap = 51 # how many top coins to include
time_list = ['24h', '7d', '30d']

time_frame = ','.join(time_list) # join time_list to one str w/ commas
end_point = 'https://api.coingecko.com/api/v3/'
change_perc_key = 'price_change_percentage_{}_in_currency'


# declare two dicts for alts and bitcoinss

bitcoin_change = {}
alt_change = {}
alt_summary = {}


# declare time_frame lists

for i in time_list:
	bitcoin_change[i] = []
	alt_change[i] = []

markets_end_point = end_point + \
('coins/markets?vs_currency=USD&order=market_cap_desc&per_page={}&page=1&sparkline=false&price_change_percentage={}')\
.format(list_cap, time_frame)

api_response = requests.get(markets_end_point)
api_data = api_response.json()


# check if they are not NoneType

for i in api_data:
	if i['id'] == 'bitcoin':
		for time in time_list:
			bitcoin_change[time] = float(i[change_perc_key.format(time)])
	else: 
		for time in time_list: 
			if i[change_perc_key.format(time)] is not None: 
				alt_change[time].append(i[change_perc_key.format(time)])
 
# sort lists (might not be needed)

for key in alt_change:
	alt_change[key].sort()

# get mean and median

for key in alt_change:
	alt_summary[key + '_mean']= np.mean(alt_change[key])
	alt_summary[key + '_median']= np.median(alt_change[key])

for key in bitcoin_change:
	bitcoin_change[key] = round((bitcoin_change[key]), 2)

for key in alt_summary:
	alt_summary[key] = round((alt_summary[key]), 2)

print (('24 hour change: BTC: {} %, ALT_MEAN: {} %, ALT_MEDIAN: {} %').format(bitcoin_change['24h'], alt_summary['24h_mean'], alt_summary['24h_median']))
print (('07 day change: BTC: {} %, ALT_MEAN: {} %, ALT_MEDIAN: {} %').format(bitcoin_change['7d'], alt_summary['7d_mean'], alt_summary['7d_median']))
print (('30 day change: BTC: {} %, ALT_MEAN: {} %, ALT_MEDIAN: {} %').format(bitcoin_change['30d'], alt_summary['30d_mean'], alt_summary['30d_median']))

