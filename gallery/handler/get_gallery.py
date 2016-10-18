from django.template.context_processors import csrf

from gallery import utils
from gallery.forms import PictureForm, CommentsForm
from gallery.models import Picture, Comment, Likes

from gallery.utils.gallery_utils import *
from loginer.models import User


def get_pictures(request):
    args = {}
    args['username'] = get_user(request.session.get('user'))
    if request.session.get('user'):
        args['pictures'] = Picture.objects.exclude(id_pictures_id=None).filter(check=1)
    else:
        args['pictures'] = Picture.objects.exclude(id_pictures_id=None).filter(check=1 , public=1)

    return args


def get_add_picture(request):
    picture_form = PictureForm
    args = {}
    args.update(csrf(request))
    args['form'] = picture_form
    args['username'] = get_user(request.session.get('user'))
    return args


def get_picture_id(picture_id):
    pic = Picture.objects.get(id=picture_id)


def get_admin_profile(request, user_id):
    args = {}
    args.update(csrf(request))
    args['miniature'] = Picture.objects.filter(check=0).exclude(id_pictures_id=None)
    args['user'] = User.objects.get(id_users=user_id)
    args['username'] = get_user(request.session.get('user'))

    if request.POST:
        try:
            print(request.POST['fr'])
            pic = Picture.objects.get(id=request.POST['fr'])
            args['user_info'] = User.objects.get(id_users=pic.id_user_id)
            args['count'] = Picture.objects.filter(id_user=pic.id_user_id, check=1).exclude(id_pictures_id=None).count()
            picture_info(request)
            return args
        except:
            return args
    return args


def get_user_profile(request, user_id):
    args = {}
    args.update(csrf(request))
    args['pictures'] = Picture.objects.filter(id_user=user_id).exclude(id_pictures_id=None)
    args['comments'] = Comment.objects.filter(id_user=user_id)
    args['user'] = User.objects.get(id_users=user_id)
    args['username'] = get_user(request.session.get('user'))
    return args


def get_edit_profile(request, user_id):
    args = {}
    args.update(csrf(request))
    args['user'] = User.objects.get(id_users=user_id)
    args['username'] = get_user(request.session.get('user'))

    return args


def get_picture(request, picture_id, user_id=''):
    comment_form = CommentsForm
    pic = Picture.objects.get(id=picture_id)

    if not request.session.get(('picture%s' % picture_id)):
        pic.views += 1
        pic.save()
        request.session[('picture%s' % picture_id)] = picture_id
    if request.is_ajax():
        pass
    args = {}
    args.update(csrf(request))  # create token
    args['text'] = decode_picture(picture_id)
    args['bytes'] = picture_info(decode_picture(picture_id))
    args['likes'] = Likes.objects.filter(picture=picture_id)
    args['checklike'] = like_check(request, picture_id)
    args['picture'] = Picture.objects.get(id=picture_id)
    args['comments'] = Comment.objects.filter(id_picture=picture_id)
    args['form'] = comment_form
    args['username'] = get_user(request.session.get('user'))
    if request.POST:
        if int_check(request.POST['size']):
            dec_pic = decode_picture(picture_id)

            pic =resize_picture(dec_pic, int(request.POST['size']))
            args['text'] = pic
            args['bytes'] = picture_info(pic)
            args['size'] = picture_size(pic)
            print(args['size'], args['bytes'])
            return args
        else:
            args['error'] = 'input a number'
            return args
    return args

