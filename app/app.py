import io
import sys
import time
import os
import socket
import json
import httplib2

from flask import Flask, render_template, request, redirect, flash
from flask import send_from_directory
import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseDownload
from apiclient import discovery


def get_env_vars(*names):
    missing = []
    for name in names:
        try:
            yield os.environ[name]
        except KeyError:
            missing.append(name.upper())
    if missing:
        print('Environment variables {0} are needed'.format(', '.join(missing)))
        sys.exit(1)


MAPS_KEY, SHEET, FOLDER, GOOGLE_CREDENTIALS = get_env_vars(
    'MAPS_KEY', 'SHEET', 'FOLDER', 'GOOGLE_CREDENTIALS')


app = Flask(__name__)


def get_sheet(sheet_id):
    c = pygsheets.authorize(service_file=GOOGLE_CREDENTIALS)
    sheet = c.open_by_key(sheet_id)
    return sheet.worksheet_by_title('Sheet1')

def get_drive():
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_CREDENTIALS, scopes=['https://www.googleapis.com/auth/drive'])
    http = creds.authorize(httplib2.Http())
    return discovery.build('drive', 'v3', http=http)


def get_picture(drive, folder, name):
    q = "'{folder}' in parents and not trashed".format(folder=folder)
    files = drive.files().list(
        q=q, fields='files(description,id,name)').execute()
    for file in files['files']:
        name, _ = os.path.splitext(file['name'])
        if name == name:
            target = os.path.join('static/images', file['name'])
            download(drive, file['id'], target)
            return target
    raise Exception(name)


def download(drive, file_id, target):
    request = drive.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    with open(target, 'w+b') as out:
        out.write(fh.getvalue())

        
sheet = get_sheet(SHEET)


def get_data(sheet):
    records = sheet.get_all_records()
    for record in records:
        yield [record['Business name'], record['Facebook URL'],
               record['Website'], record['Activity'], record['image name']]
        

@app.route('/')
def main():
    data = list(get_data(sheet))
    return render_template(
        'index.html',
        maps_key=MAPS_KEY,
        data=json.dumps(data))
    #     sheet_link='https://docs.google.com/spreadsheets/d/{}'.format(SHEET),
    #     folder_link='https://drive.google.com/drive/u/1/folders/{}'.format(FOLDER)
    # )


