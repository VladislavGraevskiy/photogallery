import urllib.parse
import requests
import json


def email_check(email):
    username = 'uladzislau'
    password = 'sarodo64'
    check_email = email
    api_url = 'http://api.verify-email.org/api.php?'

    url = '%susr=%s&pwd=%s&check=%s' %(api_url, username, password, check_email)
    print(url)
    page = requests.get(url)
    p = page.json()
    if int(p['verify_status']):
        print('EEEEE')




email_check('vladislavgraevskiy@gmail.com')