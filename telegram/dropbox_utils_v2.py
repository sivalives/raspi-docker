import dropbox
import os

class DropboxUtilsClass(object):
    def __init__(self):
        # Initialize Dropbox client using app key, app secret, and refresh token from environment variables
        self.dbx = dropbox.Dropbox(
            app_key=os.environ["DROPBOX_APP_KEY"],
            app_secret=os.environ["DROPBOX_APP_SECRET"],
            oauth2_refresh_token=os.environ["DROPBOX_REFRESH_TOKEN"]
        )

    def upload_file(self, file_from, file_to):
        print("Updating file {0} in Dropbox".format(file_to))
        # Open the file in binary read mode
        with open(file_from, 'rb') as f:
            # Overwrite file in Dropbox to retain the shared link with every write
            self.dbx.files_upload(
                f.read(),
                file_to,
                mode=dropbox.files.WriteMode('overwrite')
            )

    def delete_file(self, file):
        file_path = f"/lifx/{file}"
        print(f"Deleting file {file_path} from Dropbox")
        self.dbx.files_delete(file_path)

    def file_exists(self, filename):
        print(f"Checking if file {filename} exists in Dropbox")
        try:
            files = self.dbx.files_list_folder(path="/lifx").entries
            return filename in [f.name for f in files]
        except dropbox.exceptions.ApiError as e:
            print(f"Error listing files: {e}")
            return False

'''
if __name__ == '__main__':
    dbx = DropboxUtilsClass()
    file_from = "switch_off_lifx"
    file_to = '/lifx/switch_off_lifx'
    dbx.upload_file(file_from, file_to)
    dbx.delete_file("test.py")
    dbx.file_exists("switch_off_lifx.txt")
'''
