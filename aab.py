import requests
import time 
import numpy as np
from datetime import datetime
import os
import json

list_cap = 51 # how many top coins to include
time_list = ['1h', '24h', '7d', '30d', '200d', '1y']
m = 5 #remove outlier if data is more than m times of std away from mean

time_frame = ','.join(time_list) # join time_list to one str w/ commas
end_point = 'https://api.coingecko.com/api/v3/'
change_perc_key = 'price_change_percentage_{}_in_currency'


# declare empty dicts
bitcoin_change = {}
alt_change = {}
alt_summary = {}
data_dict = {}

# remove outliers
def reject_outliers(data, m):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

# round the numbers
def round_nums(list, point):
	for key in list:
		list[key] = round((list[key]), point)

def export_JSON(directory, dict_name):
	filename = directory
	with open(filename, 'r') as f:
	    data = json.load(f)

	    # overwrite existing obj in json
	    print (data)
	    data = dict_name

	os.remove(filename)
	with open(filename, 'w') as f:
	    # sort key = true to remain the key order
	    json.dump(data, f, indent=4, sort_keys=True)

# declare time_frame lists

for i in time_list:
	bitcoin_change[i] = []
	alt_change[i] = []

markets_end_point = end_point + \
('coins/markets?vs_currency=USD&order=market_cap_desc&per_page={}&page=1&sparkline=false&price_change_percentage={}')\
.format(list_cap, time_frame)

api_response = requests.get(markets_end_point)
api_data = api_response.json()


for i in api_data:
	if i['id'] == 'bitcoin':
		for time in time_list:
			bitcoin_change[time] = float(i[change_perc_key.format(time)])
	else: 
		for time in time_list: 
			if i[change_perc_key.format(time)] is not None: # New coins sometimes do not have data for longer time frame
				alt_change[time].append(i[change_perc_key.format(time)]) # append all alt data into one list


# sort lists and remove outliers
for key in alt_change:
	alt_change[key].sort()
	alt_change[key] = reject_outliers(np.asarray(alt_change[key]), m)

# get mean and median
for key in alt_change:
	alt_summary[key + '_mean']= np.mean(alt_change[key])
	alt_summary[key + '_median']= np.median(alt_change[key])

# round the numbers
round_nums(bitcoin_change, 2)
round_nums(alt_summary, 2)


# Print Summary
# for i in time_list:
#	print (('{} change: BTC: {} %, ALT_MEAN: {} %, ALT_MEDIAN: {} %').format(i, bitcoin_change[i], alt_summary[i + '_mean'], alt_summary[i + '_median']))

# add to the output dicts
for i in time_list:
	data_dict[i.upper()] = {}
	data_dict[i.upper()]['btc'] = bitcoin_change[i]
	data_dict[i.upper()]['alt_mean'] = alt_summary[i + '_mean'] #no i.upper() since it's calling the 1h_mean from alt_summary
	data_dict[i.upper()]['alt_median'] = alt_summary[i + '_median']

# print("Current Time =", current_time)
now = datetime.now()
current_time = now.strftime("%b %d %Y %H:%M:%S")
data_dict['time'] = current_time

export_JSON('priceData.json', data_dict)
