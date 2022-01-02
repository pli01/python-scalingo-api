# python-scalingo-api

WIP:

This module provides the basic API interface for Scalingo.

Scalingo API details:  https://developers.scalingo.com/index#global-information

Inspiration: https://gist.github.com/stefansundin/96b655f1512d1ce9d570e008dbe122d3


```python

import scalingo
import os

token = os.environ.get('SCALINGO_TOKEN')

scalingo_conn = scalingo.get_token(token)
if not scalingo_conn:
    raise("Error: invalid token")

regions = scalingo_conn.regions
print(regions)
print(regions['osc-fr1'])

# request to /apps api
r = scalingo_conn.get("apps",region="osc-fr1")
print(r.json())
 
# get "my-app" if exists
r = scalingo_conn.get("apps/my-app",region="osc-fr1")

# Try to Create "test-app" (Dry Run mode)
r = scalingo_conn.post("apps",region="osc-fr1", headers={"X-Dry-Run": "true"}, json={"app":{"name":"test-app"}})
print(r.status_code)
print(r.json())

```
