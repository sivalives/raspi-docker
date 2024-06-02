import dropbox
import os

class DropboxUtilsClass(object):
	def __init__(self):
		self.dbx=dropbox.Dropbox('CbXmj_hVWRQAAAAAAAAJkdh7Ils1L1dPUq--XD5GIFr_lZC7MZtb6EIFFSn_SENT')

	def upload_file(self,file_from, file_to):
		print ("Updating file {0} in dropbox".format(file_to))
		f = open(file_from, 'rb')
		#Overwrite file in dropbox so that the shared link is retained with every write!!
		self.dbx.files_upload(f.read(), file_to,dropbox.files.WriteMode('overwrite', None))

	def delete_file(self,file):
		self.dbx.files_delete("/links/{0}".format(file))

	def files_exist(self, filename):
		files = self.dbx.files_list_folder(path=os.path.dirname("/links/")).entries
		return filename in [ f.name for f in files ]

#if __name__ == '__main__':
	#dbx=DropboxUtilsClass()
	#file_from="switch_off_lifx"
	#file_to='/links/switch_off_lifx'
	#dbx.upload_file(file_from,file_to)
	#dbx.delete_file("test.py")
	#dbx.file_exists("switch_off_lifx.txt")
