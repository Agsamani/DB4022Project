import random
import string
from django.core.cache import cache

OTP_EXPIRY_TIME = 300  # OTP expiry time in seconds (5 minutes)

# TODO: use proper OTP generator
# TODO: send OTP to phone or email
def generate_otp(identifier, length=6):
    digits = string.digits
    otp = ''.join(random.choices(digits, k=length))
    cache.set(identifier, otp, timeout=OTP_EXPIRY_TIME)
    return otp


def validate_otp(identifier, otp):
    cached_otp = cache.get(identifier)
    if cached_otp is not None and cached_otp == otp:
        cache.delete(identifier)  # Invalidate OTP after successful validation
        return True
    return False
