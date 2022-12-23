from datetime import datetime

from django.core.files.storage import default_storage
from money_track.firebase import storage


def upload_image_and_get_url(image, name=None):
    """Upload image to firebase and get corresponding url"""
    default_storage.save(image.name, image)
    file_name = str(datetime.now().time().strftime('%H.%M.%S'))
    path = storage.child("files/" + file_name + name).put(image.name)
    url = storage.child(
        "files/" + file_name + name).get_url(path['downloadTokens'])
    default_storage.delete(image.name)
    return url
