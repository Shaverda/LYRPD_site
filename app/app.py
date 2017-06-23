import io
import sys
import time
import os
import socket
import json
import traceback

import httplib2
import multiprocessing


from flask import Flask, render_template, request, redirect, flash
from flask import send_from_directory
from flask_cors import CORS
import pygsheets
from googleplaces import GooglePlaces, GooglePlacesError

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
CORS(app)
google_places = GooglePlaces(MAPS_KEY)


def get_sheet(sheet_id):
    c = pygsheets.authorize(service_file=GOOGLE_CREDENTIALS)
    sheet = c.open_by_key(sheet_id)
    return sheet.worksheet_by_title('Sheet1')

        
sheet = get_sheet(SHEET)
last_update = None


def get_geo(name):
    time.sleep(0.5)  # sleep to avoid over quote in google places
    try:
        print('Getting geo location for {0}'.format(name), file=sys.stderr)
        query_result = google_places.text_search(
            location="Austin, Texas", radius=500, query=name)
        if len(query_result.places) > 1:
            print("Warning: got more than one place for '{0}'".format(name))
        if len(query_result.places) == 0:
            print("Got no results!")
            return '', '', ''
        place = query_result.places[0]
        return str(place.geo_location['lat']), str(place.geo_location['lng']), place.place_id
    except GooglePlacesError:
        print("Got an error from google places API:")
        traceback.print_exc()
        return '', '', ''


def get_data(sheet):
    records = sheet.get_all_records()
    for record in records:
        yield [record.get('Business name', ''), record.get('Facebook URL', ''),
               record.get('Website', ''), record.get('Info', ''),
               record.get('image name', ''), record.get('Category'),
               *get_geo(record.get('Geo Code'))
               ]


def create_data_file():
    data = list(get_data(sheet))
    with open('data.json', 'w') as f:
        json.dump(data, f)


def update():
    global last_update
    
    data = list(get_data(sheet))
    d = get_images.download_updated(last_update)
    if d:
        print('Refreshed images')
        last_update = d
    return data
        

def read_data():
    try:
        with open('data.json') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def read_images():
    global last_update
    
    d = get_images.download_updated(last_update)
    if d:
        print('Refreshed images')
        last_update = d
    

def read_everything():
    while True:
        create_data_file()
        read_images()
        time.sleep(5*60)


def read_in_process():
    reader = multiprocessing.Process(target=read_everything, name='reader')
    reader.start()


def start_reader():
    children = multiprocessing.active_children()
    for child in children:
        if child.name == 'reader':
            return
    read_in_process()

start_reader()

@app.route('/')
def main():
    data = read_data()
    return render_template(
        'index.html',
        maps_key=MAPS_KEY,
        data=json.dumps(data))
