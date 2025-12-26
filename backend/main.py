from fastapi import FastAPI
import pandas as pd
from pathlib import Path

app = FastAPI(title="Power Outage Dashboard API")


DATA_PATH = Path(__file__).parent / "data" / "outages.csv"
df = pd.read_csv(DATA_PATH)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/outages")
def get_outages():
    """
    Return all outage records as JSON
    """
    return df.to_dict(orient="records")
