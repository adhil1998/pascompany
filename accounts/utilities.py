import pyrebase
import environ
from datetime import datetime
from django.core.files.storage import default_storage

env = environ.Env()
environ.Env.read_env()
config = {
  "apiKey": env('FIREBASE_API_KEY'),
  "authDomain": env('FIREBASE_AUTH_DOMAIN'),
  "projectId": env('FIREBASE_PROJECT_ID'),
  "storageBucket": env('FIREBASE_BUCKET'),
  "messagingSenderId": env('FIREBASE_SENDER_ID'),
  "appId": env('FIREBASE_APP_ID'),
  "measurementId": env('FIREBASE_MEASUREMENT_ID'),
  "databaseURL": "",
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


def upload_image_and_get_url(image, name=None):
    """Upload image to firebase and get corresponding url"""
    default_storage.save(image.name, image)
    file_name = str(datetime.now().time().strftime('%H.%M.%S'))
    path = storage.child("files/" + file_name + name).put(image.name)
    url = storage.child(
        "files/" + file_name + name).get_url(path['downloadTokens'])
    default_storage.delete(image.name)
    return url
