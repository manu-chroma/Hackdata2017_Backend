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
base_url = ''

text_to_test = input("enter data: ")


res          = requests.get(base_url+text_to_test)
content_json = res.json()

# pretty print json dict
pprint.pprint(content_json)
