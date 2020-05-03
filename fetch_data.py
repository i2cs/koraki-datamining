import requests
import mysql.connector
import datetime
from collections import defaultdict
import csv
import argparse
import json

from apriori import apriori

def run_rule_mining(siteid, confidence, support, conf):
    db = mysql.connector.connect(host=conf['mysql']['host'], port=conf['mysql']['port'], user=conf['mysql']['user'], passwd=conf['mysql']['password'], database=conf['mysql']['database'])
    cursor = db.cursor()
    
    response = requests.get(conf['piwik']['fetch_events'].replace('{{siteid}}', siteid))
    if response.status_code == 200:
        product_meta = {}
        data = response.json()
        if len(data) > 0:
            product_visits_count=0
            for visitor in data:
                for action in visitor['actionDetails']:
                    if action['type'] == 'event' and action['eventCategory'] == 'Product':
                        event = action['eventName'].split(' # ')
                        if len(event) == 4:
                            #print(siteid + ':' + visitor['visitorId'] + ':' + event[3])

                            if event[3] not in product_meta:
                                product_meta[event[3]] = { 'name': action['eventAction'], 'url': event[1], 'image': event[2] }

                            timestamp = datetime.datetime.fromtimestamp(action['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                            sql = "INSERT IGNORE INTO datamining_product_visits (siteid, visitor, item, action_time) VALUES (%s, %s, %s, %s)"
                            val = (siteid, visitor['visitorId'], event[3], timestamp)
                            cursor.execute(sql, val)
                            product_visits_count = product_visits_count+1
            db.commit()
            print(product_visits_count, " was inserted/updated to product_visits.")

            #print(product_meta)
            product_meta_count=0
            for product_id, product in product_meta.items():
                sql = "INSERT IGNORE INTO datamining_product_meta (siteid, product_id, product_name, product_url, product_image) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE product_name=%s, product_url=%s, product_image=%s, publish_time=CURRENT_TIMESTAMP"
                val = (siteid, product_id, product['name'], product['url'], product['image'], product['name'], product['url'], product['image'])
                cursor.execute(sql, val)
                product_meta_count = product_meta_count+1

            db.commit()
            print(product_meta_count, " was inserted/updated to product_meta.")

            data = defaultdict(set)
            sql = "select * from datamining_product_visits where siteid=" + siteid
            cursor.execute(sql)

            results = cursor.fetchall()

            for x in results:
              data[x[2]].add(x[3])

            results = list(apriori(data.values(), min_support = support, min_confidence = confidence, max_length = 2))

            sql = "delete from datamining_rules where siteid=" + siteid
            cursor.execute(sql)

            inserted_rule_count = 0;
            for x in results:
                for stats in x.ordered_statistics:
                    if len(stats.items_base) > 0:
                        sorted_keys = list(stats.items_base)
                        sorted_keys.sort()
                        base_items = ','.join(sorted_keys)
                        suggests = list(stats.items_add)
                        for suggestion in suggests:
                            sql = "INSERT IGNORE INTO datamining_rules (siteid, base_items, suggest, confidence) VALUES (%s, %s, %s, %s)"
                            val = (siteid, base_items, suggestion, stats.confidence)
                            #print(siteid, base_items, suggestion, stats.confidence)
                            cursor.execute(sql, val)
                            inserted_rule_count = inserted_rule_count + 1

            db.commit()
            print(inserted_rule_count, " was inserted to rules.")

    else:
        print "Failed to fetch from Analytics API"

    cursor.close()
    db.close ()
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser() 
    # Adding optional argument 
    parser.add_argument("-i", "--siteid", help = "Site id to fetch data from", required=True)
    parser.add_argument("-c", "--confidence", help = "Minumum confidence", type=float, default=0.5)
    parser.add_argument("-s", "--support", help = "Minumum support", type=float, default=0.003)
    args = parser.parse_args() 

    if args.siteid: 
        siteid = args.siteid
        
    with open("config.json", "r") as json_file:
        conf = json.load(json_file)
        
    run_rule_mining(siteid, args.confidence, args.support, conf)