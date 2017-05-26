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

import get_images


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


MAPS_KEY, SHEET, GOOGLE_CREDENTIALS = get_env_vars(
    'MAPS_KEY', 'SHEET', 'GOOGLE_CREDENTIALS')


app = Flask(__name__)


def get_sheet(sheet_id):
    c = pygsheets.authorize(service_file=GOOGLE_CREDENTIALS)
    sheet = c.open_by_key(sheet_id)
    return sheet.worksheet_by_title('Sheet1')

        
sheet = get_sheet(SHEET)
last_update = None


def get_data(sheet):
    records = sheet.get_all_records()
    for record in records:
        yield [record['Business name'], record['Facebook URL'],
               record['Website'], record['Activity'], record['image name']]
        

def update():
    global last_update
    
    data = list(get_data(sheet))
    d = get_images.download_updated(last_update)
    if d:
        print('Refreshed images')
        last_update = d
    return data
        

@app.route('/')
def main():
    data = update()
    return render_template(
        'index.html',
        maps_key=MAPS_KEY,
        data=json.dumps(data))