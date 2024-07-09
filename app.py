from flask import Flask, render_template, request, redirect, url_for
from storage import *

app = Flask(__name__)


@app.route('/')
def index():
    """Renders the index.html template with the data collected from the JSON
     file which is read in the storage file"""
    blog_posts = read_data('blog_data.json')
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    blog_posts = read_data('blog_data.json')
    if request.method == 'POST':
        if blog_posts:
            new_id = max(post['id'] for post in blog_posts) + 1
        else:
            new_id = 1
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }
        blog_posts.append(new_post)
        sync_data('blog_data.json', blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    blog_posts = read_data('blog_data.json')
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break  # The loop breaks after the post has been removed, as it is
            # assumed that the ID is unique
    sync_data('blog_data.json', blog_posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
