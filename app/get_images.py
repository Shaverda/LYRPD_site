import datetime
import httplib2
import io
import os

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseDownload
from apiclient import discovery
from PIL import Image


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


FOLDER, GOOGLE_CREDENTIALS = get_env_vars(
    'FOLDER', 'GOOGLE_CREDENTIALS')


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


def list_updated(drive, folder, since=None):
    if since is None:
        since = datetime.datetime.fromtimestamp(0)
    q = "'{FOLDER}' in parents and modifiedTime > '{SINCE}'".format(
        FOLDER=folder,
        SINCE=since.isoformat())
    files = drive.files().list(
        q=q, fields='files(description,id,name)').execute()
    if not files['files']:
        return

    q = "'{FOLDER}' in parents and not trashed".format(FOLDER=folder)
    files = drive.files().list(
        q=q, fields='files(description,id,name)').execute()

    for file in files['files']:
        yield file
    

def download(drive, file_id, target):
    request = drive.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    with open(target, 'w+b') as out:
        out.write(fh.getvalue())


def download_new(drive, folder, last_update=None):
    updated = list(list_updated(drive, folder, last_update))
    for file in updated:
        target = os.path.join('static/images', file['name'])
        download(drive, file['id'], target)
        # crop(target)
    
    if updated:
        return datetime.datetime.utcnow()


def make_square(h, w):
    if h <= w:
        return ((w-h)/2, 0, w-(w-h)/2, h)
    else:
        return (0, (h-w)/2, w, h-(h-w)/2)

    
def crop(target):
    print("Cropping")
    img = Image.open(target)
    img = img.crop(make_square(img.height, img.width))
    img.save(target)
    

def download_updated(last_update=None):
    drive = get_drive()
    return download_new(drive, FOLDER, last_update)
