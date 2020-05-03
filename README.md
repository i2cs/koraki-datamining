# koraki-datamining project

## installation
pip install flask
pip install flask-restful
pip install waitress

pip install request
pip install mysql-connector


## apriori.py
A simple implementation of Apriori algorithm by Python by Yu Mochizuki

## fetch_data.py
Library to fetch this week product event data from Koraki piwik API and populate data to database. Next step is to call apriori implementation to mine frequent rules

usage: fetch_data.py [-h] -i SITEID [-c CONFIDENCE] [-s SUPPORT]

optional arguments:
  -h, --help            show this help message and exit
  -i SITEID, --siteid SITEID
                        Site id to fetch data from
  -c CONFIDENCE, --confidence CONFIDENCE
                        Minumum confidence
  -s SUPPORT, --support SUPPORT
                        Minumum support

####Sample usage
> fetch_data.py -i 64 -c 0.5 -s 0.003
> Run rule mining for piwik site id 64 with apriori algorithm parameters being 0.5 confidence and 0.003 support

##site_executer.py
Main entry point to execute rule mining for frequently active sites (sites which were active yesterday). Script will iterate through sites and call fetch_data.py internally. 

usage: site_executer.py [-h] [-c CONFIDENCE] [-s SUPPORT]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIDENCE, --confidence CONFIDENCE
                        Minumum confidence
  -s SUPPORT, --support SUPPORT
                        Minumum support
####Sample usage
> site_executer.py -c 0.5 -s 0.003
> Run rule mining for piwik frequently active sites with apriori algorithm parameters being 0.5 confidence and 0.003 support