# -*- coding: utf-8 -*-
"""
This module provides the basic API interface for Scalingo.

Inspired: https://gist.github.com/stefansundin/96b655f1512d1ce9d570e008dbe122d3
Scalingo API details:https://developers.scalingo.com/index#global-information

Usage:
    token = os.environ.get('SCALINGO_TOKEN')
    scalingo = RequestsScalingoApi(token)

    r=scalingo.regions
    print(r)
    print(r['osc-fr1'])

    # get apps in region "osc-fr1"
    r = scalingo.get("apps",region="osc-fr1")
    print(r.json())

    # get self information
    r = scalingo.get("users/self",region="osc-fr1")
    r = scalingo.get("scm_integrations")
    r = scalingo.get("addon_providers",region='osc-fr1')

    # get my-app if exists
    r = scalingo.get("apps/my-app",region="osc-fr1")
    # get process in my my-app
    r = scalingo.get("apps/my-app/ps",region="osc-fr1")

    # Create test-app in Dry Run
    r = scalingo.post("apps",region="osc-fr1", headers={"X-Dry-Run": "true"}, json={"app":{"name":"test-app"}})

    print(r.status_code)
    print(r.json())

"""
import requests

# constant
SCALINGO_API_VERSION = 'v1'
SCALINGO_AUTH_URL = 'https://auth.scalingo.com'
SCALINGO_HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}

class RequestsScalingoApi(object):
    """The core RequestApi class."""

    def __init__(self, session=None, **kwargs):
        super(RequestsScalingoApi, self).__init__()
        self.auth_url = SCALINGO_AUTH_URL
        if session is None:
            session = requests.session()

        self.session = session
        # We only want JSON back.
        self.session.headers.update(SCALINGO_HEADERS)
        for arg in kwargs:
            if isinstance(kwargs[arg], dict):
                kwargs[arg] = self.__deep_merge(getattr(self.session, arg), kwargs[arg])
            setattr(self.session, arg, kwargs[arg])

    def authenticate(self, token):
        """Logs user into Scalingo with given api_key."""
        # Get bearer token from token (1 hour ttl)
        self.bearer_token = self.__get_bearer_token('/v1/tokens/exchange',token)
        if self.bearer_token:
            self.session.headers.update({'Authorization': 'Bearer ' + str(self.bearer_token)})
            self._api_token_verified = True
            # get a map of region name and region api
            self.regions = self.__get_regions(self.auth_url+'/v1/regions')

        self._api_token_verified = True if self.bearer_token else False

        return self._api_token_verified


    def __get_bearer_token(self, url, token, **kwargs):
        """Get bearer token from api token ."""
        try:
            response = self.session.post(self.auth_url+url, timeout=5, auth=('',token))
            response.raise_for_status()
            bearer_token = response.json()['token']
            return bearer_token
        except requests.exceptions.HTTPError as err:
            print(err)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def __get_regions(self, url, **kwargs):
        """Get all regions name and regions api endpoint."""
        regions = self.session.get(url,**kwargs).json()
        names = dict( (x['name'], x['api']) for x in regions['regions'])
        return names

    def __get_base_url(self, region=None):
        """Return api endpoint from region name."""
        if region and region in self.regions:
            base_url = self.regions[region]
        else:
            base_url = self.auth_url
        return base_url

    def _url_for(self, region=None, *args):
        """Return api url, composed from "region api url"/"scalingo version"/"url"""
        args = map(str, args)
        return "/".join([self.__get_base_url(region), SCALINGO_API_VERSION]  + list(args))

    def request(self, method, url, region=None, **kwargs):
        return self.session.request(method, self._url_for(region,url), **kwargs)

    def head(self, url, region=None, **kwargs):
        return self.session.head(self._url_for(region,url), **kwargs)

    def get(self, url, region=None, **kwargs):
        return self.session.get(self._url_for(region,url), **kwargs)

    def post(self, url, region=None, **kwargs):
        return self.session.post(self._url_for(region,url), **kwargs)

    def put(self, url, region=None, **kwargs):
        return self.session.put(self._url_for(region,url), **kwargs)

    def patch(self, url, region=None, **kwargs):
        return self.session.patch(self._url_for(region,url), **kwargs)

    def delete(self, url, region=None, **kwargs):
        return self.session.delete(self._url_for(region,url), **kwargs)

    @staticmethod
    def __deep_merge(source, destination):
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                RequestsScalingoApi.__deep_merge(value, node)
            else:
                destination[key] = value
        return destination
