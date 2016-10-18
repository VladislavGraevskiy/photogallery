import base64
from io import BytesIO
import io


from PIL import Image
from gallery.models import Picture, Likes

from loginer.models import User


def get_user(id_user):
    """get user object using id_user"""
    try:
        user = User.objects.get(id_users=id_user)
    except:
        user = None
    return user


def encode_picture(f):
    file = f.read()
    base = base64.b64encode(file)
    f.close()
    return base


def resize_picture(base_image, width=300):
    img = from_base_to_img(base_image)
    wpercent = (width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img.thumbnail((width, hsize), Image.ANTIALIAS)
    buffer = BytesIO()
    img.save(buffer, format="%s" % img.format)
    img_str = base64.b64encode(buffer.getvalue())
    buffer.close()  # encode miniature picture


    return img_str



def picture_info(base_img):
    """:return picture size"""

    return  base_img.__sizeof__()


def from_base_to_img(base_img):
    img = Image.open(io.BytesIO(base64.b64decode(base_img)), mode='r')
    return img



def decode_picture(id_picture):
    """search picture on id and return him in base64 format"""
    pic = Picture.objects.get(id=id_picture)
    p = pic.pictures
    b = p.tobytes()
    return b


def picture_size(b):
    """input picture in base64 format"""
    img = from_base_to_img(b)
    i = img.size
    img.close()
    return ('%sx%s') %(i[0],i[1])


def admin_check(request, user_id):
    if int(user_id) == request.session.get('user') and get_user(request.session.get('user')) == User.objects.get(email="admin@admin.admin"):
        return True
    else:
        return False


def like_check(request, picture_id):
    likes = Likes.objects.filter(picture=picture_id, user=request.session.get('user'))
    for l in likes:
        if l.user_id == request.session.get('user'):
            return True
        else:
            return False


def int_check (value):
    try:
        someVar = int(value)
        return 1
    except (TypeError, ValueError):
        return 0



