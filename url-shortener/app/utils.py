# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need

from urllib.parse import urlparse
import random
import string


def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))



def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

