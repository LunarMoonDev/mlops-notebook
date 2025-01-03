### CURL command for the API trigger

```curl
curl -X POST http://localhost:6789/api/runs \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer 857ea51208ad4e2ca57aa9e54f8b36d9' \
  --data '{
    "run": {
        "pipeline_uuid": "predict",
        "block_uuid": "inference",
        "variables": {
            "inputs": [
                {
                    "DOLocationID": "239",
                    "PULocationID": "236",
                    "trip_distance": 1.98
                },
                {
                    "DOLocationID": "239",
                    "PULocationID": "236",
                    "trip_distance": 1.98
                }
            ]
        }
    }
}'