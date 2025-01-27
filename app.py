## Import the Flask class from the flask module
from flask import Flask, render_template, jsonify

app = Flask(__name__)

## Create a list of dictionaries for test
GIGS = [
    {
        'id': 1,
        'title': 'UAV Pilot',
        'description': 'We are looking for a UAV pilot to fly our drones.',
        'location': 'San Francisco, CA',
        'salary': '$100,000'
    },

    {
        'id': 2,
        'title': 'UAS Engineer 1',
        'description': 'We are looking for a UAS Engineer to help us build our drones.',
        'location': 'london, UK',
        'salary': '$102,000'
    },

    {
        'id': 3,
        'title': 'UAV Pilot Drone Operator',
        'description': 'We are looking for a UAV pilot to fly our drones.',
        'location': 'Cape Town, South Africa',
        'salary': '$95,000'
    },

    {
        'id': 4,
        'title': 'UAV/UAS 107 Pilot',
        'description': 'We are looking for a UAV and unmaned systems pilot to fly our drones.',
        'location': 'Maimi, FL',
        'salary': '$115,000'
    }]

## Create a routes
## Route for the html pages
@app.route('/')
def load_homepage():
    return render_template('index.html', 
                           gigs=GIGS,
                           company_name='DronesTube',)   

## Create API JSON Endpoints
@app.route("/api/gigs")
def list_gigs():
    return jsonify(GIGS) 

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  