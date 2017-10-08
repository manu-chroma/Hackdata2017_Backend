from flask import Flask, request, jsonify
import sys

# google vision and luis
from . import api

app = Flask(__name__)

@app.route("/")
def hello():
	print("console logging", file=sys.stdout)
	return "Hello World!"

# this is essentially get request only
@app.route('/post/<int:post_id>')
def show_post(post_id):
	# show the post with the given id, the id is an integer
	return 'Post %d' % post_id


# Send POST request to this method
# body {img: binary file, type: "contact, event, etc."}
@app.route("/img", methods = ['GET', 'POST'])
def img():
	if request.method == 'GET':
		return "Make a POST request with 'img' and 'data' :)"

	if request.method == 'POST':

		# try:
		img   = request.json['img']
		# type_ = request.form['type']

		# send img to google API call
		# print("console logging: {}".format(img), file=sys.stdout)
		
		# call those api's 
		extracted_text = api.google_vision(img)
		datetime       = api.luis(extracted_text)
		location       = api.google_nlp(extracted_text)         




		response = {
			'response' : 'OK',
			'contact'  : {
				'name' : '',
				'datetime' : datetime,
				'location' : location
			}
		} 

		response_fail = {
			'response' : 'FAIL'
		}
		
		print("console logging: {}".format(extracted_text), file=sys.stdout)
		return jsonify({'text' : extracted_text})
		# return "return dummy data"
	
		# except:
			# return jsonify({'text' : 'no text found'})

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)