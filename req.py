import urllib
import json
import httplib2

data = {'principal': '1481689', 'credentials': 'niga123@', 'system':'lucy'}

h = httplib2.Http()
resp, content = h.request("https://api-et.hellocash.net/authenticate", method="POST", body=json.dumps(data), headers={'Content-Type':'application/json'})

content = json.loads(content)
token = content['token']
print(token)