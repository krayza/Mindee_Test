import json

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from base64 import b64encode
import requests

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

mindee_url = "MINDEE_URL"
mindee_headers = {
    'MINDEE': "HEADER",
}

from models.post import Post
db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    title = request.form['title']
    file = request.files['inputFile']

    files = {'file': file}
    res = requests.post(mindee_url, files=files, headers=mindee_headers)

    file.seek(0)
    post = Post(title=title, image=file.read(), image_name=file.filename, api_return=res.text)

    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/images')
def list_images():
    posts = Post.query.all()
    myposts = [(post.title, b64encode(post.image).decode('utf-8'), post.image_name, post.api_return) for post in posts]
    return render_template('listImages.html', posts=myposts)


def to_pretty_json(value):
    return json.dumps(json.loads(value), sort_keys=True, indent=4, separators=(',', ': '))


app.jinja_env.filters['tojson_pretty'] = to_pretty_json

if __name__ == '__main__':
    app.run(debug=True)
