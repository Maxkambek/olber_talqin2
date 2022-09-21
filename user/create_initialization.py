from paycomuz import Paycom
paycom = Paycom()
url = paycom.create_initialization(amount=5.00, order_id='197', return_url='https://2d78-213-230-121-237.ngrok.io/user/check-merchant/')
print(url)