#!/usr/bin/env python3
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from sqlalchemy import create_engine

Snapshot_URL = "https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt={}"

def _parseString(raw_data):
    lines = raw_data.split('\n')
    required_data = [line for line in lines if ';' in line]

    values = []
    count = 0
    column = []

    for element in required_data:
        if count == 0:
            column = element.split(';')
            column[-1] = column[-1].rstrip()
        else:
            value = element.split(';')
            value[-1] = value[-1].rstrip()
            values.append(value)
        count += 1

    df = pd.DataFrame(values, columns=column)
    return df

def _getRawData(date):
    formatted_date = date.strftime('%d-%b-%Y')
    response = requests.get(Snapshot_URL.format(formatted_date))
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup.get_text()

def _preprocessData(df):
    df.rename(columns={'Net Asset Value': 'ticker_close', 'Date\r': 'Date'}, inplace=True)
    df['Date'] = df['Date'].str.strip().str.replace('\r', '')
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%Y')
    
    return df

def getMarketSnapshot(date):
    raw_data = _getRawData(date)
    df = _parseString(raw_data)
    df = _preprocessData(df)
    return df