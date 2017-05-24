import sys
import time
import os
import socket
import json

from flask import Flask, render_template, request, redirect, flash
from flask import send_from_directory


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


data = [
        ["Peter Pan Mini Golf", "https://www.facebook.com/PeterPanMiniGolf/", "http://peterpanminigolf.com/", "make bandanas", "../static/images/peterpan.jpg"],
        ["ZACH Theatre", "https://www.facebook.com/zachtheatre/", "http://zachtheatre.org/", "conduct a play", "../static/images/zach.jpg"]
]

@app.route('/')
def main():
    return render_template(
        'index.html',
        maps_key=MAPS_KEY,
        data=json.dumps(data))
    #     sheet_link='https://docs.google.com/spreadsheets/d/{}'.format(SHEET),
    #     folder_link='https://drive.google.com/drive/u/1/folders/{}'.format(FOLDER)
    # )

@app.route('/download', methods=['POST'])
def download():
    return send_from_directory(directory='.', filename='out.pdf')

