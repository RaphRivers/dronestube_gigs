from flask import Flask, render_template
from flask import Flask

app = Flask(__name__)

@app.route('/')

def load_homepage():
    return render_template('index.html')      

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  