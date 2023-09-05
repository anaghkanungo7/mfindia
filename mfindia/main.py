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


def getLastPrice(schemeCode):
    """Gets last price of a particular fund lookup by scheme code

    Args:
        schemeCode (string): String representation of scheme code

    Returns:
        float: Float value of the NAV of that fund today
    """
    date = datetime.today() - timedelta(days=1)
    df = getMarketSnapshot(date)
    df = df[df['Scheme Code'] == schemeCode]
    return df['ticker_close'].iloc[0]


def getMultipleFundsData(scheme_codes, date):
    raw_data = _getRawData(date)
    df = _parseString(raw_data)
    df = _preprocessData(df)
    
    results = []
    
    for scheme_code in scheme_codes:
        scheme_data = df[df['Scheme Code'] == scheme_code]
        if not scheme_data.empty:
            last_price = scheme_data['ticker_close'].iloc[0]
            results.append({"scheme_code": scheme_code, "last_price": last_price})
    
    return results

def getSimpleReturn(scheme_code, lookback_period):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=lookback_period)
    
    df = getMarketSnapshot(end_date)
    fund_data_start = df[(df['Scheme Code'] == scheme_code) & (df['Date'] == start_date)]
    fund_data_end = df[(df['Scheme Code'] == scheme_code) & (df['Date'] == end_date)]
    
    if fund_data_start.empty or fund_data_end.empty:
        return None  # Data not available for specified dates
    
    nav_start = float(fund_data_start['ticker_close'].iloc[0])
    nav_end = float(fund_data_end['ticker_close'].iloc[0])
    
    simple_return = ((nav_end - nav_start) / nav_start) * 100
    return simple_return


