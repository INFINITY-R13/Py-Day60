from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Sample blog posts data
blog_posts = [
    {
        'id': 1,
        'title': 'Getting Started with Flask',
        'subtitle': 'A beginner\'s guide to web development',
        'author': 'John Doe',
        'date': 'March 15, 2024',
        'content': '''
        Flask is a lightweight and flexible web framework for Python. It's perfect for beginners 
        who want to learn web development without getting overwhelmed by complex features.
        
        In this post, we'll explore the basics of Flask and build our first web application.
        Flask follows the principle of "micro-framework" which means it provides the core
        functionality while allowing developers to choose their own tools and libraries.
        '''
    },
    {
        'id': 2,
        'title': 'Understanding Jinja Templates',
        'subtitle': 'Dynamic content made easy',
        'author': 'Jane Smith',
        'date': 'March 20, 2024',
        'content': '''
        Jinja is a powerful templating engine that comes built-in with Flask. It allows you
        to create dynamic HTML pages by embedding Python-like expressions in your templates.
        
        With Jinja, you can use variables, loops, conditionals, and filters to create
        sophisticated web pages without repeating code. This makes your application
        more maintainable and scalable.
        '''
    },
    {
        'id': 3,
        'title': 'Building RESTful APIs',
        'subtitle': 'Creating web services with Flask',
        'author': 'Mike Johnson',
        'date': 'March 25, 2024',
        'content': '''
        REST (Representational State Transfer) is an architectural style for designing
        web services. Flask makes it easy to build RESTful APIs that can be consumed
        by various clients including web browsers, mobile apps, and other services.
        
        In this tutorial, we'll learn how to create endpoints that handle different
        HTTP methods and return JSON responses.
        '''
    }
]

@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404
    return render_template('post.html', post=post, posts=blog_posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Print the form information
        print("=== Contact Form Submission ===")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Email: {email}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        print("===============================")
        
        # Return the template with success message
        return render_template('contact.html', success=True)
    
    # GET request - show the form
    return render_template('contact.html')

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        author = request.form.get('author')
        content = request.form.get('content')
        
        # Basic validation
        if not all([title, subtitle, author, content]):
            flash('All fields are required!', 'error')
            return render_template('create.html')
        
        # Create new post
        new_id = max([post['id'] for post in blog_posts]) + 1 if blog_posts else 1
        new_post = {
            'id': new_id,
            'title': title,
            'subtitle': subtitle,
            'author': author,
            'date': datetime.now().strftime('%B %d, %Y'),
            'content': content
        }
        
        # Add to blog posts
        blog_posts.append(new_post)
        
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('post_detail', post_id=new_id))
    
    return render_template('create.html')

@app.route('/manage')
def manage_posts():
    return render_template('manage.html', posts=blog_posts)

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    global blog_posts
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('manage_posts'))

if __name__ == '__main__':
    app.run(debug=True)