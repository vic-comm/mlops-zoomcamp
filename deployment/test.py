import predict, requests
ride = {'PULocationID': 10, 'DOLocationID': 50, 'trip_distance': 50}

# features = predict.prepare_features(ride)
# pred = predict.predict(features)
# print(pred)
url = 'http://127.0.0.1:9696/predict'
response = requests.post(url, json=ride)
print(response.json())