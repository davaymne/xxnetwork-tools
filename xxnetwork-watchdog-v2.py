import psutil
import subprocess
import logging
import time
import requests
from requests.utils import quote
from requests.compat import urljoin

good_status = ['sleeping', 'idle', 'running', 'stopped']
api = 'https://protonet-api.xx.network/v1/nodes/'
node_id = 'MYqKI26Kc3KkJOMmF5n0tiwlSY/lhYCFYreTRh9c4NAC'

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)

def telegram_bot_sendtext(bot_msg):
    bot_token = '<>'
    bot_chatID = '<>'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_msg
    response = requests.get(send_text)
    return response.json()

def getStatus():
    status = []
    for p in psutil.process_iter(['name', 'status']):
        if p.info['name'].find('xxnetwork') >= 0 and p.info['status'] not in good_status:
            status.append(p.info)
    return status

def getNodeStatus(api):
    try:
        response = requests.get(api).json()
    except requests.exceptions.RequestException as e:
        logging.error('Can\'t get node {} status. Error: {}'.format(node_name, e))
    if response.get('error'):
        logging.error('Can\'t get node {} status. Response: {}'.format(node_name, response))
    return response

def parseResponse(response, node_id):
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
        if item['id'] == node_id:
            node_status = item['status']
    return online, offline, error, other, node_status

def restartProcess(cmd):
    try:
        print(cmd)
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(e.returncode)

while True:
    response = getNodeStatus(api)
    online, offline, error, other, node_status = parseResponse(response, node_id)
    online_rate = online / (online + offline + error + other)
    p_status_list = []
    p_status_list = getStatus()
    logging.info('XXNetwork: Node: davaymne, Process: {}. Node status is: {}. Overall offline is: {:.2%}.'.format(p_status_list, node_status, (1 - online_rate)))
    if len(p_status_list) > 0:
        for process in p_status_list:
            logging.info('XXNetwork: Node: davaymne, Process: {}, status: {}. Node status is: {}. Overall offline is: {:.2%} - restarting now.'.format(process['name'], process['status'], node_status, (1 - online_rate)))
            telegram_bot_sendtext('XXNetwork: Node: davaymne, Process: {}, status: {}. Node status is: {}. Overall offline is: {:.2%} - restarting now.'.format(process['name'], process['status'], node_status, (1 - online_rate)))
            restartProcess(["sudo", "/bin/systemctl", "restart", process['name']])
    time.sleep(600)
