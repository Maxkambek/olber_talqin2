import requests


def verify(phone_number, code):
    URL = " http://notify.eskiz.uz/api/message/sms/send"
    PARAMS = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjk1NSwicm9sZSI6InVzZXIiLCJkYXRhIjp7ImlkIjo5NTUsIm5hbWUiOiJcdTA0MWVcdTA0MWVcdTA0MWUgUHJvZm9vZG1peCIsImVtYWlsIjoiZ2F5cmF0cTEyMzQ1NnFAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJhcGlfdG9rZW4iOiJleUowZVhBaU9pSktWMVFpTENKaGJHY2lPaUpJVXpJMU5pSjkuZXlKemRXSWlPamsxTlN3aWNtOXNaU0k2SW5WelpYSWlMQ0prWVhSaElqcDdJbWxrSWpvNU5UVXNJbTVoYldVaU9pSmNkVEEwTVdWY2RUQTBNV1ZjZFRBME1XVWdVSEp2Wm05dlpHMXBlQ0lzSW1WdFlXbHNJam9pWjJGNWNtRjBjVEV5TXpRMU5uRkFaMjFoYVd3dVkyOXRJaXdpY205c1pTSTZJblZ6WlhJaUxDSmhjR2xmZEc5clpXNGlPaUpsZVVvd1pWaEJhVTlwU2t0V01WRnBURU5LYUciLCJzdGF0dXMiOiJhY3RpdmUiLCJzbXNfYXBpX2xvZ2luIjoiZXNraXoyIiwic21zX2FwaV9wYXNzd29yZCI6ImUkJGsheiIsInV6X3ByaWNlIjo1MCwidWNlbGxfcHJpY2UiOjUwLCJiYWxhbmNlIjoyODA2NTAsImlzX3ZpcCI6MCwiaG9zdCI6InNlcnZlcjEiLCJjcmVhdGVkX2F0IjoiMjAyMi0wOC0wMVQwNzowMDo0MC4wMDAwMDBaIiwidXBkYXRlZF9hdCI6IjIwMjItMTAtMTNUMTA6MTM6MzUuMDAwMDAwWiJ9LCJpYXQiOjE2NjU2NTY1ODQsImV4cCI6MTY2ODI0ODU4NH0.ZOhN41tuFW8MjWZyZYwkNBIFkSJ8kpBh7ax8B6AlwFQ"}
    phone = str(phone_number)[1:13]
    data = {
        'mobile_phone': phone,
        'message': code,
        'from': "4546",
        'callback_url': 'http://0000.uz/test.php'
    }

    response = requests.request("POST", URL, data=data, headers=PARAMS)
    return response

