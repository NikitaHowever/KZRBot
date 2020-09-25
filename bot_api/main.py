from bottle import run, post, request
import requests
import uuid

url = "https://api.telegram.org/bot1398450165:AAFC9iquGnVr6Kyy49RvojtSJbMNdtlHT5Q/sendMessage"


@post("/success-pay")
def success_pay():
    id = uuid.uuid4()
    obj = {
            'chat_id': request.json.get('custom').get('userId'),
            'text': "Ваш номер заказа: {}".format(id)
        }
    
    x = requests.post(url, json=obj)


run(reloader=True, debug=True)