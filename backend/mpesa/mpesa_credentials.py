import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
from .mpesa_config import MpesaConfig as config


class MpesaC2bCredential:
    consumer_key = config.CONSUMER_KEY
    consumer_secret = config.CONSUMER_SECRET
    api_URL = config.URL


class MpesaAccessToken:
    response = requests.get(MpesaC2bCredential.api_URL,
                            auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(response.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']


class LipanaMpesaPassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = config.SHORTCODE
    passkey = config.PASSKEY
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')
