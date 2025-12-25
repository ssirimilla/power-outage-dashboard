from fastapi import FastAPI

app = FastAPI(title="Power Outage Dashboard API")


@app.get("/health")
def health_check():
    return {"status": "ok"}
