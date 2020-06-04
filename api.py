from flask import Flask,request
import logging
import json
import requests
from elasticsearch import Elasticsearch
import uuid

app = Flask(__name__)
logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
log_format = logging.Formatter('%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
log_handler.setFormatter(log_format)
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

def Get_Location(ip):
    """
    Get Location from IP address by using IPStack api
    :param ip: remote ip address
    :return: all location details in json
    """
    api_key = "8ab4398aadc69b45094c83fce1701efc"
    api_uri = "http://api.ipstack.com/"
    full_api_uri = f"{ api_uri }{ ip }?access_key={ api_key }"
    response_location = requests.request("GET", full_api_uri)

    if response_location.status_code == 200:
        logger.info("Location was Found")
    else:
        logger.info(f"Doesn't get Client location, please see HTTP Error {response_location.status_code}")
    return response_location
def Write_To_Elasticsearch(obj):
    
    es = Elasticsearch(
        hosts=['elasticsearch'],
        port=9200
    )

    es.indices.create(index="api", ignore=400)
    es_response = es.index(
        index="api",
        id=uuid.uuid4(),
        body=obj)
    print(es_response['result'])

    return es_response
@app.route('/tracking', methods=['GET', 'POST'])
def tracking():
    product_type = request.args.get('type')
    product = request.args.get('product')
    usage =  request.args.get('usage')
    price =  request.args.get('price')
    currency =  request.args.get('currency')
    cl_ip = request.remote_addr
    Location = Get_Location(cl_ip)

    Jout = {
        "product_type": product_type,
        "product": product,
        "product_usage": usage,
        "product_price": price,
        "product_currency": currency,
        "client_ip": cl_ip,
        "client_continent":  Location.json()["continent_name"],
        "client_country": Location.json()["country_name"]
    }
    logger.info("Json Output was created ")
    Elastic_response = Write_To_Elasticsearch(Jout)

    if Elastic_response == 0:
        logger.info("Object was wrote to Elastic")

    return json.dumps(Jout, sort_keys=True, indent=4)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True, threaded=True)