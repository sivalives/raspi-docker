# -*- coding: utf-8 -*-
import requests
import concurrent.futures
from dropbox_utils_v2 import DropboxUtilsClass

'''
ZEE_CHANNELS = [
"0-9-zeetvhd",
"0-9-zeetalkies",
"0-9-zeeyuva",
"0-9-tvhd_0",
"0-9-bigmagic_1786965389",
"0-9-zeeanmol",
"0-9-250",
"0-9-zeecinemahd",
"0-9-channel_2105335046",
"0-9-tvpictureshd",
"0-9-zeeaction",
"0-9-zeeclassic",
"0-9-zeecinema",
"0-9-zeeanmolcinema",
"0-9-176",
"0-9-209",
"0-9-353",
"0-9-zing",
"0-9-133",
"0-9-134",
"0-9-privéhd",
"0-9-zeecafehd",
"0-9-channel_2105335046",
"0-9-296",
"0-9-390","0-9-411","0-9-ddindia","0-9-419","0-9-389","0-9-indiatoday","0-9-280","0-9-273","0-9-423","0-9-310","0-9-413","0-9-channel_1422341819","0-9-424","0-9-317","0-9-wion"
] 
'''

def get_zee_channel_ids(languages):
	channel_dict={}
	for lang in languages:
		channel_list_uri = "https://catalogapi.zee5.com/v1/channel/bygenre?sort_by_field=title&sort_order=ASC&genres=Movie,News,Entertainment,Devotional,Lifestyle,Music,Sports&country=IN&translation=en&languages={0}".format(lang)
		response = requests.get(url=channel_list_uri)
		#print response.json()
		for k1,v1 in response.json().items():
			for v2 in v1:
				for k2,v2 in v2.items():
					if isinstance(v2,list):
						if v2:
							for i in v2:
								#print   i.get("id"),i.get("title") 
								channel_dict[i.get("title")] = i.get("id")
	return channel_dict

'''
def create_m3u8_formatted_output(channel_dict):
	m3u8_format='#EXTINF:-1 tvg-id="{0}" tvg-name="{1}" tvg-log="" group-title-""'
	out=open(output_file,"w")
	out.write('$EXTM3U\n')
	#for channel_name, channel_id in channel_dict
	out.writelines()
'''


def get_zee5_m3u8s(channel_id):
	m3u8_format='#EXTINF:-1 tvg-id="{0}" tvg-name="{1}" tvg-logo="" group-title="",{1}\n{2}'
	ZEE_API="https://zee.avipatilpro.repl.co/?c={0}"
	channel_uri = ZEE_API.format(channel_id)
	response = requests.get(url=channel_uri)
	try:
		channel_name = [k for k in channel_dict.keys() if channel_dict[k] == channel_id]
	except:
		print (channel_id)
	#print channel_name[0],channel_id,
	x= m3u8_format.format(channel_id,channel_name[0],response.text)
	return x

if __name__ == "__main__":
	
	languages = ["ml","ta","en","hi"]
	channel_dict = get_zee_channel_ids(languages=languages)
	channel_ids = channel_dict.values()
	print("#EXTM3U")

	#Print to std out which will write to /iptv-volume/zee.m3u
	with concurrent.futures.ThreadPoolExecutor() as executor:
		results = executor.map(get_zee5_m3u8s,channel_ids)
		for i in results:
			print (i)

	#Copy to dropbox 
	dbx=DropboxUtilsClass()
	file_from="/iptv-volume/zee5.m3u"
	file_to='/links/zee5.m3u'
	dbx.upload_file(file_from,file_to)
