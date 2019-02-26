from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars = mongo.db.mars_data.find_one()
    tables = mongo.db.tables.find_one()
    return render_template("index.html", mars=mars, tables=tables)

@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    mars_d = scrape_mars.scrape()
    mars_data.update({}, mars_d, upsert=True)
    return redirect("/", code=302)

@app.route('/shutdown')
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Shutting down Flask server...'

if __name__ == "__main__":
    app.run(debug=True)