import base64
import io

from io import BytesIO
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf

from gallery.forms import CommentsForm, PictureForm
from gallery.models import Picture, Comment, Likes
from loginer.models import User


def pictures(request):
    return render_to_response('pictures.html',
                              {'pictures': Picture.objects.exclude(id_pictures_id=None).filter(check=1),
                               # add a miniature
                               'username': username(request.session.get('user'))},
                              )


def picture(request, picture_id=1):
    comment_form = CommentsForm
    args = {}

    args.update(csrf(request))  # create tokent
    args['text'], args['size'], args['bytes'] = get_picture_from_DB(picture_id)
    args['likes'] = Likes.objects.filter(picture=picture_id)
    args['checklike'] = checklike(request, picture_id)
    args['picture'] = Picture.objects.get(id=picture_id)
    args['comments'] = Comment.objects.filter(id_picture=picture_id)
    args['form'] = comment_form
    args['username'] = username(request.session.get('user'))
    return render_to_response('picture.html', args)


def add_like(request, picture_id, user_id):
    l = Likes(
        user=User.objects.get(id_users=user_id),
        picture=Picture.objects.get(id=picture_id)
    )
    l.save(force_insert=True)

    # if picture_id not in request.COOKIES:
    #    try:
    #       picture_like = Picture.objects.get(id=picture_id)
    #      picture_like.likes += 1
    #     picture_like.save()
    #    # add cookie
    #   response = redirect('/picture/%s/' % picture_id)
    #  response.set_cookie(picture_id, 'test')
    # return response
    # except ObjectDoesNotExist:
    #   raise Http404

    return redirect('/picture/%s/' % picture_id)


def add_comment(request, picture_id, user_id):
    pic = Picture.objects.get(id=picture_id)
    if request.POST and ('pause' not in request.session):
        form = CommentsForm(request.POST)
        print(form)
        comment = form.save(commit=False)
        comment.id_user_id = user_id
        comment.id_picture = Picture.objects.get(id=picture_id)
        form.save()
        # request.session.set_expiry(60)  # session add and set to expiry om 60 seconds
        # request.session['pause'] = True
    return redirect('/picture/%s/' % picture_id)


def add_picture(request):
    global user
    picture_form = PictureForm
    args = {}
    args.update(csrf(request))
    args['form'] = picture_form
    args['username'] = username(request.session.get('user'))

    if request.POST:
        file = request.FILES['file']
        form = PictureForm(request.POST, request.FILES)

        if form.is_valid():
            print('VALID')

            image, miniature = encode_picture(request.FILES['file'])
            user = User.objects.get(pk=request.session.get('user'))
            pic = Picture(name_of_picture=request.POST['name_of_picture'],
                          pictures=image)
            pic.id_user = user
            pic.save()
            mini = Picture.objects.get(id=pic.id)
            mini_p = Picture(  # create a miniature picture
                id_pictures_id=mini.id,
                pictures=miniature,
                name_of_picture=mini.name_of_picture,
                id_user_id=mini.id_user_id
            )
            mini_p.save()
        else:
            print("NOT VALID")
    else:
        return render_to_response('add_picture.html', args)
    return redirect('/profile/%s/' % user.id_users)


def encode_picture(f, basewidth=300):
    file = f.read()
    stri = base64.b64encode(file)
    img = Image.open(io.BytesIO(file), mode='r')
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img.thumbnail((basewidth, hsize), Image.ANTIALIAS)
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue())
    buffer.close()  # encode miniature picture
    # print(file, '\n', stri, '\n', img.size, '\n', img_str, buffer)
    f.close()
    return stri, img_str


def get_picture_from_DB(id_picture):
    pic = Picture.objects.get(id=id_picture)
    p = pic.pictures
    b = p.tobytes()
    img = Image.open(io.BytesIO(base64.b64decode(b)), mode='r')
    size = b.__sizeof__()
    i = img.size

    return b, '%sx%s' % (i[0], i[1]), size


def username(id_user):
    try:
        user = User.objects.get(id_users=id_user)
    except:
        user = None
    return user


def checklike(request, picture_id):
    likes = Likes.objects.filter(picture=picture_id, user=request.session.get('user'))
    for l in likes:
        print(l.user, request.session.get('user'))
        if l.user_id == request.session.get('user'):
            return 'd'

        else:

            return ''


def admin_profile(request, user_id):
    args = {}
    args.update(csrf(request))
    args['pictures'] = Picture.objects.filter(check=0, id_pictures_id=None)
    args['miniature'] = Picture.objects.filter(check=0).exclude(id_pictures_id=None)
    args['comments'] = Comment.objects.filter(id_user=user_id)
    args['user'] = User.objects.get(id_users=user_id)
    args['username'] = username(request.session.get('user'))
    if request.POST:
        if request.POST['check']:
            pic_mini = Picture.objects.get(id=request.POST['value'])
            pic_mini.check = 1
            pic_mini.save()
            print('ok')

        if request.POST['check'] == 'cancel':
            Picture.objects.get(id=request.POST['value']).delete()
            print('cancel')
        if request.POST['check'] == 'info':
            pic = Picture.objects.get(id=request.POST['value'])
            args['user_info'] = User.objects.get(id_users=pic.id_user_id)
            args['count'] = Picture.objects.filter(id_user=pic.id_user_id, check=1).exclude(id_pictures_id=None).count()

            # args['user_info']
            return render_to_response('admin_profile.html', args)
    return render_to_response('admin_profile.html', args)


def profile(request, user_id):
    print(user_id)
    if request.session.get("user") == 1001 and user_id == '1001':
        return admin_profile(request, user_id)

    else:

        args = {}
        args.update(csrf(request))
        args['pictures'] = Picture.objects.filter(id_user=user_id).exclude(id_pictures_id=None)
        args['comments'] = Comment.objects.filter(id_user=user_id)
        args['user'] = User.objects.get(id_users=user_id)
        args['username'] = username(request.session.get('user'))
        if request.POST:
            print(request.POST)
            picture_id = int(request.POST.get("picture_id", ''))
            miniature_picture = Picture.objects.get(id=picture_id)
            Comment.objects.filter(id_picture=miniature_picture.id_pictures_id).delete()
            Picture.objects.get(id=miniature_picture.id_pictures_id).delete()

        return render_to_response('profile.html', args)


def remove_like(request, picture_id, user_id):
    Likes.objects.filter(user=user_id, picture=picture_id).delete()
    return redirect('/picture/%s/' % picture_id)


def resize_picture(picture_id):
    pass


def picture2(request, picture_id, user_id=''):
    comment_form = CommentsForm
    pic = Picture.objects.get(id=picture_id)
    # if request.COOKIES.get('picture') != picture_id:
    #        pic.save()
    #      request.COOKIES.set_expiry(3600)
    #     request.COOKIES['picture'] = picture_id

    args = {}
    args.update(csrf(request))  # create tokent
    args['text'], args['size'], args['bytes'] = get_picture_from_DB(picture_id)
    args['likes'] = Likes.objects.filter(picture=picture_id)
    args['checklike'] = checklike(request, picture_id)
    args['picture'] = Picture.objects.get(id=picture_id)
    args['comments'] = Comment.objects.filter(id_picture=picture_id)
    args['form'] = comment_form
    args['username'] = username(request.session.get('user'))

    if request.POST:
        print('test=')
        return render_to_response('picture.html', args)
    else:
        return render_to_response('picture.html', args)


def edit_profile(request, user_id):
    args = {}
    args.update(csrf(request))
    args['user'] = User.objects.get(id_users=user_id)
    if request.POST:
        date = request.POST
        print(date)
        return redirect('/profile/%s/' % user_id)

    return render_to_response('edit_profile.html', args)
