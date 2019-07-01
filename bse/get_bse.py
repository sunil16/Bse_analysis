#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
# import urllib2
from zipfile import ZipFile
import csv
import requests
try:
    import urllib.request as urllib2
    from urllib.error import URLError, HTTPError
except ImportError:
    import urllib2

class BseBhav():

    def __init__(self):
        self.todays_date = datetime.datetime.now()
        self.yesterday_date = self.todays_date - datetime.timedelta(days=1)

    def make_url(self):
        download_today_bse = self.yesterday_date .strftime("%d%m%y")
        url = 'http://www.bseindia.com/download/BhavCopy/Equity/EQ' + download_today_bse + '_CSV.ZIP'
        return url

    def get_bhav_zip(self):
        url = self.make_url()
        request = urllib2.Request(url)
        try:
            response = urllib2.urlopen(request)
            if response.getcode() == 200:
                contents = response.read()
                return contents
            else:
                return None
        except urllib2.HTTPError as e:
            print('Bhav copy not available for this date please  https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx', e)
        except (urllib2.URLError):
            print('Bhav copy not available for this date please  https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx', e)
        except Exception:
            import traceback
            print('generic exception: ' + traceback.format_exc())

    def local_file_store(self):
        contents = self.get_bhav_zip()
        if contents is not None:
            ref_date = self.yesterday_date.strftime("%d%m%y")
            local_file_name = 'EQ' + ref_date + '_CSV.ZIP'
            local_zip = open("./bhavlocalzip/bhavlocalzip" + local_file_name, "wb")
            local_zip.write(contents)
            local_zip.close()
            zip_file = ZipFile("./bhavlocalzip/bhavlocalzip" + local_file_name)
            zip_file.extractall(path='./bhavlocalzip/')
            zip_file.close()
