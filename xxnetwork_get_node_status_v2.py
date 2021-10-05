#!/usr/bin/env python3
import argparse
import json
import logging
import requests
import time
from requests.utils import quote
from requests.compat import urljoin

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--node-id',
        dest='node_id',
        help='XX network Node ID',
        default='MYqKI26Kc3KkJOMmF5n0tiwlSY/lhYCFYreTRh9c4NAC',
        type=str)
    parser.add_argument('--node-name',
        dest='node_name',
        help='XX network Node Name',
        default='davaymne',
        type=str)
    parser.add_argument('--api',
        dest='api',
        help='XX network API (default: %(default)s)',
        default='https://protonet-api.xx.network/v1/nodes/',
        type=str)
    return parser.parse_args()

def telegram_bot_sendtext(bot_msg):
    bot_token = '<>'
    bot_chatID = '<>'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_msg
    response = requests.get(send_text)
    return response.json()


def getNodeStatus(api):
    try:
        response = requests.get(api).json()
    except requests.exceptions.RequestException as e:
        logging.error('Can\'t get node {} status. Error: {}'.format(node_name, e))
    if response.get('error'):
        logging.error('Can\'t get node {} status. Response: {}'.format(node_name, response))
    return response

def parseResponse(response, args):
    counter = error = offline = online = other = 0
    for item in response['nodes']:
        counter = counter + 1
        if item['status'] == 'online':
            online = online + 1
        elif item['status'] == 'offline':
            offline = offline + 1
        elif item['status'] == 'error':
            error = error + 1
        else: other = other + 1
        if item['id'] == args.node_id:
            node_status = item['status']
    return online, offline, error, other, node_status


def main():
    while True:
        args = parseArguments()
        response = getNodeStatus(args.api)
        online, offline, error, other, node_status = parseResponse(response, args)
        online_rate = online / (online + offline + error + other)
        if node_status != 'online':
            logging.info('XXNetwork: Node {} status is {}. Overall online is {:.2%}'.format(args.node_name, node_status, online_rate))
            telegram_bot_sendtext('XXNetwork: Node {} status is {}. Overall online is {:.2%}'.format(args.node_name, node_status, online_rate))
        time.sleep(600)

if __name__ == "__main__":
    main()
