import psutil
import subprocess
import time
import requests

good_status = ['sleeping', 'idle', 'running', 'stopped']

def telegram_bot_sendtext(bot_msg):
    bot_token = 'YOUR TOKEN'
    bot_chatID = 'YOU CHAT ID'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_msg
    response = requests.get(send_text)
    return response.json()

def getStatus():
    status = []
    for p in psutil.process_iter(['name', 'status']):
        if p.info['name'].find('xxnetwork') >= 0 and p.info['status'] not in good_status:
            status.append(p.info)
    return status

def restartProcess(cmd):
    try:
        print(cmd)
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(e.returncode)

while True:
    p_status_list = []
    p_status_list = getStatus()
    if len(p_status_list) > 0:
        for process in p_status_list:
            telegram_bot_sendtext('Process: {}, status: {} - restarting now.'.format(process['name'], process['status']))
            restartProcess(["sudo", "/bin/systemctl", "restart", process['name']])
    time.sleep(300)
