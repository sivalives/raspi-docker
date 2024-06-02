import os
import time
import lifx
from dropbox_utils_v2 import DropboxUtilsClass

hr=time.strftime('%H')
#Exclusion list : Add hours that light should be up
#Set in UTC if running on Docker !!
while True:
	time.sleep(3)
	dbx=DropboxUtilsClass()
	#If disable_lifx_automation.txt files exist in dropbox do not turn off lights 
	if not dbx.files_exist("disable_lifx_automation.txt"):
		#if disable file not exist , try to kill light if in NOT hours
		if  hr not in ('11','12','13','14','15','16','17'):
			print("Shutdown lifx")
			#Switch off lights
			data = {"power": "off"}
			
			lifx.setState(os.environ["LIFX_BULB1_ID"],data)
			lifx.setState(os.environ["LIFX_BULB2_ID"],data)
	else:
		print("Automation turned off")