
from django.shortcuts import redirect
from gallery.forms import CommentsForm, PictureForm
from gallery.models import Likes, Picture, Comment
from gallery.utils.gallery_utils import encode_picture, resize_picture, picture_size
from loginer.models import User


def add_like(request, picture_id, user_id):
    l = Likes(
        user=User.objects.get(id_users=user_id),
        picture=Picture.objects.get(id=picture_id)
    )
    l.save(force_insert=True)
    return redirect('/picture/%s/' % picture_id)


def remove_like(request, picture_id, user_id):
    Likes.objects.filter(user=user_id, picture=picture_id).delete()
    return redirect('/picture/%s/' % picture_id)


def add_comment(request, picture_id, user_id):
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
    form = PictureForm(request.POST, request.FILES)
    print(form)
    if form.is_valid():
        print('VALID', request.POST)

        image = encode_picture(request.FILES['file'])
        miniature= resize_picture(image)
        size = picture_size(image)

        user = User.objects.get(pk=request.session.get('user'))
        pic = Picture(name_of_picture=form.cleaned_data['name_of_picture'],
                      pictures=image,
                      public=int(form.cleaned_data['check']),
                      picture_size=size
                      )
        pic.id_user = user
        pic.save()
        mini = Picture.objects.get(id=pic.id)
        mini_p = Picture(  # create a miniature picture
            id_pictures_id=mini.id,
            pictures=miniature,
            name_of_picture=mini.name_of_picture,
            id_user_id=mini.id_user_id,
            public=int(form.cleaned_data['check'])
        )
        mini_p.save()
    else:
        print("NOT VALID")


def delete_picture(request, picture_id):
    print(request.POST)
    #picture_id = int(request.POST.get("picture_id", ''))
    #miniature_picture = Picture.objects.get(id=picture_id)
    Comment.objects.filter(id_picture=picture_id).delete()
    Picture.objects.get(id=picture_id).delete()
    return redirect("/profile/%s/" % request.session.get('user'))


def admin_to_approve_the_picture(request, picture_id):
    pic_mini = Picture.objects.get(id=picture_id)
    pic_mini.check = 1
    pic_mini.save()
    return redirect("/profile/%s/" % request.session.get('user'))


def edit_user_data(request,user_id):
    print(request.POST)
    user = User.objects.get(id_users=user_id)
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.nikname = request.POST['nikname']

    user.save()
    pass


