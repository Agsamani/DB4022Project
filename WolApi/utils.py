import random
import string
from django.core.cache import cache
from PIL import Image
from django.conf import settings

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
        cache.delete(identifier)
        return True
    return False


def save_request_image(image, image_id):
    image = Image.open(image)
    image = image.convert('RGB')
    path = settings.MEDIA_ROOT / f"{image_id}.png"
    image.save(path, 'PNG')
    return path

