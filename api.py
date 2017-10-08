import requests
import base64
import json
import io
import os
import pprint
import sys

# import cStringIO
from PIL import Image

GOOGLE_VISION_KEY = 'AIzaSyB7_LM0SWtHJAHRSuMB3xUi0b181JaNP7Q'

# @potential for description: 
# website url, contact number, name, work of art, organisation, people?: Google's nlp API

# this is description, returned to flask server through google_nlp function
description = ''

# helper print function: 
def _print(string):
	print(string, file=sys.stdout)


def greyscale_image(string):
	pass

# no need of arguement because manjul is giving base64 encoded image.
def convert_to_base64(greyscale = False):

	# hard-coding path for testing.
	with open('/home/manu/coursework/hackdata/data/result_bw.png', 'rb') as f:
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

    # convert json to dict
	response_dict = r.json()
	
	# @breaking: seems to work almost all of the time
	extracted_string = response_dict['responses'][0]['textAnnotations'][0]['description']

	# @improve: CLEAN DATA
	extracted_string = extracted_string.replace("\n", " ")#.replace(".", '/')

	_print("EXTRACTED STRING:")
	_print(extracted_string)
	_print("\n\n")

	return extracted_string

def luis(string):
	base_url = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/3a7bdb13-78b4-4a96-9548-81233ace1bd5?subscription-key=ef0101d81c8741939cfe5ba5ddcb03f3&timezoneOffset=0&verbose=true&q='

	text_to_test = string


	res = requests.get(base_url+text_to_test)
	
	# error handling for LUIS.
	if res.content == b'': # case when text got too long and failed the API
		content_json = {'entities' : []}
	else:
		content_json = res.json()

	_print("ENTITIES FROM LUIS:")
	pprint.pprint(content_json['entities'])
	_print("\n\n")

	datetime = ''

	# content_json['entities'] is a list
	# there are other types of entity also, we're interested in `builtin.datetimeV2.datetime`
	for i in content_json['entities']:
		if i['type'] == 'builtin.datetimeV2.datetime':
			if i['resolution']['values'][0]['type'] == 'datetime':
				datetime = i['resolution']['values'][0]['value']


	if datetime != '':
		datetime = datetime.replace(" ", "T")
		_print("whole datetime: {}\n\n".format(datetime))
		return datetime

	date = ''
	time = '09:00:00' # default time to be returned


	# @todo: can be improved in case of multiple dates.
	for i in content_json['entities']:
		if i['type'] == 'builtin.datetimeV2.date':
			if i['resolution']['values'][0]['type'] == 'date':
				date = i['resolution']['values'][0]['value']

		if i['type'] == 'builtin.datetimeV2.time':
			if i['resolution']['values'][0]['type'] == 'time':
				time = i['resolution']['values'][0]['value']

	# if date is still empty, try first value of `daterange` 
	if date == '':
		for i in content_json['entities']:
			if i['type'] == 'builtin.datetimeV2.daterange':
				if i['resolution']['values'][1]['type'] == 'daterange':
					date = i['resolution']['values'][1]['start']


	# if date is empty, the system falls down
	if date != '':
		datetime = date + 'T' + time + "+05:30"


	_print("\n\nDatetime: {}".format(datetime))
	
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
	response_dict = r.json() 

	_print("PRINTING ENTITIES:")
	pprint.pprint(r.json()['entities'])
	_print("\n\n")

	location = ''
	global description

	for i in response_dict['entities']:
		if i['type'] == 'LOCATION':
			location += " " + i['name']

		# @todo: fix description. not working as intended for now.
		if i['type'] == 'PROPER':
			description += " " + i['content']

		if i['mentions'][0]['type'] == 'PROPER':
			description += " " + i['mentions'][0]['text']['content']



	# take care of formatting issues and cleaning
	# front strip, remove duplicates
	location = location.lstrip()
	location = remove_duplicates(location)
	

	# @todo: remove terms such as venue from the final location var
	_print("\n\nLOCATION: {}".format(location))
	_print("\n\nDESCRIPTION: {}".format(description))
	return (location, description)

def remove_duplicates(string):
	words = string.split()
	word_set = set(words)

	# @todo: self explantory. 
	# maybe this is not the right place to implement it
	# this function is now being used by description and location both	
	# word_set.remove('location')
	
	return " ".join(sorted(word_set, key=words.index))

if __name__ == '__main__':
	extracted_text = google_vision()
	datetime       = luis(extracted_text)

	# @goals: title, location, anything else?
	location, description = google_nlp(extracted_text)	

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
