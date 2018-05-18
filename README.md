# IpSection
全球IP段数据整理，分别精细到大洲以及国家

### 数据来源 
#### IP 段数据
全球各大互联网络信息中心

* [RIPENCC](ftp://ftp.apnic.net/pub/stats/ripe-ncc/delegated-ripencc-extended-latest) 
* [LACNIX](ftp://ftp.apnic.net/pub/stats/lacnic/delegated-lacnic-extended-latest) 
* [ARIN](ftp://ftp.apnic.net/pub/stats/arin/delegated-arin-extended-latest) 
* [AFRINIC](ftp://ftp.apnic.net/pub/stats/afrinic/delegated-afrinic-extended-latest) 
* [APNIC](ftp://ftp.apnic.net/pub/stats/apnic/delegated-apnic-extended-latest) 
* [IPIP](http://ipip.net)
* [GeoLite](http://dev.maxmind.com)

http://inan-data.boxjan.li/ 提供了 NIC 的数据拷贝

#### 国家及其所属大洲
国家名称缩写遵循 ISO 3166
数据来源 MaxMind GeoLite

考虑到部分IP被广播到全世界各地 所以使用了 ipip.net 免费数据库 GeoLite免费数据库 作为辅助验证

## 使用方法
git clone 后进入目录 
然后执行 ``` python3 main.py``` 
会在目录下生成文件夹 data 和 日期目录，进入之后会有不同数据来源的文件夹 ，进入后按洲和国家，ipv4和ipv6分文件夹
