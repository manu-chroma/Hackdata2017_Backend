import requests
import base64
import json
import io
import os
import pprint
import sys

GOOGLE_VISION_KEY = ''

# no need of arguement because manjul is giving base64 encoded image.
def convert_to_base64():

	# hard-coding path for testing.
	with open('/home/manu/coursework/hackdata/data/14.jpg', 'rb') as f:
		img         = f.read()
		encoded_img = base64.b64encode(img)
	
	return encoded_img

def google_vision(img=''):

	# if image is not coming from flask server i.e. TESTING
	if img == '':
		encoded_img = convert_to_base64()
		encoded_img = encoded_img.decode('utf-8')

	# image coming from server i.e. PRODUCTION
	else:
		# sending binary data
		encoded_img = img

	data = {
			  "requests": [
				{
				  "image": {
					"content": encoded_img
				  },

				  "features": [
					{
					  "type": "TEXT_DETECTION"
					}
				  ]
				}
			  ]
			}

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		
	url = 'https://vision.googleapis.com/v1/images:annotate?key='

	r = requests.post(url+GOOGLE_VISION_KEY, data=json.dumps(data), headers=headers)
	
	# pprint.pprint(r.json()['responses']['textAnnotations'][0])

    # convert json to dict
	response_dict = r.json()

	# pprint.pprint(response_dict['responses']['fullTextAnnotation']['textAnnotations']['description'])
	
	# @breaking: seems to work almost all of the time
	extracted_string = response_dict['responses'][0]['textAnnotations'][0]['description']

	# @improve: CLEAN DATA
	extracted_string = extracted_string.replace("\n", " ")#.replace(".", '/')

	print(extracted_string, file=sys.stdout)



	return extracted_string

def luis(string):
	base_url = ''

	text_to_test = string


	res          = requests.get(base_url+text_to_test)
	content_json = res.json()

	pprint.pprint(content_json['entities'])

	datetime = ''

	# content_json['entities'] is a list
	for i in content_json['entities']:
		if i['resolution']['values'][0]['type'] == 'datetime':
			datetime = i['resolution']['values'][0]['value']


	if datetime != '':
		return datetime

	date = ''
	time = '09:00:00' # default time to be returned


	# @todo: can be improved in case of multiple dates.
	for i in content_json['entities']:
		if i['resolution']['values'][0]['type'] == 'date':
			date = i['resolution']['values'][0]['value']

		if i['resolution']['values'][0]['type'] == 'time':
			time = i['resolution']['values'][0]['value']

	# if date is empty, the system falls down
	if date != '':
		datetime = date + ' ' + time

	return datetime

	# return content_json


def google_nlp(string):

	data =	{
	      	  "encodingType": "UTF8",
	      	  "document": {
	      	    "type": "PLAIN_TEXT",
	      	    "content": string
	      	  }
	      	}

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

	url = 'https://language.googleapis.com/v1/documents:analyzeEntities?key='

	r = requests.post(url+GOOGLE_VISION_KEY, data=json.dumps(data), headers=headers)

	pprint.pprint(r.json()['entities'])

if __name__ == '__main__':
	extracted_text = google_vision()
	datetime       = luis(extracted_string)

	print("Extracted Text: {}".format(extracted_text))
	print("Datetime: {}".format(datetime))

	# @goals: title, location, anything else?







# ------------------------------------------------------------------------------------------------

	# if we want to use Image URL 

	# data = {
	#	  "requests": [
	#		{
	#		  "image": {
	#			"source": {
	#		"imageUri": "https://cloud.google.com/vision/docs/images/abbey_road.png"
	#			}
	#		  },
	#		  "features": [
	#			{
	#			  "type": "DOCUMENT_TEXT_DETECTION"
	#			}
	#		  ]
	#		}
	#	  ]
	#	}