#!/usr/bin/env python
# coding: utf-8

# In[1]:
# imports
from influxdb import InfluxDBClient
from influxdb import DataFrameClient

# In[2]:
# params
host = '127.0.0.1'
port = 8086
dbname = 'jmeter'

# In[3]:
# init db connection
client = InfluxDBClient(host, port, dbname)
dfclient = DataFrameClient(host, port, dbname)
client.create_database(dbname)

# In[4]:
# delete old metrics from influx
dfclient.query(
    f''' DELETE FROM "jmeter" WHERE "application" = 'rambler_session' ''', database=dbname)

# In[5]:
# check result

q = dfclient.query(
    f''' SELECT * FROM "jmeter" WHERE "application" = 'rambler_session' ''', database=dbname)
if (not q):
    print('OLD METRICS HAS BEEN DELETED FROM INFLUX!')
