# Hidden keys and configs
from backend.settings import env


class MpesaConfig:
    CONSUMER_KEY = env('CONSUMER_KEY')
    CONSUMER_SECRET = env('CONSUMER_SECRET')
    SHORTCODE = env('SHORTCODE')
    BASE_URL = env('BASE_URL')
    PASSKEY = env('PASSKEY')
    URL = env('URL')

    # SERVER_URL
    SERVER_URL = env('BASE_SERVER_URL')
    SANDBOX_URL = "https://sandbox.safaricom.co.ke/mpesa/"
