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
    """Handles the creation of a new post. GET method: Renders the template
     "add.html" to display the form for adding a new blog post. POST method:
     Processes the form data to create a new post and redirects to the
      start page."""
    blog_posts = read_data('blog_data.json')
    if request.method == 'POST':
        if blog_posts:
            new_id = max(post['id'] for post in blog_posts) + 1
        else:
            new_id = 1
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        likes = request.form.get('likes', 0)
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content,
            'likes': likes
        }
        blog_posts.append(new_post)
        sync_data('blog_data.json', blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    """Handles the deletion of a blog post and redirects to the start page."""
    blog_posts = read_data('blog_data.json')
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break  # The loop breaks after the post has been removed, as it is
            # assumed that the ID is unique
    sync_data('blog_data.json', blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update an existing blog post with new title, author, or content.
    Redirect to the home page after updating."""
    post = fetch_post_by_id('blog_data.json', post_id)  # Fetch the blog posts from the JSON file
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        title = request.form.get('title')
        if title is None:  # If no new info is provided then keep the previous
            title = post['title']
        else:
            title = title
        author = request.form.get('author')
        if author is None:
            author = post['author']
        else:
            author = author
        content = request.form.get('content')
        if content is None:
            content = post['content']
        else:
            content = content
        updated_post = {
            'id': post_id,
            'author': author,
            'title': title,
            'content': content,
            'likes': post['likes']
        }
        post.update(updated_post)
        update_post_in_json('blog_data.json', updated_post)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    """Increments likes for the specified post and updates 'blog_data.json'.
    Redirects to the index page or returns a 404 if the post is not found."""
    post = fetch_post_by_id('blog_data.json', post_id)
    if post:
        likes = post['likes'] + 1
        liked_post = {
            'id': post_id,
            'author': post['author'],
            'title': post['title'],
            'content': post['content'],
            'likes': likes
        }
        post.update(liked_post)
        update_post_in_json('blog_data.json', liked_post)
        return redirect(url_for('index'))
    return "Post not found", 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
