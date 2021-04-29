#!/usr/bin/env python
# coding: utf-8

# In[1]:
# imports
from influxdb import InfluxDBClient
from influxdb import DataFrameClient
import datetime
import pandas as pd

# In[2]:
# params
host = '127.0.0.1'
port = 8086
dbname = 'jmeter'

# In[3]:
# init
client = InfluxDBClient(host, port, dbname)
dfclient = DataFrameClient(host, port, dbname)
client.create_database(dbname)

# In[4]:


def MaxPct95(application):
    startRow = dfclient.query(
        f''' SELECT first(maxAT) FROM "jmeter" WHERE "transaction" = 'internal' AND "application" = '{application}' ''', database=dbname)
    endRow = dfclient.query(
        f''' SELECT last(maxAT) FROM "jmeter" WHERE "transaction" = 'internal' AND "application" = '{application}' ''', database=dbname)

    startRow = startRow['jmeter']
    endRow = endRow['jmeter']

    startRowTime = startRow.index[0]
    endRowTime = endRow.index[0]

    unix_startRowTime = int(pd.to_datetime(startRowTime).value / 1000000)
    unix_endRowTime = int(pd.to_datetime(endRowTime).value / 1000000)

    result = dfclient.query(
        f''' SELECT max("pct90.0") FROM "jmeter" WHERE time >= {unix_startRowTime}ms and time <= {unix_endRowTime}ms ''', database=dbname)
    return result['jmeter']


# In[5]:
# create and save file
maxPct95_result = str(MaxPct95('rambler_session'))
print(maxPct95_result)
line = f'Max 95 percentile for the test = {maxPct95_result}'
filename = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
file = open(f'artifact_{filename}.txt', 'w')
file.write(line)
