import os
import time
import json
import telepot
from telepot.loop import MessageLoop
from dropbox_utils_v2 import DropboxUtilsClass
import lifx
import subprocess
from log2rabbitmq import publish2rmq
from datetime import datetime

# Initialize global variables
TOKEN = os.environ["TELEGRAM_BOTFATHER_APIKEY"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
LIFX_BULB1_ID = os.environ["LIFX_BULB1_ID"]
LIFX_BULB2_ID = os.environ["LIFX_BULB2_ID"]
bot = telepot.Bot(TOKEN)
ROUTING_KEY_TELEGRAM="telegram"
ROUTING_KEY_TEST="test"

def create_data_payload(msg, status, raspberry_response=""):
    """Creates a fresh data payload."""
    return {
        "post_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "status": status,
        "raspberry_response": raspberry_response,
        "from_username": msg.get("from", {}).get("username", "unknown"),
        "from_firstname": msg.get("from", {}).get("first_name", "unknown"),
        "from_id": msg.get("from", {}).get("id", "unknown"),
        "from_lang_code": msg.get("from", {}).get("language_code", "unknown"),
        "from_command": msg.get("text", "unknown"),
        "type": msg.get("chat", {}).get("type", "unknown"),
        "message_id": msg.get("message_id", "unknown"),
        "payload": json.dumps(msg),
    }

def send_message(chat_id, message):
    """Sends a message to the user."""
    bot.sendMessage(chat_id, message)

def handle_command_zee5(chat_id, data):
    """Handles the /zee5 command."""
    send_message(chat_id, "Preparing IPTV list, please wait...")
    file_path = "/iptv-volume/zee5.m3u"
    data["status"] = "success"
    publish2rmq(ROUTING_KEY_TELEGRAM,data)
    bot.sendDocument(chat_id=chat_id, document=open(file_path, 'rb'))

def handle_command_fishfeed(chat_id, data):
    """Handles the /fishfeed command."""
    send_message(chat_id, "fish feeding please wait...")
    fish_result = subprocess.check_output('docker exec -it fish-feeder python3 bin/fish/servo_motor_180.py', shell=True).decode()
    data["raspberry_response"] = fish_result
    data["status"] = "success"
    publish2rmq(ROUTING_KEY_TELEGRAM,data)
    send_message(chat_id, "fish feeding complete")

def handle_command_rabbitmq(chat_id, data):
    """Handles the /rabbitmq command."""
    for i in range(1000):
        publish2rmq(ROUTING_KEY_TEST,data)
    data["status"] = "success"
    send_message(chat_id, "Added 1000 messages to RMQ TEST Queue")

def handle_command_reboot(chat_id, data):
    """Handles the /reboot command."""
    with open("/iptv-volume/telegram_pi_instructions.txt", "w") as f:
        f.write("sudo reboot now")
    data["status"] = "success"
    publish2rmq(ROUTING_KEY_TELEGRAM,data)
    send_message(chat_id, "Rebooting system...")

def handle_command_speedtest(chat_id, data):
    """Handles the /speedtest command."""
    send_message(chat_id, "Performing speed test...")
    try:
        speed_result = subprocess.check_output('speedtest --simple', shell=True).decode()
        data["status"] = "success"
        data["raspberry_response"] = speed_result
        publish2rmq(ROUTING_KEY_TELEGRAM,data)
        send_message(chat_id, speed_result)
    except Exception as e:
        send_message(chat_id, f"Speed test failed: {e}")

def handle_lifx(chat_id, data, power_state, message_on_success):
    """Handles LIFX commands with error handling for invalid or missing responses."""
    dbx = DropboxUtilsClass()
    data["status"] = "success"
    result = {}

    def set_light_state(bulb_id, power_state):
        """Attempts to set the state of a LIFX bulb and handles errors."""
        try:
            response = lifx.setState(bulb_id, {"power": power_state})
            if response and isinstance(response, dict):
                bulb_result = response.get("results", [{}])[0]
                label = bulb_result.get("label", "Unknown")
                status = bulb_result.get("status", "error")
                return label, "ok" if status == "ok" else "error"
            return "Unknown", "error"
        except Exception as e:
            print(f"Error setting light state for bulb {bulb_id}: {e}")
            return "Unknown", "error"

    # Set state for bulb1
    label1, status1 = set_light_state(os.environ["LIFX_BULB1_ID"], power_state)
    result[label1] = status1

    # Set state for bulb2
    label2, status2 = set_light_state(os.environ["LIFX_BULB2_ID"], power_state)
    result[label2] = status2

    # Update status based on results
    if "error" in result.values():
        data["status"] = "error"

    if power_state == "off":
        disable_file = "/tmp/disable_lifx_automation.txt"
        open(disable_file, "w").close()
        dbx.upload_file(disable_file, "/lifx/disable_lifx_automation.txt")

    data["raspberry_response"] = json.dumps(result)
    publish2rmq(ROUTING_KEY_TELEGRAM,data)

    # Send status messages for each bulb
    for bulb_label, status in result.items():
        bot.sendMessage(chat_id, f"{bulb_label} bulb: {'Success' if status == 'ok' else 'Error'}")


def handle(msg):
    """Main handler for Telegram messages."""
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        return

    command = msg["text"].lower()
    if str(chat_id) != CHAT_ID:
        unauthorized_msg = "Sorry, you are not authorized!"
        data = create_data_payload(msg, "unauthorized", unauthorized_msg)
        publish2rmq(ROUTING_KEY_TELEGRAM,data)
        send_message(chat_id, unauthorized_msg)
        return

    data = create_data_payload(msg, "pending")
    if command == "/zee5":
        handle_command_zee5(chat_id, data)
    elif command == "/rabbitmq":
        handle_command_rabbitmq(chat_id, data)
    elif command == "/reboot":
        handle_command_reboot(chat_id, data)
    elif command == "/speedtest":
        handle_command_speedtest(chat_id, data)
    elif command == "/lifxon":
        handle_lifx(chat_id, data, "on", "Lights should be on now!")
    elif command == "/lifxoff":
        handle_lifx(chat_id, data, "off", "Lights should be off now!")
    elif command == "/fishfeed":
        handle_command_fishfeed(chat_id, data)
        send_message(chat_id, "will try fish feeding 1 more time in 10 seconds")
        time.sleep(10)
        handle_command_fishfeed(chat_id, data)
    else:
        unknown_command_msg = "Unknown command received!"
        data["status"] = "unknown_command"
        data["raspberry_response"] = unknown_command_msg
        publish2rmq(ROUTING_KEY_TELEGRAM,data)
        send_message(chat_id, unknown_command_msg)

if __name__ == '__main__':
    MessageLoop(bot, handle).run_as_thread()
    print("Listening...")
    while True:
        time.sleep(10)

