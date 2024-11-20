from flask import Flask, request, redirect, url_for, render_template, abort
from datetime import datetime
import json
import os

app = Flask(__name__)

POSTS_FILE = "posts.json"

# Helper functions
def load_posts():
    """Load blog posts from the JSON file."""
    if not os.path.exists(POSTS_FILE):
        return []
    with open(POSTS_FILE, "r") as file:
        return json.load(file)

def save_posts(posts):
    """Save blog posts to the JSON file."""
    with open(POSTS_FILE, "w") as file:
        json.dump(posts, file, indent=4)

# Routes
@app.route('/')
def index():
    """Display all blog posts."""
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts, year=datetime.now().year)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new blog post."""
    if request.method == 'POST':
        # Handle form submission
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        if not author or not title or not content:
            # Validate input data
            return "All fields are required!", 400

        blog_posts = load_posts()
        new_post = {
            'id': len(blog_posts) + 1,  # Assign a new unique ID
            'author': author,
            'title': title,
            'content': content
        }

        blog_posts.append(new_post)
        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('add.html', year=datetime.now().year)

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update an existing blog post."""
    blog_posts = load_posts()
    post = next((post for post in blog_posts if post['id'] == post_id), None)

    if not post:
        abort(404, description="Post not found")

    if request.method == 'POST':
        post['author'] = request.form.get('author', post['author'])
        post['title'] = request.form.get('title', post['title'])
        post['content'] = request.form.get('content', post['content'])
        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)

@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete a blog post."""
    blog_posts = load_posts()
    updated_posts = [post for post in blog_posts if post['id'] != post_id]

    if len(updated_posts) == len(blog_posts):
        abort(404, description="Post not found")

    save_posts(updated_posts)
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
