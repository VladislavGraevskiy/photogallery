from django.shortcuts import render_to_response, redirect
from gallery.handler import get_gallery
from gallery.servises import database_servise
import gallery.utils.gallery_utils as utils


def pictures(request):
    return render_to_response('pictures.html', get_gallery.get_pictures(request))


def add_picture(request):
    if request.POST:
        database_servise.add_picture(request)
    else:
        return render_to_response('add_picture.html', get_gallery.get_add_picture(request))
    return redirect('/profile/')


def profile(request, user_id):
    if utils.admin_check(request, user_id):
        return render_to_response('admin_profile.html', get_gallery.get_admin_profile(request, user_id))
    else:
        return render_to_response('profile.html', get_gallery.get_user_profile(request, user_id))


def picture2(request, picture_id, user_id=''):
    if request.POST:
        print('POST')
        return render_to_response('picture.html', get_gallery.get_picture(request, picture_id, user_id))

    return render_to_response('picture.html', get_gallery.get_picture(request, picture_id, user_id))


def edit_profile(request, user_id):
    if request.POST:
        database_servise.edit_user_data(request,user_id)
        return redirect('/profile/%s/' % user_id)

    return render_to_response('edit_profile.html', get_gallery.get_edit_profile(request, user_id))
