import os
from oauth2client.file import Storage
from oauth2client import tools
from oauth2client import client

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

CREDENTIALS_DIRECTORY_NAME = '.credentialstest'
CLIENT_SECRET_FILE_NAME = 'client_secrets.json'
BASE_URL = 'https://www.googleapis.com/auth/'
SCOPE_LIST = ['https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/drive.appdata',
              'https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/drive.metadata',
              'https://www.googleapis.com/auth/drive.metadata.readonly',
              'https://www.googleapis.com/auth/drive.photos.readonly',
              'https://www.googleapis.com/auth/drive.readonly',
              'https://www.googleapis.com/auth/drive.scripts',
              'https://www.googleapis.com/auth/gmail.readonly',
              'https://www.googleapis.com/auth/gmail.compose',
              'https://www.googleapis.com/auth/gmail.send',
              'https://www.googleapis.com/auth/gmail.insert',
              'https://www.googleapis.com/auth/gmail.labels',
              'https://www.googleapis.com/auth/gmail.modify',
              'https://www.googleapis.com/auth/gmail.metadata',
              'https://www.googleapis.com/auth/gmail.settings.basic',
              'https://www.googleapis.com/auth/gmail.settings.sharing']


def get_credentials(scope):

    # Get the path of the home directory
    home_dir = os.path.expanduser('~')

    # Get the path of the .credentials folder in the home directory
    cred_dir = os.path.join(home_dir, CREDENTIALS_DIRECTORY_NAME)

    # Create the .credentials folder if it does not exist
    if not os.path.exists(cred_dir):
        os.makedirs(cred_dir)

    # Get the path of the clients_secret file
    clients_secret_path = os.path.join(cred_dir, CLIENT_SECRET_FILE_NAME)

    # Get the name of the credential file based on the scope's name
    cred_file_name = f"{scope.replace(BASE_URL, '').replace('.', '_')}.json"

    # Get the path of the credential file
    cred_file_path = os.path.join(cred_dir, cred_file_name)

    # Get the credentials
    store = Storage(cred_file_path)
    credentials = store.get()

    # Create the credentials if they don't exist
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(clients_secret_path, scope)
        flow.user_agent = 'Google API Python'
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
            result = f'The credentials file has to be created and stored here {cred_file_path}'
            print(result)

    return credentials
