import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# Hidden keys and configs
class MpesaConfig:
    CONSUMER_KEY = env('CONSUMER_KEY')
    CONSUMER_SECRET = env('CONSUMER_SECRET')
    SHORTCODE = env('SHORTCODE')
    BASE_URL = env('BASE_URL')
    PASSKEY = env('PASSKEY')
    URL = env('URL')
