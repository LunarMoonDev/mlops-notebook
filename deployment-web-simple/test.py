import predict
import requests

ride = {
    "PULocationID": [10],
    "DOLocationID": [20],
    "trip_distance": [30],    
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=ride)
print(response.json())