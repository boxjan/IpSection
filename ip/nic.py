from ip.ip_base import IPBase
import os
import shutil
import math


class Nic(IPBase):
    temp_path = ""
    date_path = ""

    def __init__(self):
        super().__init__()
        self.temp_path = self.path + "temp/"
        self.date_path = self.path + __name__.split('.')[-1] + "/"
        self.make_work_dir()

    def main(self):
        self.download_date()

        for file in os.listdir(self.temp_path):
            if os.path.isfile(self.temp_path + file):
                print("Handle " + self.temp_path + file)
                self.deal_data(self.temp_path + file)

    def download_date(self):
        download_url = {r'http://inan-data.boxjan.li/delegated-afrinic-extended-latest',
                        r'http://inan-data.boxjan.li/delegated-apnic-extended-latest',
                        r'http://inan-data.boxjan.li/delegated-arin-extended-latest',
                        r'http://inan-data.boxjan.li/delegated-lacnic-extended-latest',
                        r'http://inan-data.boxjan.li/delegated-ripencc-extended-latest'}

        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(7) as executor:
            status = {executor.submit(self.download, url, self.temp_path + url.split('/')[-1]): url for url in download_url}

            for future in concurrent.futures.as_completed(status):
                status, url = future.result()
                if status is True:
                    print(url.split('/')[-1], "down success")
                else:
                    print(url.split('/')[-1], "down success down fail\n Please Check Url")

    def make_work_dir(self):
        if os.path.exists(self.date_path):
            shutil.rmtree(self.date_path)

        self.make_dir(self.date_path)
        self.make_dir(self.temp_path)

        for ip_accuracy in self.ip_accuracy:
            for ip_type in self.ip_type:
                self.make_dir(self.date_path + "/".join([ip_accuracy, ip_type]))

    def deal_data(self, file_name):
        path = {'country': {}, 'continent': {}}
        for ip_accuracy in self.ip_accuracy:
            for ip_type in self.ip_type:
                path[ip_accuracy][ip_type] = self.date_path + "/".join([ip_accuracy, ip_type]) + "/"

        country_file_group = {'ipv4': {}, 'ipv6': {}}
        continent_file_group = {'ipv4': {}, 'ipv6': {}}
        continent = {"AS", "EU", "ZZ", "NA", "SA", "OC", "AQ", "AF"}

        for i in continent:
            continent_file_group['ipv4'][i] = open(path['continent']['ipv4'] + i, "a+")
            continent_file_group['ipv6'][i] = open(path['continent']['ipv6'] + i, "a+")

        file = open(file_name)
        for line in file:
            if len(line.split('|')) != 8:
                continue

            nic_name, country_code, ip_type, ip, num, date, status, info = line.split('|')
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

    if __name__ == '__main__':
        main()
