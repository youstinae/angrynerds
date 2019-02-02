from flask import Flask
from flask import render_template

app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.default')

# Load the configuration from the instance folder
# app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_object('config.development')

@app.route('/')
@app.route('/home')
def home():
    return render_template('views/index.html')

@app.route('/about')
def about():
    return render_template('views/about.html')

@app.route('/accomodation')
def accomodation():
    return render_template('views/accomodation.html')

@app.route('/gallery')
def gallery():
    return render_template('views/gallery.html')

@app.route('/blog')
def blog():
    return render_template('views/blog.html')

@app.route('/elements')
def elements():
    return render_template('views/elements.html')

@app.route('/contact')
def contact():
    return render_template('views/contact.html')

if __name__ == "__main__":
    app.run()