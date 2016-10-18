import base64
from datetime import datetime

from gallery.models import Picture


def import_fun():
    with open("1470892885_88_like.png", "rb") as imageFile:
        stri = base64.b64encode(imageFile.read())

    return stri


def add_to_picture():
    p = Picture(picture=import_fun(),id_user=1, date_of_add=datetime.now(),name_of_picture="like")
    p.save()




