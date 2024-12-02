import os
import sys
import time
import json
import telepot
from telepot.loop import MessageLoop
from dropbox_utils_v2 import DropboxUtilsClass
import lifx
import subprocess
import requests
from log2rabbitmq import publish2rmq
from datetime import datetime

def handle(msg):
    #payload for Rabbit MQ and store in telegram kvstore
    data = {
        "post_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "status": "",
        "raspberry_response": "",
        "from_username": msg.get("from", {}).get("username", "unknown"),
        "from_firstname": msg.get("from", {}).get("first_name", "unknown"),
        "from_id": msg.get("from", {}).get("id", "unknown"),
        "from_lang_code": msg.get("from", {}).get("language_code", "unknown"),
        "from_command": msg.get("text", "unknown"),
        "type": msg.get("chat", {}).get("type", "unknown"),
        "message_id": msg.get("message_id", "unknown"),
        "payload": json.dumps(msg),
    }

    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    dbx=DropboxUtilsClass()
    if content_type == 'text' and msg["text"].lower() == "/zee5" and str(chat_id) == os.environ["TELEGRAM_CHAT_ID"]:
        # let the human know that the pdf is on its way        
        bot.sendMessage(chat_id, "preparing iptv list for {0}, pls wait..".format(msg["text"].lower()))
        file="/iptv-volume/zee5.m3u"
        #Publish to Rabbit MQ for retrieval from splunk Asyc, as Mac might sleep all the time
        data["status"] = "success"
        publish2rmq(data)
        # send the pdf doc
        bot.sendDocument(chat_id=chat_id, document=open(file, 'rb'))
    elif content_type == 'text' and msg["text"].lower() == "/reboot" and str(chat_id) == os.environ["TELEGRAM_CHAT_ID"]:
        f=open("/iptv-volume/telegram_pi_instructions.txt","w")
        f.write("sudo reboot now")
        f.close()
 
        #Publish to Rabbit MQ for retrieval from splunk Asyc, as Mac might sleep all the time
        data["status"] = "success"
        publish2rmq(data)
 
        bot.sendMessage(chat_id, "Rebooting System")
    elif content_type == 'text' and msg["text"].lower() == "/speedtest" and str(chat_id) == os.environ["TELEGRAM_CHAT_ID"]:
        bot.sendMessage(chat_id, "Doing speed test..")
        cmd='speedtest --simple'
        speedresult = subprocess.check_output(cmd, shell=True)
        data["status"] = "success"
        data["raspberry_response"] = speedresult
        publish2rmq(data)
        bot.sendMessage(chat_id, speedresult)
    elif content_type == 'text' and msg["text"].lower() == "/lifxon" and str(chat_id) == os.environ["TELEGRAM_CHAT_ID"]:
        bot.sendMessage(chat_id, "Enabling Lifx automation")
        try:
            if dbx.files_exist("disable_lifx_automation.txt"):
                dbx.delete_file("disable_lifx_automation.txt")
                bot.sendMessage(chat_id, "Deleted disable_lifx_automation.txt on Dropbox")
            data={"power":"on"}
            res1=lifx.setState(os.environ["LIFX_BULB1_ID"],data)
            res2=lifx.setState(os.environ["LIFX_BULB2_ID"],data)
            status="success"
        except Exception as e:
            res1="error"
            res2="error"
            status="error"
 
        #Publish to Rabbit MQ for retrieval from splunk Asyc, as Mac might sleep all the time
        data["status"] = status
        result = {"bulb1" : res1, "bulb2": res2}
        data["raspberry_response"] = json.dumps(result)
        publish2rmq(data)
 
        bot.sendMessage(chat_id, "Lights should be on now!")
    elif content_type == 'text' and msg["text"].lower() == "/lifxoff" and str(chat_id) == os.environ["TELEGRAM_CHAT_ID"]:
        bot.sendMessage(chat_id, "Disabling Lifx automation")
        data={"power":"off"}
        res1=lifx.setState(os.environ["LIFX_BULB1_ID"],data)
        res2=lifx.setState(os.environ["LIFX_BULB2_ID"],data)
        bot.sendMessage(chat_id, "Lights should be off now!")
        #Create a dummy file and write to dropbox; used by lifx automation container!!
        open("/tmp/disable_lifx_automation.txt", "w").close()
        dbx.upload_file("/tmp/disable_lifx_automation.txt","/links/disable_lifx_automation.txt")

        #Publish to Rabbit MQ for retrieval from splunk Asyc, as Mac might sleep all the time
        data["status"] = "success"
        result = {"bulb1" : res1, "bulb2": res2}
        data["raspberry_response"] = json.dumps(result)
        publish2rmq(data)
     
        bot.sendMessage(chat_id, "Uploaded disable_lifx_automation.txt on Dropbox")
    elif content_type == 'text':
        msg="Sorry, You are not authorised!!"
        #Publish to Rabbit MQ for retrieval from splunk Asyc, as Mac might sleep all the time
        data["status"] = "unauthorized"
        data["raspberry_response"] = msg

        #Publish to Rabbit MQ for retrieval from splunk Asyc, as Mac might sleep all the time
        publish2rmq(data)
 
        bot.sendMessage(chat_id, msg)

if __name__ == '__main__':
    TOKEN = os.environ["TELEGRAM_BOTFATHER_APIKEY"]
    bot = telepot.Bot(TOKEN)
    MessageLoop(bot, handle).run_as_thread()
    print ('Listening ...')
    # Keep the program running.
    while 1:
        time.sleep(10)
