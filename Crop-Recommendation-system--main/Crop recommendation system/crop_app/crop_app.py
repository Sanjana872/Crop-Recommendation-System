import joblib
from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# Define the model file name
model_file = 'crop_file'

# Construct the full path to the model file assuming it's in the same directory as this Flask app
model_path = os.path.join(os.path.dirname(__file__), model_file)

@app.route('/')
def home():
    # Render the Home_1.html template when accessing the root URL
    return render_template('Home_1.html')

@app.route('/Predict')
def prediction():
    # Render the Index.html template when accessing the /Predict route
    return render_template('Index.html')

@app.route('/form', methods=["POST"])
def brain():
    # Extract form data
    Nitrogen = float(request.form['Nitrogen'])
    Phosphorus = float(request.form['Phosphorus'])
    Potassium = float(request.form['Potassium'])
    Temperature = float(request.form['Temperature'])
    Humidity = float(request.form['Humidity'])
    Ph = float(request.form['ph'])
    Rainfall = float(request.form['Rainfall'])
     
    # Store form data in a list
    values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]
    
    # Check if form data is valid
    if 0 < Ph <= 14 and Temperature < 100 and Humidity > 0:
        try:
            # Load the machine learning model
            model = joblib.load(model_path)
            # Make prediction using the model
            arr = [values]
            acc = model.predict(arr)
            # Render the prediction.html template with the prediction result
            return render_template('prediction.html', prediction=str(acc))
        except Exception as e:
            # Handle any errors that occur during prediction
            return f"Error occurred during prediction: {e}"
    else:
        # Return an error message if form data is invalid
        return "Sorry... Error in entered values in the form. Please check the values and fill it again."

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
