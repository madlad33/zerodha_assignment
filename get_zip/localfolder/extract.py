from datetime import datetime, time
from zipfile import ZipFile
import schedule
from scrapy.crawler import CrawlerRunner
from get_zip.get_zip.spiders.bhavcopy import BhavcopySpider


def run_spider():
    runner = CrawlerRunner()
    runner.crawl(BhavcopySpider)


def get_file_name():
    date_today = datetime.today().strftime('%d%m%y')
    file_name = f'EQ{date_today}_CSV.zip'
    return file_name


def get_file_name_csv():
    date_today = datetime.today().strftime('%d%m%y')
    file_name = f'EQ{date_today}.csv'
    return file_name


def convert_zip():
    with ZipFile(get_file_name(), 'r') as zip:
        # printing all the contents of the zip file
        zip.printdir()

        # extracting all the files
        print('Extracting all the files now...')
        zip.extractall()
        print('Done!')



