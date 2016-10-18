
from django.shortcuts import  render_to_response, redirect
from django.template.context_processors import csrf
from loginer.forms import UserForm
from loginer.models import User
import requests


from loginer.utils.login_utils import check_user, login_check, del_user_session, hashed_password


def registration(request):
    picture_form = UserForm
    args = {}
    args.update(csrf(request))
    args['form'] = picture_form
    if request.POST:
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
           # mistake = login_check(user.nikname, user.email)
            user.password = hashed_password(user.password)
            if True:
                form.save()
                return redirect('/login/')
            else:
                args['login_error'] = 'Sorry, %s' #% mistake
                return render_to_response('registration.html', args)

    return render_to_response('registration.html', args)


def login(request):
    if not request.session.get('user'):
        args = {}
        args.update(csrf(request))
        if request.POST:
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            id_user = check_user(email, password)

            if id_user:
                request.session['user'] = id_user
                return redirect('/')
            else:
                args['login_error'] = 'Sorry, your password or email was incorrect'
                return render_to_response('login.html', args)
        else:
            return render_to_response('login.html', args)
    else:
        return redirect('/')


def logout(request):
    del_user_session(request)
    return redirect('/')






