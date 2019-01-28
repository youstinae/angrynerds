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

@app.route('/elements')
def elements():
    return render_template('elements.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run()