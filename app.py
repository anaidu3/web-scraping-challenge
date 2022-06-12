from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

#import scrape_mars script
import scrape_mars

#create an instance of our Flask app
app = Flask(__name__)

#use flask pymongo to set up mongo connection
mongo = PyMongo(app, uri= 'mongodb://localhost:27017/mars_app')

# connect to mongo db and collection
@app.route("/")

def index():
    ##find one
    mars = mongo.db.mars.find_one()
    #pass that to render_template
    return render_template('index.html', mars=mars)

@app.route("/scrape")
def scrape():
    
    #create a mars database
    mars = mongo.db.mars
    
    #import python scrip to scrape data
    scraped_data = scrape_mars.scrape()
    
    #Update the Mongo database using update and upsert=True
    mars.update({},scraped_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)