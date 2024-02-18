#!/usr/bin/env python
# coding: utf-8

# In[18]:


from flask import Flask, render_template, request
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib

app = Flask(__name__)

# Load the machine learning model
model = joblib.load('cb.pkl')

# Function to encode categorical variables
def encode_categorical(value):
    return 1 if value.lower() == 'yes' or value.lower() == 'male' else 0

# List of questions and their corresponding features
questions = [
    ("Have you ever been told by a doctor, nurse or other health professional that you have high blood pressure? (yes/no): ", 'HighBP'),
    ("Have you ever been told by a doctor, nurse or other health professional that you have high cholesterol? (yes/no): ", 'HighChol'),
    ("Have you had your cholesterol checked in the last 5 years? (yes/no): ", 'CholCheck'),
    ("Please enter your BMI: ", 'BMI'),
    ("Have you smoked at least 5 packs of cigarettes in your entire life? (yes/no): ", 'Smoker'),
    ("Have you ever had a stroke? (yes/no): ", 'Stroke'),
    ("Do you have Coronary Heart Disease or myocardial infarction? (yes/no): ", 'HeartDiseaseorAttack'),
    ("Have you exercised within the last 30 days? (yes/no): ", 'PhysActivity'),
    ("Do you eat fruit one or more times a day? (yes/no): ", 'Fruits'),
    ("Do you eat vegetables one or more times a day? (yes/no): ", 'Veggies'),
    ("Are you a heavy drinker? (men: 14 or more alcoholic beverages weekly. Women: 7 or more) (yes/no): ", 'HvyAlcoholConsump'),
    ("Do you have healthcare coverage? (yes/no): ", 'AnyHealthcare'),
    ("Was there a time in the last 12 months where you wanted to see a doctor but could not afford it? (yes/no): ", 'NoDocbcCost'),
    ("On a scale of 1-5, please rate your general health (1 = excellent, 5 = poor): ", 'GenHlth'),
    ("In regard to mental health, which includes stress, depression, and problems with emotions, for how many days during the past 30 days was your mental health not good? ", 'MentHlth'),
    ("Now thinking about your physical health, which includes physical illness and injury, for how many days during the past 30 days was your physical health not good? ", 'PhysHlth'),
    ("Do you have serious difficulty walking or climbing stairs? (yes/no): ", 'DiffWalk'),
    ("Please indicate your gender (Male/Female): ", 'Sex'),
    ("Please indicate your age: ", 'Age')
]

# Render the form template
@app.route('/')
def index():
    return render_template('index.html', questions=questions)

# Handle form submission
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Process user input
        feature_vector = []
        for _, feature_name in questions:
            user_input = request.form.get(feature_name)
            if feature_name in ['BMI', 'GenHlth', 'MentHlth', 'PhysHlth', 'Age']:
                user_input = float(user_input)
            elif feature_name == 'Sex':
                user_input = encode_categorical(user_input)
            else:
                user_input = encode_categorical(user_input)
            feature_vector.append(user_input)

        # Reshape the feature vector
        feature_vector = np.array(feature_vector).reshape(1, -1)
        
        # Standard scaling
        scaler = StandardScaler()
        feature_vector_standard_scaled = scaler.transform(feature_vector)
        
        # PCA scaling
        pca = PCA(n_components=len(feature_vector[0]))
        feature_vector_pca_scaled = pca.transform(feature_vector_standard_scaled)

        # Make predictions
        prediction = model.predict(feature_vector_pca_scaled)
        
        # Return prediction to user
        if prediction == 0:
            result = "You don't have Diabetes"
        else:
            result = "You have Diabetes"
        
        return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:




