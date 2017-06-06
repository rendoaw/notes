# Simple Telegram Bot to Monitor Linux Server

## Background

This post is trying to document my telegram-based linux server monitoring script. 
My current problem is, i have a 1RU server at home that i need to monitor its temperature closely, especially during summer time like now.

Before creating the script that will be covered by this post, usually i have a cron-based script that will send an email alert when the condition exceed preconfigured threshold. Recently, i realized that my SMTP server is unstable and most of the time the email that sent from my server was blocked by Gmail because i don't have matching PTR and A record, which is an impossible requirement for me since i get a dynamic IP from my ISP and no control on the DNS PTR record. 
I fix the email problem by using Gmail as my relay server, by using SMTP+SSL authentication, but that's another story.

Even though i have the email alert working, this system lacks of feedback mechanism. After receiving the alert, if i want to check my server, i need to ssh to the server. When i am on the go, usually i use Juice SSH on my android to do that. This works but not that convenient if i simply need to send 1 or 2 commands. 
In the past, few years ago, before google talk become Hangout, i managed to have few "bot" based on google talk. All of them were stop working once Hangout is not fully XMPP compliant anymore. 

So, the script that will be covered here is my starting point to revive my old bot, but with a new backend: Telegram API.



## What the script do

The script will do the following

* Periodically monitor the server temperature

    * CPU temeprature is done by using LM sensors application

    * Room temperature is done by using usb based temperature sensor
        * https://github.com/rendoaw/notes/blob/master/linux/usb.temperature.sensor.md

* If the temperature exceed the threshold, send message to admin


* listen for any command send by the admin and run it as a shell command

    * Only admin can send command. Verification is done by checking sender username, user id and a simple password.
    
    * Any message received by unknown sender will be ignored.
    
    * syntax: "<password> <any linux command">
        * e.g: "mypassword ifconfig -a"


* Periodically send "i am alive" message to admin.

  * Telegram Bot has no online/offline status, so i simply ask the bot to tell me if it is still alive every few minutes.


## Pre-requisites

* You need to register your Telegram Bot and obtain the token 

    * https://core.telegram.org/bots

* You need to install the following modules

    *  telepot (http://telepot.readthedocs.io/en/latest/)

        ```
        # pip install telepot --upgrade
        ```


## The script

Here is the sample script, please adjust the parameter value accordingly ( they are marked with "SET THIS:")

```
#!/usr/bin/env python

import sys
import time
import telepot

import logging
import subprocess
from logging import handlers
from pprint import pprint
import re


reload(sys)
sys.setdefaultencoding('utf8')

def run_shell_command(cmd):
    logger.info("--> cmd line : "+cmd)
    response = ""
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in p.stdout.readlines():
        logger.info("--> output : "+str(line))
        response = response + str(line)
    logger.info("shell response : "+str(response))
    return response


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    #pprint(msg)
    parse = msg['text'].split(' ')
    if len(parse) < 2:
        logger.info("Invalid command")
        return
    passcode = msg['text'][0]
    cmd = msg['text'].split(' ', 1)[1]

    if msg['from']['username'] != admin_username and msg['from']['id'] != admin_uid and passcode == admin_passcode:
        logger.info("un-authorized command from: "+msg['from']['username']+" cmd: "+cmd)
        return

    if content_type == 'text':
        ret = run_shell_command(cmd)
        # max telegram message is 4096
        # https://core.telegram.org/method/messages.sendMessage
        if len(ret) > 4095:
            ret = ret[:4000]+"\n\n...message is truncated..."
        bot.sendMessage(chat_id, cmd+": "+ret)


def check_temperature_room():
    ret = run_shell_command("/usr/local/bin/pcsensor")
    parse = re.split("\s+", ret)
    logger.info(ret)
    if len(parse) > 4:
        temperature = int(float(parse[4].replace("C","")))
        if temperature > max_temperature_room_celcius:
            response = "Room Temperature ALERT !!!\nthreshold:"+str(max_temperature_room_celcius)+"C\n"+ret
            logger.info(response)
            return response
    return ""

def check_temperature_cpu():
    ret = run_shell_command("sensors -u | grep _input | awk '{print $2}' | sort | tail -1")
    temperature = int(float(ret))
    logger.info("highest cpu temperature: "+ret)
    if temperature > max_temperature_cpu_celcius:
        ret = run_shell_command("sensors")
        response = "CPU  Temperature ALERT !!!\nthreshold:"+str(max_temperature_cpu_celcius)+"C\n"+ret
        logger.info(response)
        return response
    return ""


def check_all():
    ret = check_temperature_room()
    if ret != "":
        bot.sendMessage(admin_uid, ret)
    ret = check_temperature_cpu()
    if ret != "":
        bot.sendMessage(admin_uid, ret)
    return





if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    LOG_FORMAT = "%(levelname) -10s %(asctime)s %(name) -15s %(funcName) -20s %(lineno) -5d: %(message)s"
    hdlr = handlers.RotatingFileHandler(filename='<SET THIS:Location of log file>', mode='a', maxBytes=100000000, backupCount=20, encoding='utf8')
    hdlr.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger().addHandler(hdlr)
    logging.getLogger().setLevel(logging.INFO)

    logger.info("Program started")

    # Adjust this section
    # -----------------------------------------------------------------
    TOKEN="<SET THIS: Your Bot Token>"
    admin_uid = <SET THIS: Your UID, integer, you can get it by uncomment the pprint command inside handle function above>
    admin_username =  "<SET THIS: Your username, string, you can get it by uncomment the pprint command inside handle function above>"
    admin_passcode = "<SET THIS: any single word, does not support space yet>"
    interval = <SET THIS: how frequent you want to run the checking, integer>
    max_temperature_room_celcius = <SET THIS, max threshold for room temperature, integer>
    max_temperature_cpu_celcius = <SET THIS, max threshold for CPU temperature, integer>
    # -----------------------------------------------------------------

    bot = telepot.Bot(TOKEN)
    bot.message_loop(handle)
    print ('Listening ...')
    bot.sendMessage(admin_uid, "bot is started")

    # Keep the program running.
    starttime=int(time.time())
    while 1:
        curtime = int(time.time())
        if curtime - starttime > interval:
            bot.sendMessage(admin_uid, "I am alive")
            check_all()
            starttime=int(time.time())
        time.sleep(10)
```


## Optional Steps

To make sure the script is started during power-on and auto-restarted if it crash for any reason, i am using supervisord to monitor the script.
In general, i did the following:

* Install supervisord

    ```
    # apt-get install -y supervisor
    # service supervisor start
    ```

* add configuration file for my bot

    ```
    # cat /etc/supervisor/conf.d/bot.conf
    [program:bot]
    command=/home/rendo/telepot/bin/python /home/rendo/scripts/bot.py
    autostart=true
    autorestart=true
    startretries=3
    stderr_logfile=/home/rendo/logs/bot.supervisor.err.log
    stdout_logfile=/home/rendo/logs/bot.supervisor.log
    user=root
    ```

* activate supervisord monitoring for this script

    ```
    # supervisorctl reread
    # supervisorctl update
    ```


## Limitation

* The script currently only support direct chat. 
    * It can be improved to have a callback mechanism so multiple user can interact with the bot at the same time, and we can include the bot into a telegram group.
* The security is very minimum right now, it only check if the sender ID and username match to a specific value and the passcode (which is the first word of the received message) is matched.
    * Potential improvement:
        * hash the password value
        * support multiple admin
        * ...



## resources:

* https://core.telegram.org/bots
* https://github.com/nickoala/telepot
* http://telepot.readthedocs.io/en/latest/
* https://serversforhackers.com/monitoring-processes-with-supervisord
