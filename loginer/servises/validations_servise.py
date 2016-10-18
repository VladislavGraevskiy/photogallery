import requests


def email_validate(email):
    username = 'uladzislau'
    password = 'sarodo64'
    check_email = email
    api_url = 'http://api.verify-email.org/api.php?'
    url = '%susr=%s&pwd=%s&check=%s' % (api_url, username, password, check_email)
    page = requests.get(url)
    p = page.json()

    return int(p['verify_status'])