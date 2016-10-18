import bcrypt
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from loginer.models import User
from loginer.servises.validations_servise import email_validate


def del_user_session(request):
    del request.session['user']
    request.session.modified = True


def check_user(email, password):
    try:
        user = User.objects.get(email=email)
        salt = bytes(user.password, 'utf-8')
        if user and hashed_password(password, salt) == salt:
            return user.id_users
        else:
            return False
    except ObjectDoesNotExist:
        return False


def login_check(nickname, email):
    for user in User.objects.all():
        if nickname == user.nikname:
            return 'a user with the nickname already exists'
        if user.email == email:
            return 'a user with the email already exists'
    if not email_validate(email):
        return 'your email was incorrect'
    else:
        return False


def hashed_password(password, salt=bcrypt.gensalt(14)):

    pw = bytes(password, 'utf-8')
    print(salt)

    hashed = bcrypt.hashpw(pw, salt)
    if bcrypt.hashpw(pw, salt) == salt:
        print(bcrypt.hashpw(pw, hashed), hashed)
        print("It Matches!")
    else:
        print("It Does not Match :(")
    print(hashed)
    return hashed
