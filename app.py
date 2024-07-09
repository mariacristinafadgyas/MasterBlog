from flask import Flask, render_template
from storage import *

app = Flask(__name__)


@app.route('/')
def index():
    """Renders the index.html template with the data collected from the JSON
     file which is read in the storage file"""
    blog_posts = read_data('blog_data.json')
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
