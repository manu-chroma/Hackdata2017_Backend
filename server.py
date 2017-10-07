from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def hello():
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

        img   = request.form['img']
        type_ = request.form['type']

        # send img to google API call
        
        return type_
        # return "return dummy data"