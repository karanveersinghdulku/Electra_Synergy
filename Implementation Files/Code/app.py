from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import pickle

app = Flask(__name__)

# Load the saved model
with open('naive_bayes_model.pkl', 'rb') as file:
    knn_model = pickle.load(file)
    
################################################
@app.route('/', methods=['POST','GET'] )
def first():
    return render_template('home.html')

################################################
users = {
    "electric": "pass123",
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            return render_template('main.html')
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html', error="")

#################################################

# Define a route to render the home page
@app.route('/home', methods=['POST','GET'] )
def home():
    return render_template('main.html')

#################################################

# Define a route to handle form submission and make predictions
@app.route('/predict', methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        # Get user input from the form
        start_hour = float(request.form['start_hour'])
        end_hour = float(request.form['end_hour'])
        duration = float(request.form['duration'])

        # Create a DataFrame from user input
        new_input_data = pd.DataFrame({
            'Start_plugin_hour': [start_hour],
            'End_plugout_hour': [end_hour],
            'Duration_hours': [duration]
        })

        # Make predictions using the loaded model
        prediction = knn_model.predict(new_input_data)
        return render_template('main.html', prediction=prediction[0])
    
##################################################
@app.route('/performance')
def performance():
    return render_template('performance.html')

#################################################
@app.route('/logout')
def logout():
    return render_template('home.html')

#################################################
@app.route('/about')
def about():
    return render_template('about.html')








if __name__ == '__main__':
    app.run()
