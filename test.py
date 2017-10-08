# MICROSOFT VISION API SERVICE 

# key = '22ba2efab03f45d18ea3d65efb2dab27'

# import requests

# url_base = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0'

# headers = {
#     # Request headers.
#     'Content-Type': 'application/json',
#     'Ocp-Apim-Subscription-Key': subscription_key,
# }



# params = {
#     # Request parameters. All of them are optional.
#     'visualFeatures': 'Categories,Description,Color',
#     'language': 'en',
# }

# body = 

# MS LUIS TESTING
import requests
import pprint
import json

# on telegram 
base_url = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/3a7bdb13-78b4-4a96-9548-81233ace1bd5?subscription-key=ef0101d81c8741939cfe5ba5ddcb03f3&verbose=true&timezoneOffset=330&spellCheck=true&q='

text_to_test = input("enter data: ")


res          = requests.get(base_url+text_to_test)
content_json = res.json()

# pretty print json dict
pprint.pprint(content_json)

#venue[:][ ][0-9]*[a-z]*[ ][A-Z]*[ ][a-z]*

print((res.json()['query']))

queryToBeParsed = res.json()['query']
print(queryToBeParsed)

import re

#regex as a last resort
#what other alternatives are there?

pattern = re.compile(r"\[venue: \]")
print(re.search(pattern, "venue: D217"))