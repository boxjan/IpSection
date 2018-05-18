from ip.ip_base import IPBase
from urllib import request
import os
import shutil
import math


class Nic(IPBase):

    def __init__(self):
        super().__init__()

    def main(self):
        self.download_date()
        self.read_data()

    def download_date(self):
        download_url = {'http://inan-data.boxjan.li/delegated-afrinic-extended-latest',
                        'http://inan-data.boxjan.li/delegated-apnic-extended-latest',
                        'http://inan-data.boxjan.li/delegated-arin-extended-latest',
                        'http://inan-data.boxjan.li/delegated-lacnic-extended-latest',
                        'http://inan-data.boxjan.li/delegated-ripencc-extended-latest'}
        temp_path = self.path + "temp/"
        self.make_dir(temp_path)

        for url in download_url:
            print("start download " + url)
            request.urlretrieve(url, temp_path + url.split('/')[-1])
            print("download " + url + " success")

    def read_data(self):
        path = self.path + "temp/"
        if os.path.exists(self.path + "nic/"):
            shutil.rmtree(self.path + "nic/")
        self.make_dir(self.path + "nic/country/ipv4")
        self.make_dir(self.path + "nic/country/ipv6")
        self.make_dir(self.path + "nic/continent/ipv4")
        self.make_dir(self.path + "nic/continent/ipv6")
        for file in os.listdir(path):
            print(path + file)
            if os.path.isfile(path + file):
                self.deal_data(path + file)


    def deal_data(self, file_name):
        path = {'country':{}, 'continent':{}}
        path['country']['ipv4'] = self.path + "nic/country/ipv4/"
        path['country']['ipv6'] = self.path + "nic/country/ipv6/"
        path['continent']['ipv4'] = self.path + "nic/continent/ipv4/"
        path['continent']['ipv6'] = self.path + "nic/continent/ipv6/"

        file = open(file_name)
        country_file_group = {'ipv4': {}, 'ipv6': {}}
        continent_file_group = {'ipv4': {}, 'ipv6': {}}
        continent = {"AS", "EU", "ZZ", "NA", "SA", "OC", "AQ", "AF"}
        for i in continent:
            continent_file_group['ipv4'][i] = open(path['continent']['ipv4'] + i, "a+")
            continent_file_group['ipv6'][i] = open(path['continent']['ipv6'] + i, "a+")

        for line in file:
            if len(line.split('|')) != 8:
                continue

            nic_name, country_code, ip_type, ip, num, date, status, asnum = line.split('|')
            if ip_type == "asn":
                continue

            if country_code == "":
                country_code = "ZZ"

            if country_code not in country_file_group[ip_type].keys():
                country_file_group[ip_type][country_code] = open(path['country'][ip_type] + country_code, "a+")

            country_file_group[ip_type][country_code].write(ip + "/" + str(32-int(math.log2(float(num)))) + "\n")
            continent_file_group[ip_type][self.country_to_continent(country_code)].write(
                ip + "/" + str(32-int(math.log2(float(num)))) + "\n")

        for k, v in country_file_group.items():
            for key, i in v.items():
                i.close()
