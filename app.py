## Import the Flask class from the flask module
from flask import Flask, render_template, jsonify
from database import load_gigs_from_db # Import load_gigs_from_db function from database.py

app = Flask(__name__) # Create an instance of the Flask class
    
# Create route for the html pages and load db objects
@app.route('/') # Home page route

def load_homepage(): # Load homepage function
    gigs_list = load_gigs_from_db() # assign variable for db gigs list
    return render_template('index.html', # Load index.html template
                        gigs=gigs_list, # Pass gigs list to index.html template
                        company_name='DronesTube',)  # Pass company name to index.html template 

## Create API JSON Endpoints
@app.route("/api/gigs") # Create API route for gigs
def list_gigs(): # Define list gigs function
    gigs_list = load_gigs_from_db() # Load gigs list from database
    return jsonify(gigs_list) # Return gigs list in JSON format

# Run the app
if __name__ == '__main__': # Check if app.py is run as main program
    app.run(host='0.0.0.0', debug=True)  # Run app on localhost and debug mode