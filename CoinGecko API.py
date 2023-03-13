#!/usr/bin/env python
# coding: utf-8

import requests
import json
from datetime import timedelta, date, datetime
import time
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

top_coins = [
    'Bitcoin',
    'Ethereum',
    'Tether',
    'USD Coin',
    'BNB',
]

# ## Creating DB for results
# 
# https://coinmarketcap.com/


conn = sqlite3.connect('coin_prices.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS prices (
    coingecko_id nvarchar(255),
    price_date date,
    btc REAL,
    usd REAL,
    insert_dttm datetime
    )
''')

conn.commit()

c.execute('''
    SELECT distinct price_date
    FROM prices
''')
conn.commit()

# ## Save loaded data

dates_saved = [
    datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S') for x in c.fetchall()
]


def get_simple_coins_list() -> dict:
    """
    Функция возвращает список всех поддерживаемых coingecko криптовалют
    """
    coins_url = (
        'https://api.coingecko.com/api/v3/coins/list?include_platform=false'
    )
    content = requests.get(coins_url)
    return json.loads(content.text)


def get_history(coin: str, date: str) -> dict:
    """
    Функция возвращает историю по монете за дату
    
    Args:
        coin (str): тикер монеты
        date (str): дата в формате "07-07-2022"
    
    Returns:
        (dict): словарь с двнными по цене
    """
    history_url = (
        f'https://api.coingecko.com/api/v3/coins/{coin}/history?date={date}'
    )
    content = requests.get(history_url)
    return json.loads(content.text)


# ## Get coins data and list of all items

coins_meta = get_simple_coins_list()


# get_ipython().run_cell_magic('time', '', 'coins_meta = get_simple_coins_list()\n')


def parse_coins_id(coins_meta: dict) -> list:
    """
    Функция парсит данные по наименованиям монет и возвращает только нужные поля
    
    Args:
        coins_meta (dict): словарь всех монет
    Returns:
        (list):  с преобразованными данными по монетам
    """
    list_id = []
    for row in coins_meta:
        list_coin = (row['id'], row['symbol'], row['name'])
        list_id.append(list_coin)
    return list_id


# # Generate DataFrame fom list of all supported by coingecko cryptoCurrencies

df_coins_all_meta = pd.DataFrame(parse_coins_id(coins_meta), columns=['id', 'symbol', 'name'])
print(df_coins_all_meta.shape)
print(df_coins_all_meta.head())

# # We select currencies which only are exists in our list

coins_set = df_coins_all_meta.loc[df_coins_all_meta.name.isin(top_coins)]
print(coins_set)

# Generate start date and all date pool which we are need to processing. Period could be variable.

DELTA_PERIOD = 14

if dates_saved:
    start_date = max(dates_saved) + timedelta(days=1)
else:
    start_date = date.today() - timedelta(days=DELTA_PERIOD)

end_date = date.today() - timedelta(days=1)
daterange = [x.strftime('%d-%m-%Y') for x in pd.date_range(start_date, end_date)]


def get_coins_price_set(coins_ids: np.ndarray, daterange: list) -> list:
    """
    Функция парсит данные по наименованиям монет и возвращает только нужные поля.
    Args:
        coins_ids (np.ndarray): массив из тикеров монет
    """
    list_hist = []

    for each_id in coins_ids:
        for i, each_date in enumerate(daterange):
            try:
                print(each_id, f'day {i + 1}')
                data = get_history(each_id, each_date)
                btc_price = data['market_data']['current_price']['btc']
                usd_price = data['market_data']['current_price']['usd']
                list_hist.append((each_id, each_date, btc_price, usd_price))
                time.sleep(10.25)  # follow limitation 50req/sec
            except Exception as e:
                print(f'Error was occured {e}')
                continue
    return list_hist


print(f"Getting history for {coins_set['id'].nunique()} coins and {DELTA_PERIOD} days")
list_hist = get_coins_price_set(coins_set['id'].unique(), daterange)

pd.set_option('display.float_format', str)

set_loaded_history_coins = pd.DataFrame(list_hist, columns=['coingecko_id', 'price_date', 'btc', 'usd']).sort_values(
    'price_date')
set_loaded_history_coins['price_date'] = set_loaded_history_coins['price_date'].apply(
    lambda x: datetime.strptime(x, '%d-%m-%Y'))
set_loaded_history_coins['insert_dttm'] = datetime.now()

set_history_coins = pd.DataFrame([x for x in c.fetchall()],
                                 columns=['coingecko_id', 'price_date', 'btc', 'usd', 'insert_dttm'])
set_history_coins['price_date'] = set_history_coins['price_date'].apply(lambda x: datetime.strptime(x, '%d-%m-%Y'))

set_all_coins = pd.concat([set_history_coins, set_loaded_history_coins])

set_all_coins.price_date = set_all_coins['price_date'].astype('datetime64[ns]')
set_loaded_history_coins.to_sql('prices', conn, if_exists='append', index=False)

print(set_all_coins.head())

max_val_btc = set_all_coins.groupby('coingecko_id')['btc'].max()
max_val_btc_df = pd.DataFrame(max_val_btc).rename(columns={'btc': 'btc_max'})

set_history_coins_merged = pd.merge(
    set_all_coins,
    max_val_btc_df,
    on='coingecko_id'
)

set_history_coins_merged['btc_norm'] = set_history_coins_merged['btc'] / set_history_coins_merged['btc_max']

avg_score = (set_history_coins_merged[['coingecko_id', 'price_date', 'btc_norm']]
             .groupby('coingecko_id')[['btc_norm']].mean(numeric_only=True)
             .sort_values('btc_norm', ascending=False)
             )

bar_test = set_history_coins_merged.loc[set_history_coins_merged.price_date ==
                                        set_history_coins_merged.price_date.max()
                                        ].sort_values('btc_norm', ascending=False)

max_val_btc = set_all_coins.groupby('coingecko_id')['btc'].max()
max_val_btc_df = pd.DataFrame(max_val_btc).rename(columns={'btc': 'btc_max'})

bar_test.plot.bar(x='coingecko_id', y='btc_norm')
plt.ylim(.8, 1.01)
plt.show()
