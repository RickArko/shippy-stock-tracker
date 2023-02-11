# Shippy Stock Tracker Assessment
See [instructions](https://shippy.notion.site/shippy/Shippy-Take-Home-Assignment-9beae0bda2434039b937f39fad154eff) for full assessment details.

# Questions
## 1. Process Data from Stocks API (Polygon)
        - [docs](https://polygon.io/docs/stocks/getting-started)
        - [python-client](https://github.com/polygon-io/client-python)
## 2. Parse Documents
## 3. (bonus) API

### **Guidelines**

1. Upload your code in a **private** Github repository and add @akshayshippy and @mohnish7 as collaborators
2. Provide all necessary code for us to replicate your database schema, backfill data and execute your code so that we can test your submission
3. Please add a README with any setup instructions for us to be able to run and test your submission
4. Write your code as if it were to be deployed on a production server and run nightly (post market close)
5. Do not upload your supabase or polygon API keys/tokens, we will point your code to our supabase project and use our own polygon API keys.


# Setup Instructions

### Installation
```
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
```


#### Configure Environment
Create local `.env` to hold api keys
```
POLYGON_API_KEY=**********************
```

### Run Local API
```
    python main.py  # update data
    uvicorn src.app:app --port 5000 --host "0.0.0.0" --reload
    python test.py  # test api
```

When the API is running see `http://localhost:5000/docs` for swagger docs.


Example post for average ohlc data.
```
    curl -X 'POST' \
    'http://localhost:5000/average_ohlc' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '[
    "AAPL", "F"
    ]'
```