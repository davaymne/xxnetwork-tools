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
        help='XX network Node ID, e.g. MYqKI26Kc3KkJOMmF5n0tiwlSY/lhYCFYreTRh9c4NAC’,
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

# Use @BotFather to create telegram bot and group
def telegram_bot_sendtext(bot_msg):
    bot_token = ‘<YOUR TOKEN>’
    bot_chatID = ‘<YOUR CHAT ID>’
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_msg
    response = requests.get(send_text)
    return response.json()


def getNodeStatus(api, node_id, node_name):
    node_id_parsed = quote(node_id, safe='')
    node_status_api = urljoin(api, node_id_parsed)
    try:
        response = requests.get(node_status_api).json()
    except requests.exceptions.RequestException as e:
        logging.error('Can\'t get node {} status. Error: {}'.format(node_name, e))
    if response.get('error'):
        logging.error('Can\'t get node {} status. Response: {}'.format(node_name, response))
    logging.info('XX Node: {} status: {}'.format(node_name, response['node']['status']))
    return response['node']['status']


def main():
    while True:
        args = parseArguments()
        status = getNodeStatus(args.api, args.node_id, args.node_name)
        if status != 'online':
            telegram_bot_sendtext('XXNetwork: Node {} status is {}'.format(args.node_name, status))
        time.sleep(5)

if __name__ == "__main__":
    main()
