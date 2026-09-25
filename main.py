from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from curl_cffi import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/scrape")
def scrape(url: str = Query(...)):
    try:
        # Impersonates Chrome TLS/JA4 fingerprint to pass Cloudflare
        res = requests.get(url, impersonate="chrome", timeout=15)
        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=f"Upstream returned {res.status_code}")
        return {"status": "success", "html": res.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
