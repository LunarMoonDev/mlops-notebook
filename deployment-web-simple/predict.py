import pickle
import pandas as pd

from flask import Flask, request, jsonify

with open('linear.bin', 'rb') as f_in:
    # pipeline does not have pudo feature plugged in
    (pipeline, model) = pickle.load(f_in)

def predict(ride):
    # turn it into df first
    ride_df = pd.DataFrame(ride)

    X = pipeline.transform(ride_df)
    preds = model.predict(X)
    return preds

app = Flask('duration-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()
    pred = predict(ride)

    return jsonify({'duration': float(pred[0])})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)