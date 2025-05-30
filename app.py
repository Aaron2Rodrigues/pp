from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os
from src.Project1.pipeline.prediction_pipeline import PredictionPipeline

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/train', methods=['GET'])
def train():
    os.system("python main.py")
    return "Model training initiated!"

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try:
            fixed_acidity = float(request.form['fixed_acidity'])
            volatile_acidity = float(request.form['volatile_acidity'])
            citric_acid = float(request.form['citric_acid'])    
            residual_sugar = float(request.form['residual_sugar'])
            chlorides = float(request.form['chlorides'])
            free_sulfur_dioxide = float(request.form['free_sulfur_dioxide'])
            total_sulfur_dioxide = float(request.form['total_sulfur_dioxide'])  
            density = float(request.form['density'])
            pH = float(request.form['pH'])
            sulphates = float(request.form['sulphates'])
            alcohol = float(request.form['alcohol'])

            data = np.array([fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
                             free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol]).reshape(1, -1)

            obj = PredictionPipeline()
            predict = obj.predict(data)

            return render_template('results.html', prediction=str(predict))
        except Exception as e:
            return f"Something went wrong: {str(e)}"
    else:
        return render_template('index.html')
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port= 8080,debug=True) 

