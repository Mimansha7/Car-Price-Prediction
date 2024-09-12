from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Extract form data
            Present_Price = float(request.form['Present_Price'])
            Kms_Driven = int(request.form['Kms_Driven'])
            Owner = int(request.form['Owner'])
            Year = int(request.form['Year'])
            Fuel_Type = request.form['Fuel_Type']
            Seller_Type = request.form['Seller_Type']
            Transmission = request.form['Transmission']

            # Preprocess form data
            Kms_Driven2 = np.log(Kms_Driven + 1)  # Log transformation for kms driven
            no_year = 2020 - Year  # Calculate age of the car

            # One-hot encode fuel type
            fuel_Diesel = fuel_Petrol = 0
            if Fuel_Type == 'Diesel':
                fuel_Diesel = 1
            elif Fuel_Type == 'Petrol':
                fuel_Petrol = 1

            # One-hot encode seller type
            seller_type_Individual = 1 if Seller_Type == 'Individual' else 0

            # Encode transmission
            transmission_Manual = 1 if Transmission == 'Manual' else 0

            # Prepare the input array for prediction
            features = np.array([[Present_Price, Kms_Driven2, Owner, no_year,
                                  fuel_Diesel, fuel_Petrol, seller_type_Individual, transmission_Manual]])

            # Make prediction
            prediction = model.predict(features)
            output = round(prediction[0], 2)

            if output < 0:
                return render_template('index.html', prediction_texts="Sorry, you cannot sell this car")
            else:
                return render_template('index.html', prediction_text="You Can Sell The Car at ₹{}".format(output))

        except Exception as e:
            return render_template('index.html', prediction_texts=f"Error: {str(e)}")

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)