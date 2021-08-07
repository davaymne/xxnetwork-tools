# xxnetwork-watchdog

Python3 script to check whether processes `xxnetwork-node` and `xxnetwork-gateway` are zombie (aka defunct) and restart services 

* `xxnetwork-node`
* `xxnetwork-gateway`.

# Requirements

## Python3 packages
pip3 install -r requirements.txt
sudo apt-get install python3-psutil

## Telegram bot
@BotFather - https://core.telegram.org/bots

# Usage
1. Modify files with your path to watchdog script and python3 and systemctl bin files
2. Copy `xxnetwork-watchdog.py` on you server in any directory
3. Copy `xxnetwork-watchdog.service` to the `/etc/systemd/system/xxnetwork-watchdog.service`
4. Enable service `sudo systemctl enable xxnetwork-gateway.service`

# How to check service status
`sudo systemctl status xxnetwork-watchdog.service`

# How to restart watchdog service
`sudo systemctl service xxnetwork-watchdog.service`
