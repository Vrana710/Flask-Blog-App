from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

def load_posts():
    try:
        with open(os.path.join(os.path.dirname(__file__), "data/data.json"), 'r') as f:
            posts = json.load(f)
            print("Posts loaded:", posts)  # Debugging line
            return posts
    except Exception as e:
        print(f"Error loading posts: {e}")
        return []

def save_posts(posts):
    try:
        with open("data/data.json", 'w') as f:
            json.dump(posts, f, indent=4)
    except Exception as e:
        print(f"Error saving posts: {e}")

def fetch_post_by_id(post_id):
    blog_posts = load_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None

@app.route('/')
def index():
    blog_posts = load_posts()
    if isinstance(blog_posts, list) and all(isinstance(post, dict) for post in blog_posts):
        # Sort posts by 'id' in descending order
        blog_posts.sort(key=lambda x: x['id'], reverse=True)
        print("Loaded and sorted blog posts:", blog_posts)  # Debugging line
        return render_template('index.html', posts=blog_posts)
    else:
        print("Error: Blog posts data is not in the expected format.")  # Debugging line
        return "Internal Server Error", 500

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    print(f"Received POST request to like post ID: {post_id}")
    blog_posts = load_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1
            break

    save_posts(blog_posts)
    
    # Return the updated like count as JSON
    updated_post = fetch_post_by_id(post_id)
    return jsonify({'likes': updated_post['likes']})

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_posts()
        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1
        new_post = {
            'id': new_id,
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'comments': []  # Initialize an empty list for comments
        }
        blog_posts.append(new_post)
        save_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = load_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_posts(blog_posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_posts()
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        print("Form Data Received:", request.form)

        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        print("Updated Post:", post)

        for i, p in enumerate(blog_posts):
            if p['id'] == post_id:
                blog_posts[i] = post
                break

        save_posts(blog_posts)

        updated_posts = load_posts()
        print("Posts after saving:", updated_posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    print("Received POST request to add comment to post ID:", post_id)
    print("Form Data:", request.form)
    blog_posts = load_posts()
    post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    new_comment = {
        'author': request.form.get('author'),  # Changed from 'post_id' to 'author'
        'text': request.form['comment']
    }

    if 'comments' not in post:
        post['comments'] = []

    post['comments'].append(new_comment)

    for i, p in enumerate(blog_posts):
        if p['id'] == post_id:
            blog_posts[i] = post
            break

    save_posts(blog_posts)

    # Debugging line
    print(f"Updated post {post_id} with new comment: {new_comment}")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
