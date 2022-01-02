#!/usr/bin/env python

import scalingo
import pprint
import os
import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

if __name__ == '__main__':
    token = os.environ.get('SCALINGO_TOKEN')
    scalingo_conn = scalingo.get_token(token)
    if not scalingo_conn:
        raise("Error: invalid token")

    attrs = vars(scalingo_conn)
    print(', '.join("%s: %s\n" % item for item in attrs.items()))

    #r = scalingo_conn.regions
    #print(r['osc-fr1'])

    #r = scalingo_conn.get("regions")
    #r = scalingo_conn.get("scm_integrations")
    #r = scalingo_conn.get("addon_providers",region='osc-fr1')
    #r = scalingo_conn.get("users/self",region="osc-fr1")

    r = scalingo_conn.get("apps",region="osc-fr1")

    #r = scalingo_conn.get("apps/test-app",region="osc-fr1")

    print(r.status_code)
    print(r.json())
    print(r.request.headers)
    print(r.headers)

    #r = scalingo_conn.post("apps",region="osc-fr1", headers={"X-Dry-Run": "true"}, json={"app":{"name":"test-app"}})
    #print(r.status_code)
    #print(r.json())
    #print(r.request.headers)
    #print(r.headers)
    #
    #r = scalingo_conn.get("apps/test-app/ps",region="osc-fr1")
    #print(r.json())
