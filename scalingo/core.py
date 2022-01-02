import requests
from .requests_scalingo_api import RequestsScalingoApi

def get_token(token, session=None, **kwargs):
    """Returns an authenticated RequestsScalingoApi instance, via API token."""
    if not session:
        session = requests.session()
    s = RequestsScalingoApi(session=session, **kwargs)

    # Login.
    if s.authenticate(token):
        return s
    return None
