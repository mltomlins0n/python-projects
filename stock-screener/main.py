import requests, time, re, os
import pickle5 as pkl
import pandas as pd
from keys import api_key

url = 'https://api.tdameritrade.com/v1/instruments'

df = pd.read_excel('company_list.xlsx', engine='openpyxl')
# Get only the stock symbols
df_symbols = df['Symbol'].values.tolist()

## Retrieve results in batches of 500 to get around API call limits
start = 0
end = 500
files = []
while start < len(df_symbols):
    tickers = df_symbols[start:end]

    payload = {'apikey': api_key,
               'symbol': tickers,
               'projection': 'fundamental'}
               
    results = requests.get(url,params=payload)
    data = results.json()
    # Create files with timestamp and extension
    f_name = time.asctime() + '.pkl'
    # Replace the space and colon in the filename to satisfy Windows
    f_name = re.sub('[ :]','_',f_name)
    files.append(f_name)
    with open(f_name, 'wb') as file:
        pkl.dump(data,file)
    # Set new start point at the end of last run and get next batch of 500
    start = end
    end += 500
    time.sleep(0.5)

'''
Read pkl files and merge contents into a list.
Grab points of interest from the API and use them as columns
in the output.
'''
data = []
for file in files:
    with open(file, 'rb') as f:
        info = pkl.load(f)
    tickers = list(info)
    # The data to grab from results
    points = ['symbol','netProfitMarginMRQ','peRatio','pegRatio','high52','low52']
    for ticker in tickers:
        tick = []
        for point in points:
            tick.append(info[ticker]['fundamental'][point])
        data.append(tick)
    os.remove(file) # cleanup

# The columns to print to the data frame
points = ['symbol','Margin','PE','PEG','high52','low52']
df_results = pd.DataFrame(data,columns=points)

'''
Return a stock by the symbol specified
param: symbol - a String of the symbol to search for
'''
def find(symbol):
    result = df_results[(df_results['symbol'] == symbol)]
    print(result)

'''
Print the results fromm a data frame in batches of 'size'
param: frame - the data frame to view
       size - the no. of rows per batch
'''
def view(frame, size):
    start = 0
    stop = size
    while stop < len(frame):
        print(frame[start:stop])
        start = stop
        stop += size
    print (frame[start:stop])

# Slice the data frame to return results according to params we specify
df_sliced = df_results[(df_results['PEG'] < 1) & (df_results['PEG'] > 0) &
(df_results['Margin'] > 20) & (df_results['PE'] > 10) & (df_results['high52'] > 100)]
view(df_sliced, 50)

# Get only the symbols and make them a list
#df_symbols = df_sliced['symbol'].tolist()
#print(df_symbols)

# Returns True or False for each symbol
new = df['Symbol'].isin(df_symbols)
companies = df[new]
view(companies, 100)

find('GME')