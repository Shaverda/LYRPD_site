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


SHEET, FOLDER = get_env_vars('SHEET', 'FOLDER')


app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'apa!'
)


@app.route('/')
def main():
    return render_template(
        'index.html')
    #     sheet_link='https://docs.google.com/spreadsheets/d/{}'.format(SHEET),
    #     folder_link='https://drive.google.com/drive/u/1/folders/{}'.format(FOLDER)
    # )

@app.route('/download', methods=['POST'])
def download():
    return send_from_directory(directory='.', filename='out.pdf')

