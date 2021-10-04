import time
import base64
import random

import pyotp

ENCODING = 'utf-8'
TWO_FACT_AUTH_TIMEOUT = 30

def generate_secret_token():
    # Generate a random token
    secret_string = "{}".format(time.time()*random.random())
    return base64.b32encode(secret_string.encode(ENCODING)).decode(ENCODING)[4:12]

def verify_otp_code(user:str, code:str, token:dict):
    # Get the user's secret key
    secret = token#config_data['approved_users'][user]['secret']

    # Create a TOTP object
    totp = pyotp.TOTP(secret)

    two_fact_lookback = 60#config_data['2fa_lookback']

    for lookback in range(two_fact_lookback // TWO_FACT_AUTH_TIMEOUT + 1):
        if totp.verify(code, for_time=time.time() - lookback*TWO_FACT_AUTH_TIMEOUT):
            return True
    return False