from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo 
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)

db = client.mars_db

collection = db.mars_data

@app.route("/")
def index():

	mars_mission_data = collection.find_one()
	return render_template("index.html", mars_mission_data = mars_mission_data)

from scrape_mars import mars_scrape

@app.route("/scrape")
def scrape():
	mars_mission_data = mars_scrape()
	collection.update({"id": 1}, {"$set": mars_mission_data}, upsert = True)

	return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
	app.run(debug=True)

