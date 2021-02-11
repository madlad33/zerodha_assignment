import sys
import redis
import pandas as pd
import json
import schedule
from datetime import datetime, time
from zipfile import ZipFile
import schedule
from scrapy.crawler import CrawlerRunner
from get_zip.get_zip.spiders.bhavcopy import BhavcopySpider
from get_zip.localfolder.extract import run_spider,convert_zip
sys.path.append("..")
from get_zip.localfolder.extract import get_file_name, get_file_name_csv


def parse_csv():
    file_path = f'L:\Django projects\zerodha_assignment\get_zip\localfolder\{get_file_name_csv()}'
    try:
        csv_data = pd.read_csv(r'L:\Django projects\zerodha_assignment\get_zip\localfolder\EQ080221.csv')
        csv_data = csv_data[['SC_CODE', 'SC_NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE']].copy()
    except Exception as e:
        return 'Something went wrong, Kindly try again.'
    return csv_data


def set_up():
    try:
        r = redis.Redis(host="localhost",
                        port=6379,
                        charset="utf-8",
                        decode_responses=True,
                        db=2)
        return r
    except Exception:
        return "Couldn't connect to redis database."


def load_data():
    try:
        r = set_up()
        csv_data = parse_csv()
        for index, row in csv_data.iterrows():
            name = str(row['SC_NAME']).strip()
            r.hmset(name, row.to_dict())

    except Exception as e:
        return 'Trouble loading data into redis.'


def get_data():
    try:
        r = set_up()
        data = {}
        for key in r.scan_iter(match='*'):
            data[key] = r.hgetall(key)
        data_list = []
        for j in data.values():
            data_list.append(j)
        print(len(data_list))
        return data_list
    except Exception as e:
        return 'Failed to get the data from redis database.'


def search_data(searched_data):
    r = set_up()
    # a = r.hgetall('equity:*')
    # for key in r.scan_iter("equity:*"):
    #     a = key[7:]
    #     code = r.get(key)
    #     print(code)
    # keys = r.scan_iter('equity:*' + str(searched_data).upper() + '*')
    # keys = r.scan_iter(match='*' + str(searched_data).upper() + '*')
    # for key in r.scan_iter(f"equity:{searched_data}"):
    #     code = r.get(key)
    #     print(code)
    stock_list = []
    for equity in r.scan_iter(match='*' + str(searched_data).upper() + '*'):
        stock_list.append(r.hgetall(equity))

    # print(list(keys))

    # a = r.hgetall('equity:TTIENT')

    # for key in keys:
    #     data = r.hgetall(key)
    #     stock_list.append(data)

    return stock_list


# parse_csv()
# load_data()

# print(search_data('TTI'))
def schedule_function():
    schedule.every().day.at("18:01").do(run_spider(),convert_zip(),parse_csv(),load_data())
    # schedule.every().day.at("18:02").do(parse_csv())
    #     # schedule.every().day.at("18:03").do(load_data())
