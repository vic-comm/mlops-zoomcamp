import os
from flask import Flask, request, jsonify
import pickle
import requests
from pymongo import MongoClient

MODEL_FILE = os.getenv('MODEL_FILE', 'lin_reg.bin')
MONGODB_ADDRESS = os.getenv('MONGODB_ADDRESS', 'mongodb://127.0.0.1:27017')
EVIDENTLY_SERVICE_ADDRESS = os.getenv('EVIDENTLY_SERVICE', 'http://127.0.0.1:5000')

with open(MODEL_FILE, 'rb') as f_in:
    (dv, model) = pickle.load(f_in)

app = Flask('duration')
mongo_client = MongoClient(MONGODB_ADDRESS)
db = mongo_client.get_database('prediction_service')
collection = db.get_collection('data')

@app.route('/predict', methods=['POST'])
def predict():
    ride = request.get_json()
    
    features = {}
    features['PU_DO'] = f"{ride['PULocationID']}_{ride['DOLocationID']}"
    features['trip_distance'] = ride['trip_distance']
    
    X = dv.transform(features)
    preds = model.predict(X)
    
    # FIX 1: Convert numpy float to standard python float
    prediction = float(preds[0])
    
    result = {'duration': prediction}
    
    # FIX 2: Pass the single float value, not the whole numpy array
    save_to_db(features, prediction)
    send_to_evidently_service(features, prediction)

    return jsonify(result)

def save_to_db(record, prediction):
    rec = record.copy()
    rec['prediction'] = prediction
    
    # FIX 3: Insert the dictionary 'rec', NOT the float 'prediction'
    collection.insert_one(rec)

def send_to_evidently_service(record, prediction):
    rec = record.copy()
    rec['prediction'] = prediction
    
    # FIX 4: Use 'json=rec' for requests. Do not use Flask's jsonify() here.
    requests.post(f"{EVIDENTLY_SERVICE_ADDRESS}/iterate/taxi", json=rec)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)