from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__, instance_relative_config=True)
app.secret_key = b'\xbb.@\xb7S<\x9a\xd7\x8a\x0cz/\xb5\xce\xc1\xee\xc7\xd8v\xa1)\xec\xdd\x07'

# Load the default configuration
app.config.from_object('config.default')

# Load the configuration from the instance folder
# app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_object('config.development')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/accomodation')
def accomodation():
    return render_template('accomodation.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/blog/details')
def blog_details():
    return render_template('blog-details.html')

@app.route('/elements')
def elements():
    return render_template('elements.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=["POST"])
def login_post():
    #login()
    return redirect(url_for('index'))

@app.route('/logout', methods=["POST"])
def logout():
    # logout the user and redirect to home page
    return render_template('login.html')

if __name__ == "__main__":
    app.run()