from datetime import datetime
from django.conf import settings
from django.core.files.storage import default_storage
import pyrebase

config = {
  "apiKey": settings.env('FIREBASE_API_KEY'),
  "authDomain": settings.env('FIREBASE_AUTH_DOMAIN'),
  "projectId": settings.env('FIREBASE_PROJECT_ID'),
  "storageBucket": settings.env('FIREBASE_BUCKET'),
  "messagingSenderId": settings.env('FIREBASE_SENDER_ID'),
  "appId": settings.env('FIREBASE_APP_ID'),
  "measurementId": settings.env('FIREBASE_MEASUREMENT_ID'),
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
