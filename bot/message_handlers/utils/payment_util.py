import requests

def get_payment_url(username):
    url = 'https://api.capusta.space/v1/partner/payment'
    json_data =  {
            "amount": {
                "amount": 1000,
                "currency": "RUB"
            },
            "description": "kzr paper",
            "projectCode": "kzrgreen",
            "sender": {
                "name": username,
                "comment": "mmmmm"
            }
        }
    headers={"Authorization": "Bearer  rodionhakurei@gmail.com:f6dd1f50-6813-48a0-b4c0-95265e7072c7"}
    responce = requests.post(url, json=json_data, headers=headers)
    json_responce=responce.json()
    return json_responce['payUrl']