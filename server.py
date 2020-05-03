from flask import Flask
from flask_restful import Resource, Api
from waitress import serve
from flask_restful import reqparse
import mysql.connector
import json

app = Flask(__name__)
api = Api(app)

class KorakiMarketBasketAnalysis(Resource):
    def __init__(self): 
        with open("config.json", "r") as json_file:
            conf = json.load(json_file)
        self.db = mysql.connector.connect(host=conf['mysql']['host'], port=conf['mysql']['port'], user=conf['mysql']['user'], passwd=conf['mysql']['password'], database=conf['mysql']['database'])
        self.cursor = self.db.cursor()
        
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('site_id', type=int, help='Site id as in piwik analytics server', required=True)
        parser.add_argument('item_id', type=int, help='Item id to request matching rules', required=True)
        args = parser.parse_args()
        
        sql = "SELECT r.suggest as product_id, r.confidence, m.product_name, m.product_url, m.product_image, r.created_time  FROM `datamining_rules` as r,`datamining_product_meta` as m WHERE r.suggest=m.product_id AND r.siteid=m.siteid AND r.base_items=%s AND r.siteid=%s order by r.confidence DESC limit 10"
        self.cursor.execute(sql, (args.item_id, args.site_id, ))
        results = self.cursor.fetchall()
        
        data = []
        for result in results:
            data.append({ 'product_id': result[0], 'confidency': result[1], 'product_name': result[2], 'product_url': result[3], 'product_image': result[4], 'publish_time': str(result[5]) })
        
        return data

    
api.add_resource(KorakiMarketBasketAnalysis, '/')    

if __name__ == '__main__':
    with open("config.json", "r") as json_file:
            conf = json.load(json_file)
            
    serve(app, host=conf['webservice']['host'], port=conf['webservice']['port'])
