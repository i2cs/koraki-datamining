import requests
import argparse 
import fetch_data as runner
import json

parser = argparse.ArgumentParser() 


with open("config.json", "r") as json_file:
    conf = json.load(json_file)

# Adding optional argument 
parser.add_argument("-c", "--confidence", help = "Minumum confidence", type=float, default=conf['default']['confidence'])
parser.add_argument("-s", "--support", help = "Minumum support", type=float, default=conf['default']['support'])
args = parser.parse_args() 

response = requests.get(conf['piwik']['fetch_sites'])
if response.status_code == 200:
    data = response.json()
    if len(data) > 0:
        for site in data:
            print('Running for site ', site['label'])
            runner.run_rule_mining(str(site['idsite']), args.confidence, args.support, conf)