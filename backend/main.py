from fastapi import FastAPI
import pandas as pd
from pathlib import Path

STATE_TO_ABBREV = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC"
}


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

@app.get("/outages/by-state-year")
def outages_by_state_year(year: int):
    """
    Return outage counts by state for a given year.
    Used to power choropleth map.
    """
    df_year = df[df["YEAR"] == year]

    grouped = (
        df_year
        .groupby("U.S._STATE")
        .size()
        .reset_index(name="count")
    )

    grouped["state"] = grouped["U.S._STATE"].map(STATE_TO_ABBREV)
    grouped = grouped.dropna(subset=["state"])

    return grouped[["state", "count"]].to_dict(orient="records")

