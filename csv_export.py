import pandas
import os
import json
import base64
from google.cloud import bigquery
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime as _datetime
import pandas_gbq
import urllib.parse
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from dotenv import load_dotenv

load_dotenv()

def export_data():

    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'files.json'))

    data = json.load(f)

    print(data)

    print(_datetime.now())

    drive_project_id = os.environ['DRIVE_PROJECT_ID']
    drive_cred_password = os.environ['DRIVE_CRED_PASSWORD'].replace('\\n', '\n')
    drive_cred_username = os.environ['DRIVE_CRED_USERNAME']
    drive_key_id = os.environ['DRIVE_KEY_ID']
    drive_client_id = os.environ['DRIVE_CLIENT_ID']

    drive_cred = {
        "type": "service_account",
        "private_key_id":drive_key_id,
        "project_id": drive_project_id,
        "private_key": drive_cred_password,
        "client_email": drive_cred_username,
        "client_id":drive_client_id,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/"+urllib.parse.quote(drive_cred_username)
    }

    scope = ['https://www.googleapis.com/auth/drive']
    drive_credentials = ServiceAccountCredentials.from_json_keyfile_dict(drive_cred, scope)

    gauth = GoogleAuth()
    gauth.credentials = drive_credentials
    drive = GoogleDrive(gauth)

    client = bigquery.Client()

    for d in data:
        if d['overwrite'] == True:
            query = "'"+d['folder']+"' in parents"

            print(query)

            file_list = drive.ListFile({'q': query}).GetList()
            for f in file_list:
                if f['title']==d['name']:
                    f.Trash()

        df = (
            client.query(d['query'])
            .result()
            .to_dataframe(
            )
        )

        file1 = drive.CreateFile({'title': d['name']+".csv",'parents': [{'id': d['folder']}]})
        file1.SetContentString(df.to_csv(index=False))
        file1.Upload()



if __name__ == "__main__":
    export_data()
