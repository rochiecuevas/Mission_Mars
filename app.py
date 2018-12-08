# Dependencies for database CRUD
from flask_pymongo import PyMongo # Use flask_pymongo to allow running MongoDB in Python
import scrape_mars

# Dependencies for rendering the information to HTML
from flask import Flask, render_template, redirect

# Create an instance for the Flask app
app = Flask(__name__)

# Connect to a MongoDB database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Call the information in the flask app 
@app.route('/')
def index():
    # Store the collection in a list
    info = mongo.db.mars_current_data.find_one()

    # Render the template with the information in it
    return render_template("index.html", list = info)

@app.route('/scrape')
def scraper():
    info = mongo.db.mars_current_data
    info_data = scrape_mars.scrape()
    info.update({}, info_data, upsert = True)
    return redirect("/", code = 302)

if __name__ == "__main__":
    app.run(debug = True)