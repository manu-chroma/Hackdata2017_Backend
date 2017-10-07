import requests
import base64
import json
import io
import os
import pprint

GOOGLE_VISION_KEY = ''

def convert_to_base64(img):

	# hard-coding path of image for now.
	with open('/home/manu/coursework/hackdata/data/1.jpg', 'rb') as f:
		img         = f.read()
		encoded_img = base64.b64encode(img)
	
	return encoded_img

def google_vision(img=''):
	# img is image binary data

	encoded_img = convert_to_base64('')

	# sending binary data

	data = {
			  "requests": [
				{
				  "image": {
					"content": encoded_img.decode('utf-8')
				  },

				  "features": [
					{
					  "type": "TEXT_DETECTION"
					}
				  ]
				}
			  ]
			}


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

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		
	url = 'https://vision.googleapis.com/v1/images:annotate?key='

	r = requests.post(url+GOOGLE_VISION_KEY, data=json.dumps(data), headers=headers)
	# pprint.pprint(r.json()['responses']['textAnnotations'][0])

        # convert json to dict
	response_dict = r.json()

	# pprint.pprint(response_dict['responses']['fullTextAnnotation']['textAnnotations']['description'])
	
	extracted_string = response_dict['responses'][0]['textAnnotations'][0]['description']

	# CLEAN DATA
	
	extracted_string = extracted_string.replace("\n", " ").replace(".", '/')

	print(extracted_string)

	# calling LUIS
	luis_output_dict = luis(extracted_string)

	# extracting from entities
	pprint.pprint(luis_output_dict['entities'])

def luis(string):
	base_url = ''

	text_to_test = string


	res          = requests.get(base_url+text_to_test)
	content_json = res.json()


	return content_json

        
if __name__ == '__main__':
	google_vision()
