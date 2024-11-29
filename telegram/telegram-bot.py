import os
import sys
import time
import telepot
from telepot.loop import MessageLoop
from dropbox_utils_v2 import DropboxUtilsClass
import lifx
import subprocess
import requests
from log2rabbitmq import publish2rmq
from datetime import datetime

def handle(msg):
    #Disabled Mongo
    #MONGO_URI = "http://{0}/telegram".format(os.environ["MONGO_HOSTNAME"])
    #data = {"telegram": msg}
    #res = requests.post(MONGO_URI,json=data) 

    data = {
        "post_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "job_name": "telegram",
        "job_status": "success", 
        "job_error": msg
    }
    rmq_data = {"queue": "fish","message":data}
    #Publish to Rabbit MQ for retrieval from splunk Asyc, as Mac might sleep all the time
    publish2rmq(rmq_data)

    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    dbx=DropboxUtilsClass()
    if content_type == 'text' and msg["text"].lower() == "/zee5" and str(chat_id) == os.environ["TELEGRAM_CHAT_ID"]:
        # let the human know that the pdf is on its way        
        bot.sendMessage(chat_id, "preparing iptv list for {0}, pls wait..".format(msg["text"].lower()))
        file="/iptv-volume/zee5.m3u"
        # send the pdf doc
        bot.sendDocument(chat_id=chat_id, document=open(file, 'rb'))
    elif content_type == 'text' and msg["text"].lower() == "/reboot" and str(chat_id) == os.environ["TELEGRAM_CHAT_ID"]:
        f=open("/iptv-volume/telegram_pi_instructions.txt","w")
        f.write("sudo reboot now")
        f.close()
        bot.sendMessage(chat_id, "Rebooting System")
    elif content_type == 'text' and msg["text"].lower() == "/speedtest" and str(chat_id) == os.environ["TELEGRAM_CHAT_ID"]:
        bot.sendMessage(chat_id, "Doing speed test..")
        cmd='speedtest --simple'
        speedresult = subprocess.check_output(cmd, shell=True)
        bot.sendMessage(chat_id, speedresult)
    elif content_type == 'text' and msg["text"].lower() == "/lifxon" and str(chat_id) == os.environ["TELEGRAM_CHAT_ID"]:
        bot.sendMessage(chat_id, "Enabling Lifx automation")
        if dbx.files_exist("disable_lifx_automation.txt"):
            dbx.delete_file("disable_lifx_automation.txt")
            bot.sendMessage(chat_id, "Deleted disable_lifx_automation.txt on Dropbox")
        data={"power":"on"}
        lifx.setState(os.environ["LIFX_BULB1_ID"],data)
        lifx.setState(os.environ["LIFX_BULB2_ID"],data)
        bot.sendMessage(chat_id, "Lights should be on now!")
    elif content_type == 'text' and msg["text"].lower() == "/lifxoff" and str(chat_id) == os.environ["TELEGRAM_CHAT_ID"]:
        bot.sendMessage(chat_id, "Disabling Lifx automation")
        data={"power":"off"}
        lifx.setState(os.environ["LIFX_BULB1_ID"],data)
        lifx.setState(os.environ["LIFX_BULB2_ID"],data)
        bot.sendMessage(chat_id, "Lights should be off now!")
        #Create a dummy file and write to dropbox; used by lifx automation container!!
        open("/tmp/disable_lifx_automation.txt", "w").close()
        dbx.upload_file("/tmp/disable_lifx_automation.txt","/links/disable_lifx_automation.txt")
        bot.sendMessage(chat_id, "Uploaded disable_lifx_automation.txt on Dropbox")
    elif content_type == 'text':
        bot.sendMessage(chat_id, "Sorry, You are not authorised!!")

if __name__ == '__main__':
    TOKEN = os.environ["TELEGRAM_BOTFATHER_APIKEY"]
    bot = telepot.Bot(TOKEN)
    MessageLoop(bot, handle).run_as_thread()
    print ('Listening ...')
    # Keep the program running.
    while 1:
        time.sleep(10)
