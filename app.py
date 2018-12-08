# Dependencies for database CRUD
import pymongo # Use pymongo to allow running MongoDB in Python

# Dependencies for rendering the information to HTML
from flask import Flask, render_template

# Create an instance for the Flask app
app = Flask(__name__)

# Connect to a MongoDB database
conn = "mongodb://localhost:27017"

# Pass the connection to a pymongo instance
client = pymongo.MongoClient(conn)

# Connect to a database. If a database of the same name does not exist, it will create a new one.
db.client.mars_db

# Drop collection if it exists to remove duplicates
db.information.drop()

# Create a collection in the database containing scraping outputs
db.information.insert(mars_current_data)

# Call the information in the flask app 
@app.route('/')
def index():
    # Store the collection in a list
    info = list(db.information.find())
    print(info)

    # Render the template with the information in it
    return render_template("index.html", list = info)

if __name__ == "__main__":
    app.run(debug = True)