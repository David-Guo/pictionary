from flask import Flask, render_template, request
from predict import classfy
c = classfy()

app = Flask(__name__)
name = None

@app.route('/')
def index():
    return render_template('test.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['file']
    filename = "./test.png"
    file.save(filename)
    global name
    name = c.predict(filename)
    return name


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
