#!/bin/python3

from abc import ABCMeta, abstractmethod
import csv
import os
import time


class IPBase(metaclass=ABCMeta):

    cn_country = {}
    en_country = {}
    continent = {}
    __path = os.path.abspath(".") + "/"
    path = ""

    def __init__(self):
        self.get_today_path()
        self.cn_country.clear()
        self.continent.clear()
        self.en_country.clear()
        self.get_continent_data()

    def get_today_path(self):
        now_date = time.strftime("%Y-%m-%d", time.localtime())
        self.path = self.__path + "data/" + now_date + "/"

    def make_dir(self, name):
        path = name
        if not os.path.exists(path):
            os.makedirs(path)
            print("Make dir " + path + " success")
        else:
            print("Dir " + path + " is existed")

    @abstractmethod
    def download_date(self):
        return

    def country_to_continent(self, country_code):

        return self.continent[country_code]

    def get_continent_data(self):
        f = open(self.__path + "Country-info/country-en.csv")
        f_csv = csv.DictReader(f)
        for row in f_csv:
            self.en_country[row['country_name']] = row['country_iso_code']

        f.close()

        f = open(self.__path + "Country-info/country-zh.csv")
        f_csv = csv.DictReader(f)
        for row in f_csv:
            self.cn_country[row['country_name']] = row['country_iso_code']
            self.continent[row['country_iso_code']] = row['continent_code']
        f.close()

    def __del__(self):
        import shutil
        shutil.rmtree(self.path + "temp/")
