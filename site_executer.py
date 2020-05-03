import requests
import argparse 
import fetch_data as runner

parser = argparse.ArgumentParser() 
  
# Adding optional argument 
parser.add_argument("-c", "--confidence", help = "Minumum confidence", type=float, default=0.5)
parser.add_argument("-s", "--support", help = "Minumum support", type=float, default=0.003)
args = parser.parse_args() 


response = requests.get('https://analytics.koraki.io/index.php?module=API&method=MultiSites.getAll&period=day&date=yesterday&format=JSON&showColumns=&token_auth=10ce40d31a4bb14767e790f376782543')
if response.status_code == 200:
    data = response.json()
    if len(data) > 0:
        for site in data:
            print('Running for site ', site['label'])
            runner.run_rule_mining(str(site['idsite']), args.confidence, args.support)